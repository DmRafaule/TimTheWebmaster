from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()


@register.filter(name='listToURL')
def listToURL(list):
    ''' Конвертирует список в строку УРЛ для списка тегов '''
    path = ''
    for item in list:
        path += f'&tag={item}'
    return path