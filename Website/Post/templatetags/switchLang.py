from urllib.parse import urlsplit, urlunsplit

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
    new_list = []
    category = None
    for indx, url in enumerate(urlList):
        level = indx + 1
        match level:
            # Домашняя страница
            case 1:
                new_list.append(locale)
            # Категория или статические страницы
            case 2:
                category = Category.objects.filter(slug=url).first()
                # Категории
                if category:
                    new_list.append(category.slug)
                # Статические страницы
                else:
                    new_list.append(url)
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
                    new_query = f"?{query_dict.urlencode()}"
                    new_list.append(new_query)
                else:
                    subcategory = Tag.objects.filter(Q(slug_en=url) | Q(slug_ru=url)).first()
                    # Это Подкатегория
                    if subcategory and category:
                        field_name = f"slug_{locale}"
                        slug_value = getattr(subcategory, field_name, None)
                        new_list.append(slug_value)
                    # Это Пост
                    else:
                        new_list.append(url)
            # Пост в подкатегории, Пагинация
            case 4:
                if url.startswith('page='):
                    query_dict = QueryDict(url).copy()
                    tag_slugs = query_dict.getlist("tag")
                    new_slugs = []
                    for slug in tag_slugs:
                        tag = Tag.objects.filter(Q(slug_en=slug) | Q(slug_ru=slug)).first()
                        field_name = f"slug_{locale}"
                        new_slugs.append(getattr(tag, field_name, None))
                    query_dict.setlist('tag', new_slugs)
                    new_query = f"?{query_dict.urlencode()}"
                    new_list.append(new_query)
                else:
                    new_list.append(url)
    new_path = f"/{'/'.join(new_list)}"
    match(len(new_list)):
        # Домашняя, Категория, Статическая страница
        case 1:
            new_path += '/'
        case 2:
            new_path += '/'
        # Пагинация, Подкатегория или Пост
        case 3:
            # Пагинация
            if url.startswith('page='):
                pass
            # Подкатегория или Пост
            else:
                new_path += '/'
        # Пост в подкатегории, Пагинация подкатегории
        case 4:
            # Пагинация подкатегории
            if url.startswith('page='):
                pass
            # Пост в подкатегории
            else:
                new_path += '/'
    print(new_path)
    return new_path
