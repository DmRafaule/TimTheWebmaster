from urllib.parse import urlsplit

from django import template
from django.http import QueryDict
from django.template.defaultfilters import stringfilter
from django.db.models import Q

from Post.models import Tag, Category


def remove_items(list, item): 
    ''' Удаляет item из списка '''
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 

register = template.Library()

@register.filter(name='switchLang')
@stringfilter
def switchLang(path, locale):
    ''' Меняет язык УРЛа'''
    url_dict = urlsplit(path)
    updated_url = f"{url_dict.path}/{url_dict.query}"
    urlList = updated_url.split('/')
    # Подчищаем за собой
    urlList = remove_items(urlList, '')
    new_path = ""
    category = None
    for indx, url in enumerate(urlList):
        level = indx + 1
        match level:
            # Домашняя страница
            case 1:
                new_path = '/'.join([new_path, locale])
            # Категория или статические страницы
            case 2:
                category = Category.objects.filter(slug=url).first()
                new_path = '/'.join([new_path, url])
            # Пагинация, Подкатегория пагинации или Пост
            case 3:
                # Это Пагинация 
                if url.startswith('page='):
                    query_dict = QueryDict(url).copy()
                    tag_slugs = query_dict.getlist("tag")
                    new_slugs = []
                    for slug in tag_slugs:
                        tag = Tag.objects.filter(Q(slug_en=slug) | Q(slug_ru=slug)).first()
                        field_name = f"slug_{locale}"
                        new_slugs.append(getattr(tag, field_name, None))
                    query_dict.setlist('tag', new_slugs)
                    new_url = f"?{query_dict.urlencode()}"
                    new_path = '/'.join([new_path, new_url])
                else:
                    subcategory = Tag.objects.filter(Q(slug_en=url) | Q(slug_ru=url)).first()
                    # Это Подкатегория
                    if subcategory and category:
                        field_name = f"slug_{locale}"
                        slug_value = getattr(subcategory, field_name, None)
                        new_path = '/'.join([new_path, slug_value])
                    # Это Пост
                    else:
                        new_path = '/'.join([new_path, url])
            # Пост в подкатегории
            case 4:
                new_path = '/'.join([new_path, url])
    new_path += '/'
    return new_path
