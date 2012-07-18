from django import template
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.db.models import get_model
from django.utils.safestring import mark_safe

import re

register = template.Library()


kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

@register.tag
def childcrud_config(parser, token):
    # split_contents() knows not to split quoted strings.
    bits = token.split_contents()
    if len(bits) < 4:
        raise template.TemplateSyntaxError("'%s' takes at least three arguments"
                              " (parent, parent_id, child)" % bits[0])
    tag_name = bits[0]
    parent = bits[1]
    parent_id = bits[2]
    child = bits[3]
    
    # check additional keyword args
    options = {}
    if len(bits) >= 4:
        for bit in bits[4:]:
            match = kwarg_re.match(bit)
            if not match:
                raise template.TemplateSyntaxError("Malformed additional keyword arguments to %s tag" % tag_name)
            name, value = match.groups()
            options[name] = mark_safe(value)
            
    if not (parent[0] == parent[-1] and parent[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's parent argument should be in quotes" % tag_name
    if not (child[0] == child[-1] and child[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's child argument should be in quotes" % tag_name
    parent = parent[1:-1]
    child = child[1:-1]

    return ChildCRUDNode(parent, parent_id, child, options)


class ChildCRUDNode(template.Node):
    def __init__(self, parent, parent_id, child, options=None):
        self.parent_string = parent
        self.parent_id = template.Variable(parent_id)
        self.child_string = child
        self.options = options
    
    def render(self, context):
        parent_id = self.parent_id.resolve(context)
        variable_name = '%s-%s' % (self.parent_string.split('.')[-1], self.child_string.split('.')[-1])
        context.dicts[0][variable_name] = ChildCrud(self.parent_string, parent_id, self.child_string, self.options)
        t = template.loader.get_template('childcrud/childcrud_config.js')
        ctx = template.Context({'variable_name': variable_name, 
                                'urls': context.dicts[0][variable_name].get_urls(),
                                'options': self.options})
        return t.render(ctx)
        

@register.tag
def childcrud_html(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, parent, parent_id, child = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    if not (parent[0] == parent[-1] and parent[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's parent argument should be in quotes" % tag_name
    if not (child[0] == child[-1] and child[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's child argument should be in quotes" % tag_name
    parent = parent[1:-1]
    child = child[1:-1]

    return ChildCRUDHTMLNode(parent, parent_id, child)

class ChildCRUDHTMLNode(template.Node):
    def __init__(self, parent, parent_id, child):
        self.parent_string = parent
        self.parent_id = template.Variable(parent_id)
        self.child_string = child
        self.variable_name = '%s-%s' % (self.parent_string.split('.')[-1], self.child_string.split('.')[-1])
    
    def render(self, context):
        parent_id = self.parent_id.resolve(context)
        try:
            cfg = context.dicts[0][self.variable_name]
        except KeyError:
            raise Exception("Chamando tag childcrud_html sem chamar childcrud_config antes para '%s e %s'" % (self.parent_string, self.child_string))
        dialog = cfg.options.get('dialog', '').replace("'", "").replace('"','')
        verbose_name = ''
        if dialog:
            verbose_name = cfg.child_model._meta.verbose_name.capitalize()
        t = template.loader.get_template('childcrud/childcrud_config.html')
        ctx = template.Context({'variable_name': self.variable_name, 'dialog': dialog, 'verbose_name': verbose_name})
        return t.render(ctx)

        
        
        
class ChildCrud(object):
    def __init__(self, parent, parent_id, child, options):
        self.parent_string = parent
        self.parent_app = '.'.join(parent.split('.')[:-1])
        self.parent_name = parent.split('.')[-1]
        self.parent_model = get_model(self.parent_app, self.parent_name)
        self.parent_id = parent_id
        self.child_string = child
        self.child_app = '.'.join(child.split('.')[:-1])
        self.child_name = child.split('.')[-1]
        self.child_model = get_model(self.child_app, self.child_name)
        self.options = options
        self.child_model_admin = admin.site._registry.get(self.child_model, None)
        if options:
            if options.get('sticky_form', '') == 'true':
                setattr(self.child_model_admin, 'sticky_form', True)
                
    
    def get_urls(self):
        urls = {'new': reverse('childcrud-create', 
                               kwargs={'p_app_name': self.parent_app, 
                                       'p_model_name': self.parent_name,
                                       'p_id': self.parent_id,
                                       'app_name': self.child_app,
                                       'model_name': self.child_name}),
                'list': reverse('childcrud-list', 
                                kwargs={'p_app_name': self.parent_app, 
                                        'p_model_name': self.parent_name,
                                        'p_id': self.parent_id,
                                        'app_name': self.child_app,
                                        'model_name': self.child_name}),
                'edit': reverse('childcrud-update', 
                                kwargs={'p_app_name': self.parent_app, 
                                        'p_model_name': self.parent_name,
                                        'p_id': self.parent_id,
                                        'app_name': self.child_app,
                                        'model_name': self.child_name,
                                        'id': 0}),
        }
        return urls