from django import template
from urllib.parse import urlsplit

register = template.Library()

def remove_items(list, item): 
    # remove the item for all its occurrences 
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 


@register.filter(name='urlToList')
def urlToList(url: str):
    url_dict = urlsplit(url)
    updated_url = f"{url_dict.path}/{url_dict.query}"
    urlList = updated_url.split('/')
    # Clean up after slplit function
    urlList = remove_items(urlList, '')
    return urlList