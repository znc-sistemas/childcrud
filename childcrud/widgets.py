# coding: utf-8

import json
import re

from django.forms.widgets import Select
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
#from templatetags import CHILDCRUD_UI

CHILDCRUD_UI = getattr(settings, 'CHILDCRUD_UI', 'jqueryui')


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
                op_str = json.dumps(self.options).replace('"', "'")
                op_str = re.sub(r"\'formload_cb\': \'(.*)\',", r"'formload_cb': \1,", op_str)
            else:
                op_str = 'null'
            params = {
                'url_new': reverse('fk-create', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.model_name.lower()}),
                'url_upd': reverse('fk-update', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.model_name.lower(), 'id': '0'}),
                'titulo': self.rel._meta.verbose_name.capitalize(),
                'id': attrs.get('id', name),
                'style': not value and 'style="display:none"' or '',
                'static_url': settings.STATIC_URL,
                'options': op_str
            }

            bts = u"""<a href="#" onclick="return fk_dialog(this, \'%(url_new)s\', \'%(titulo)s\', %(options)s)" title="Adicionar..."><i class="icon-plus"></i></a>
            <a href="#" id="bt-%(id)s-editar" onclick="return fk_dialog(this, \'%(url_upd)s\', \'%(titulo)s\', %(options)s)" title="Editar..." %(style)s><i class="icon-edit"></i></a>"""

            if CHILDCRUD_UI == 'bootstrap':
                bts = bts + u"""<div id="%(id)s-dialog" class="modal hide fade">
                <div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3></h3></div>
                <div class="modal-body"></div>
                </div>"""
            else:
                bts = bts + u"""<div id="%(id)s-dialog"></div>"""

            bts = bts % params
        return mark_safe(u'%s%s' % (output, bts))

    class Media:
        css = {
            'all': (getattr(settings, 'JQUERY_UI_THEME', '/static/css/Aristo/jquery-ui-1.8.7.custom.css'),)
        }
        js = ('js/jquery-ui-1.7.2.custom.min.js', 'js/jquery.form.js', 'js/fk-edit.js',)
