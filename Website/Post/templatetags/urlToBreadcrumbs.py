from django import template
from Post.models import Category, Tag, Article, Termin, Question, Tool
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
    for indx, url in enumerate(urlList):
        match indx + 1:
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
                    'level': indx + 1
                })
            # Второй уровень это либо путь до категорий постов или статический страницы
            case 2:
                curr_url = '/'.join([curr_url, url])
                cat = Category.objects.filter(slug=url)
                if len(cat) == 1:
                    name = cat[0].name
                else:
                    if url == 'about':
                        name = _('Об авторе')
                    elif url == 'contacts':
                        name = _('Контакты')
                result_list.append({
                    'name': name,
                    'url': curr_url + '/',
                    'level': indx + 1
                })
            # Третий уровень, либо посты, либо страницы пагинации
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
                        'level': indx + 1
                    })
                # Значит это пост статьи или инструмента
                else:
                    curr_url = '/'.join([curr_url, url])
                    name = None
                    # Такого поста может и не быть, по этому если ничего небыло
                    # найдено не добавляем в общий список элементов "Хлебных крошек"
                    if len(Article.objects.filter(slug=url)) == 1:
                        name = Article.objects.filter(slug=url)[0].title
                    elif len(Tool.objects.filter(slug=url)) == 1:
                        name = Tool.objects.filter(slug=url)[0].name
                        
                    if name is not None:
                        result_list.append({
                            'name': name,
                            'url': curr_url + '/',
                            'level': indx + 1
                        })
            # Значит появился уровень в УРЛе, который ещё не поддерживается (то есть 4,5 и т.д.)
            # В этом случае возвращаем полностью переданный УРЛ и капитализируем его для имени
            case _:
                curr_url = '/'.join([curr_url, url])
                result_list.append({
                    'name': url.capitalize(),
                    'url': curr_url + '/',
                    'level': indx + 1
                })
    
    return result_list