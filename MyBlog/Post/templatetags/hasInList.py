from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='hasInList')
@stringfilter
def hasInList(value, arg):
    if value in arg:
        return True
    else:
        return False