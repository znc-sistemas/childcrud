from django import template

register = template.Library()


@register.simple_tag
def form_field(field, additional_text="", required=False, label=True):
    t = template.loader.get_template('form_field.html')
    return t.render(
        template.Context(
            {
                'field': field, 'additional_text': additional_text,
                'required': required,
                'label': label
            }
        )
    )
