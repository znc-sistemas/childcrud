# coding: utf-8

import json
import re

from django.forms.widgets import Select
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template.loader import get_template
# from templatetags import CHILDCRUD_UI

CHILDCRUD_UI = getattr(settings, 'CHILDCRUD_UI', 'jqueryui')


class SelectFKWidget(Select):
    def __init__(self, attrs=None, choices=(), rel=None, options=None):
        super(SelectFKWidget, self).__init__(attrs, choices)
        self.rel = rel
        self.options = options

    def render(self, name, value, attrs=None, renderer=None):
        attrs.update({'onchange': 'changeFK(this)'})
        output = super(SelectFKWidget, self).render(name, value, attrs)
        bts = ''
        if self.rel:
            if self.options:
                op_str = json.dumps(self.options).replace('"', "'")
                op_str = re.sub(r"\'formload_cb\': \'(.*)\',", r"'formload_cb': \1,", op_str)
            else:
                op_str = 'null'

            context = {
                'url_new': reverse('fk-create', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.model_name.lower()}),
                'url_upd': reverse('fk-update', kwargs={'app_name': self.rel._meta.app_label, 'model_name': self.rel._meta.model_name.lower(), 'id': '0'}),
                'titulo': self.rel._meta.verbose_name.capitalize(),
                'id': attrs.get('id', name),
                'style': not value and 'style="display:none"' or '',
                'static_url': settings.STATIC_URL,
                'options': op_str,
                'fkedit_modal_template': 'childcrud/{}/fkedit_modal.html'.format(CHILDCRUD_UI),
                'fkedit_add_icon_template': 'childcrud/{}/fkedit_add_icon.html'.format(CHILDCRUD_UI),
                'fkedit_edit_icon_template': 'childcrud/{}/fkedit_edit_icon.html'.format(CHILDCRUD_UI),
            }

            bts = get_template("childcrud/{}/fkedit_widget.html".format(CHILDCRUD_UI)).render(context)

        return mark_safe('%s%s' % (output, bts))

    class Media:
        css = {
            'all': (getattr(settings, 'JQUERY_UI_THEME', '/static/css/Aristo/jquery-ui-1.8.7.custom.css'),)
        }
        js = ('js/jquery-ui-1.7.2.custom.min.js', 'js/jquery.form.js', 'js/fk-edit.js',)
