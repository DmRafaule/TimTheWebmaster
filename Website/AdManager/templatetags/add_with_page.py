from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def add_with_page(value, page):
    if page != "NO_PAGINATION":
        return value.replace("{{PAGE}}", str(page))
    else:
        return value.replace("-{{PAGE}}", "")