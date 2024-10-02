from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()

def remove_items(list, item): 
    # remove the item for all its occurrences 
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 


@register.filter(name='urlToList')
def urlToList(url: str):
    urlList = url.split('/')
    # Clean up after slplit function
    urlList = remove_items(urlList, '')
    return urlList