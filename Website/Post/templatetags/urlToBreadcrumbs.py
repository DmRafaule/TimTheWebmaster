from django import template
from Post.models import Category, Tag, Article, Tool, Post
from django.utils.translation import gettext as _
from django.db.models import Q
from urllib.parse import urlsplit
from django.shortcuts import get_object_or_404

register = template.Library()

def remove_items(list, item): 
    ''' Удаляет item из списка '''
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 


@register.filter(name='urlToBreadcrumbs')
def urlToBreadcrumbs(url: str):
    ''' Конвертирует УРЛ в список для использования в Хлебных крошках '''
    # Собираем новый УРЛ только с необхдимыми данными (всё что после TLD)
    url_dict = urlsplit(url)
    updated_url = f"{url_dict.path}/{url_dict.query}"
    urlList = updated_url.split('/')
    # Подчищаем за собой
    urlList = remove_items(urlList, '')
    result_list = []
    curr_url = ''
    current_category = None
    for indx, url in enumerate(urlList):
        level = indx + 1
        match level:
            # Первый уровень это домашняя страница, с выбранным языком
            case 1:
                curr_url = '/'.join([curr_url, url])
                name = ''
                if url == 'ru':
                    name = _("На русском")
                elif url == 'en':
                    name = _("На английском")
                result_list.append({
                    'name': name,
                    'url': curr_url + '/',
                    'level': level
                })
            # Второй уровень это либо путь до категорий постов или статический страницы
            case 2:
                cat = Category.objects.filter(slug=url).first()
                cat_url = ""
                if cat:
                    current_category = cat
                    name = cat.name
                    cat_url = cat.get_absolute_url()
                else:
                    if url == 'about':
                        name = _('Об авторе')
                    elif url == 'contacts':
                        name = _('Контакты')
                curr_url = cat_url
                result_list.append({
                    'name': name,
                    'url': curr_url,
                    'level': level
                })
            # Третий уровень, либо посты, либо страницы пагинации, либо подкатегории
            case 3:
                # Проверяем является ли эта страница, страница пагинации, если нет то предполагаем что это пост
                if url.startswith('page='):
                    parse_res = url.split('&')
                    curr_url = '/'.join([curr_url, f'?{url}'])
                    args = {}
                    tag_counter = 0
                    for item in parse_res:
                        item_key_value = item.split('=')
                        # Если элемент строки запроса не тег (а например сортировка или фильтрация)
                        if item_key_value[0] != 'tag':
                            args.update({item_key_value[0]: item_key_value[1]})
                        # Иначе это тег, сохраняю его как, например tag1, tag2, чтобы после было легко получить к действительному имени тега
                        else:
                            args.update({item_key_value[0] + str(tag_counter): item_key_value[1]})
                            # Считаем сколько тегов в УРЛе
                            tag_counter += 1
                    name = _("Страница ") + args['page']
                    # Если есть хотя бы один тег, то генерируем имя для 2-ого уровня "Хлебных крошек"
                    if tag_counter >= 1:
                        name += ', '
                        for i in range(tag_counter): 
                            # Здесь проводиться поиск действительного имени в базе данных.
                            # Причём возвращается его локализованная версия
                            tag = get_object_or_404(Tag, Q(slug_en=args['tag' + str(i)]) | Q(slug_ru=args['tag' + str(i)]))
                            name += ','.join([tag.name, ' ' ])
                    result_list.append({
                        'name': name,
                        'url': curr_url,
                        'level': level
                    })
                # Значит это пост статьи или инструмента
                else:
                    # Ищем тег (подкатегорию)
                    tag = Tag.objects.filter(
                        Q(slug_en=url) | Q(slug_ru=url)
                    ).first()

                    # Это Подкатегория
                    if tag and current_category:
                        tag_url = f'{current_category.get_absolute_url()}{tag.slug}/'
                        curr_url = tag_url
                        result_list.append({
                            'name': tag.name,
                            'url': curr_url,
                            'level': level,
                        })
                    # Если не тег, значит это пост
                    else:
                        article = Article.objects.filter(slug=url).first()
                        tool = Tool.objects.filter(slug=url).first()
        
                        post = article or tool
                        if post:
                            curr_url = post.get_absolute_url()
                            post_name = (
                                getattr(post, 'title', None)
                                or getattr(post, 'name', None)
                                or url
                            )
                            result_list.append(
                                {'name': post_name, 'url': curr_url, 'level': level}
                            )
                        else:
                            curr_url = f'{curr_url}{url}/'
                            result_list.append(
                                {'name': url.capitalize(), 'url': curr_url, 'level': level}
                            )
            # Четвёртый уровень - Пост, находящийся внутри подкатегории ---
            case 4:
                article = Article.objects.filter(slug=url).first()
                tool = Tool.objects.filter(slug=url).first()

                post = article or tool
                if post:
                    # Вызываем get_absolute_url() объекта — он вернет полностью актуальный переведенный URL
                    curr_url = post.get_absolute_url()
                    post_name = (
                        getattr(post, 'title', None)
                        or getattr(post, 'name', None)
                        or url
                    )
                    result_list.append(
                        {'name': post_name, 'url': curr_url, 'level': level}
                    )
                else:
                    curr_url = f'{curr_url}{url}/'
                    result_list.append(
                        {'name': url.capitalize(), 'url': curr_url, 'level': level}
                )
            case _:
                curr_url = '/'.join([curr_url, url])
                result_list.append({
                    'name': url.capitalize(),
                    'url': curr_url + '/',
                    'level': level
                })
    
    return result_list