from django import template
from django.contrib.admin import helpers
from django.template.loader import get_template

register = template.Library()

@register.simple_tag(takes_context=True)
def inline_form(context, fieldset):
    inline_fieldset = context["inline_admin_formsets"][fieldset.description]
    template = get_template(inline_fieldset.opts.template)
    if template is None:
        return ""
    return template.render({'inline_admin_formset': inline_fieldset})
