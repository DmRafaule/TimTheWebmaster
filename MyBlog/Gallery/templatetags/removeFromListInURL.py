from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name='removeFromListInURL')
@stringfilter
def removeFromListInURL(value, arg):
    path = ''
    for item in arg:
        if item != value:
            path += f'&tag={item}'
    return path
