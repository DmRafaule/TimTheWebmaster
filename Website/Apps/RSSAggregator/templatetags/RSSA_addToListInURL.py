from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name='RSSA_addToListInURL')
@stringfilter
def RSSA_addToListInURL(url, list_of_urls):
    if url != 'None' or len(list_of_urls) == 0:
        path = f'?feed={url}'
    else:
        path = ''

    for item in list_of_urls:
        if url != item:
            if len(path) > 0:
                path += f'&feed={item}'
            else:
                path += f'?feed={item}'
    return path