from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name='RSSA_removeFromListInURL')
@stringfilter
def RSSA_removeFromListInURL(url, list_of_urls):
    path = ''
    for item in list_of_urls:
        if item != url:
            if len(path) > 0:
                path += f'&feed={item}'
            else:
                path += f'?feed={item}'
    return path
