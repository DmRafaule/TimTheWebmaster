from django import template
from urllib.parse import urlsplit

register = template.Library()

def remove_items(list, item): 
    ''' Удаляет item из списка '''
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 


@register.filter(name='urlToList')
def urlToList(url: str):
    ''' Конвертирует УРЛ в список '''
    url_dict = urlsplit(url)
    # Собираем новый УРЛ только с необхдимыми данными (всё что после TLD)
    updated_url = f"{url_dict.path}/{url_dict.query}"
    urlList = updated_url.split('/')
    # Подчищаем за собой
    urlList = remove_items(urlList, '')
    return urlList