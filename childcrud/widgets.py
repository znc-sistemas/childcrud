# coding: utf-8
from django.forms.widgets import Select
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import simplejson
import re


class SelectFKWidget(Select):
    def __init__(self, attrs=None, choices=(), rel=None, options=None):
        super(SelectFKWidget, self).__init__(attrs, choices)
        self.rel = rel
        self.options = options

    def render(self, name, value, attrs=None, choices=()):
        attrs.update({'onchange': 'changeFK(this)'})
        output = super(SelectFKWidget, self).render(name, value, attrs, choices=choices)
        bts = ''
        if self.rel:
            if self.options:
                op_str = simplejson.dumps(self.options).replace('"', "'")
                op_str = re.sub(r"\'formload_cb\': \'(.*)\',", r"'formload_cb': \1,", op_str)
            else:
                op_str = 'null'
            params = {
                'url_new': reverse('fk-create', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.module_name.lower()}),
                'url_upd': reverse('fk-update', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.module_name.lower(), 'id': '0'}),
                'titulo': self.rel._meta.verbose_name.capitalize(),
                'id': attrs.get('id', name),
                'style': not value and 'style="display:none"' or '',
                'static_url': settings.STATIC_URL,
                'options': op_str
            }
            bts = u"""<a href="#" onclick="return fk_dialog(this, \'%(url_new)s\', \'%(titulo)s\', %(options)s)" title="Adicionar..."><img src="%(static_url)simg/go-up.png" style="vertical-align:middle"/></a>
            <a href="#" id="bt-%(id)s-editar" onclick="return fk_dialog(this, \'%(url_upd)s\', \'%(titulo)s\', %(options)s)" title="Editar..." %(style)s><img src="%(static_url)simg/go-up.png" style="vertical-align:middle"/></a>
            <div id="%(id)s-dialog"></div>""" % params
        return mark_safe(u'%s%s' % (output, bts))

    class Media:
        css = {
            'all': (getattr(settings, 'JQUERY_UI_THEME', '/static/css/Aristo/jquery-ui-1.8.7.custom.css'),)
        }
        js = ('js/jquery-ui-1.7.2.custom.min.js', 'js/jquery.form.js', 'js/fk-edit.js',)
