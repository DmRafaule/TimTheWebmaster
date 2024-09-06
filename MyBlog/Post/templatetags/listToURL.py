from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()


@register.filter(name='listToURL')
def listToURL(list):
    path = ''
    for item in list:
        path += f'&tag={item}'
    return path