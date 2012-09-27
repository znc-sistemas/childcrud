# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import get_model, DateField, DateTimeField
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe

import os


@login_required
def ajax_create_update(request, p_app_name, p_model_name, p_id, app_name, model_name, id=None, form_class=None):
    parent_model = get_model(p_app_name, p_model_name)
    model = get_model(app_name, model_name)

    inst_parent = get_object_or_404(parent_model, pk=p_id)

    admin_registry = admin.site._registry
    if model not in admin_registry:
        raise Exception(u"Model '%s.%s' not registered!" % (app_name, model_name))

    model_admin = admin_registry[model]

    sticky_form = getattr(model_admin, 'sticky_form', False)
    keep_in_edit_form = getattr(model_admin, 'keep_in_edit_form', False)

    variable_name = '%s-%s' % (p_model_name, model_name)

    # verifies child ID to determine it's an update
    instance = None
    if id:
        instance = get_object_or_404(model, pk=id)

    if not form_class:
        form_class = model_admin.get_form(request, instance, parent_model=parent_model)

    kw = {'instance': instance}
    # pass the parent instance to the form constructor?
    if getattr(model_admin, 'form_receives_parent', False):
        kw[str(p_model_name)] = inst_parent
    # pass the request to the form constructor?
    if getattr(model_admin, 'form_receives_request', False):
        kw['request'] = request

    form = form_class(request.POST or None, request.FILES or None, **kw)

    msg = ''
    if request.method == "POST":
        # create and update
        if form.is_valid():
            instance = form.save(commit=False)
            model_admin.save_model(request, instance, form, change=id, parent_obj=inst_parent)

            msg = id and u"Item atualizado com sucesso!" or u"Novo item criado com sucesso!"
            # form novo
            if not id or (id and not keep_in_edit_form):
                form = form_class(None, None, **dict([(k, v) for k, v in kw.items() if k != 'instance']))

    return render_to_response(['%s/childcrud_%s_form.html' % (app_name, variable_name),
                               '%s/childcrud_%s_form.html' % (app_name, model_name),
                               'childcrud/childcrud_form.html'],
                              {'form': form, 'action': request.path,
                               'msg': msg, 'variable_name': variable_name,
                               'parent_object': inst_parent,
                               'show_form': sticky_form or (not sticky_form and not msg)},
                              context_instance=RequestContext(request))


@login_required
def ajax_list(request, p_app_name, p_model_name, p_id, app_name, model_name):
    parent_model = get_model(p_app_name, p_model_name)
    model = get_model(app_name, model_name)

    inst_parent = get_object_or_404(parent_model, pk=p_id)

    admin_registry = admin.site._registry
    if model not in admin_registry:
        raise Exception(u"Model '%s.%s' not registered!" % (app_name, model_name))

    variable_name = '%s-%s' % (p_model_name, model_name)

    model_admin = admin_registry[model]

    model_admin.set_parent_info(parent_model)

    can_edit = request.user.is_authenticated()

    # if ModelAdmin has check_can_edit callback method, call it to update can_edit
    if (hasattr(model_admin, 'check_can_edit')):
        can_edit = model_admin.check_can_edit(request, parent_obj=inst_parent)

    msg = ''
    if request.method == "POST":
        del_id = request.POST.get('del', '')
        if del_id:
            # delete objects from the list
            del_kw = {model_admin.fk_name: str(p_id), 'pk': str(del_id)}

            #obj = model.objects.filter(**del_kw)
            obj = model_admin.queryset(request).filter(**del_kw)

            model_admin.delete_model(request, obj, parent_obj=inst_parent)
            msg = u'Item excluído com sucesso!'

    kw = {model_admin.fk_name: str(p_id)}
    object_list = model_admin.queryset(request).filter(**kw)

    headers = []
    cols = []
    has_add_info = False
    has_upd_info = False

    list_fields = list(model_admin.list_display)
    for f in ('action_checkbox', '__str__', '__unicode__',):
        if f in list_fields:
            list_fields.remove(f)

    if list_fields:
        if model._meta.pk.name not in list_fields:
            list_fields.insert(0, model._meta.pk.name)
        fields = [model._meta.get_field(f) for f in list_fields]
    else:
        fields = model._meta.fields

    for field in fields:
        if not field.primary_key and field.name not in (model_admin.fk_name, 'user_upd', 'date_upd', 'user_add', 'date_add'):
            headers.append(field.verbose_name.capitalize())
        if field.name == 'user_add':
            has_add_info = True
        if field.name == 'user_upd':
            has_upd_info = True
        if field.name not in (model_admin.fk_name, 'user_upd', 'date_upd', 'user_add', 'date_add'):
            cols.append(field.name)
    if has_add_info:
        headers.append(u'Cadastro')
    if has_upd_info:
        headers.append(u'Atualização')

    rows = []
    for obj in object_list:
        row = []
        for col in cols:
            field = model._meta.get_field(col)
            if field.choices:
                data = getattr(obj, 'get_%s_display' % field.name)()
                if data is None:
                    data = '--'
            else:
                data = getattr(obj, field.name)
                if data is None:
                    data = '--'
                else:
                    if isinstance(field, DateField):
                        data = data.strftime("%d/%m/%Y")
                    elif isinstance(field, DateTimeField):
                        data = data.strftime("%d/%m/%Y %H:%M")
                    elif isinstance(data, File):
                        if unicode(data):
                            data = mark_safe('<a href="%s" class="download-link">%s</a>' % (data.url, os.path.basename(unicode(data))))
                        else:
                            data = ''
            row.append(data)
        if has_add_info:
            if obj.date_add:
                date_add = obj.date_add.strftime("%d/%m/%Y %H:%M")
            else:
                date_add = "--"
            if obj.user_add_id:
                user_add = obj.user_add.get_full_name() or obj.user_add
            else:
                user_add = "--"
            row.append(mark_safe('<span class="discreet">%s<br />%s</span>' % (user_add, date_add)))
        if has_upd_info:
            if obj.date_upd:
                date_upd = obj.date_upd.strftime("%d/%m/%Y %H:%M")
            else:
                date_upd = "--"
            if obj.user_upd_id:
                user_upd = obj.user_upd.get_full_name() or obj.user_upd
            else:
                user_upd = "--"
            row.append(mark_safe('<span class="discreet">%s<br />%s</span>' % (user_upd, date_upd)))
        rows.append(row)

    return render_to_response(['%s/childcrud_%s_list.html' % (app_name, variable_name),
                               '%s/childcrud_%s_list.html' % (app_name, model_name),
                               'childcrud/childcrud_list.html'],
                              {'object_list': object_list,
                               'parent_object': inst_parent,
                               'headers': headers,
                               'rows': rows,
                               'has_add_info': has_add_info,
                               'has_upd_info': has_upd_info,
                               'variable_name': variable_name,
                               'can_edit': can_edit,
                               'msg': msg,
                               'request': request},
                              context_instance=RequestContext(request))
