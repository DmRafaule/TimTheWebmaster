from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='addToListInURL')
@stringfilter
def addToListInURL(value, arg):
    path = f'&tag={value}'
    for item in arg:
        if value != item:
            path += f'&tag={item}'
    return path