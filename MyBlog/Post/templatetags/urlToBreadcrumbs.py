from django import template
from Post.models import Category, Tag, Article, TD, QA, Tool
from django.utils.translation import gettext as _
from django.db.models import Q
from urllib.parse import urlsplit
from django.shortcuts import get_object_or_404

register = template.Library()

def remove_items(list, item): 
    # remove the item for all its occurrences 
    c = list.count(item) 
    for i in range(c): 
        list.remove(item) 
    return list 


@register.filter(name='urlToBreadcrumbs')
def urlToBreadcrumbs(url: str):
    url_dict = urlsplit(url)
    updated_url = f"{url_dict.path}/{url_dict.query}"
    urlList = updated_url.split('/')
    # Clean up after slplit function
    urlList = remove_items(urlList, '')
    result_list = []
    curr_url = ''
    for indx, url in enumerate(urlList):
        match indx + 1:
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
                    elif url == 'gallery':
                        name = _('Галерея')
                result_list.append({
                    'name': name,
                    'url': curr_url + '/',
                    'level': indx + 1
                })
            case 3:
                # Check if it is a pagination page
                if url.startswith('page='):
                    parse_res = url.split('&')
                    curr_url = '/'.join([curr_url, f'?{url}'])
                    args = {}
                    tag_counter = 0
                    for item in parse_res:
                        item_key_value = item.split('=')
                        if item_key_value[0] != 'tag':
                            args.update({item_key_value[0]: item_key_value[1]})
                        else:
                            args.update({item_key_value[0] + str(tag_counter): item_key_value[1]})
                            tag_counter += 1
                    name = _("Страница ") + args['page']
                    if tag_counter >= 1:
                        name += ', '
                        for i in range(tag_counter):
                            tag = get_object_or_404(Tag, Q(slug_en=args['tag' + str(i)]) | Q(slug_ru=args['tag' + str(i)]))
                            name += ','.join([tag.name, ' ' ])
                    result_list.append({
                        'name': name,
                        'url': curr_url,
                        'level': indx + 1
                    })
                else:
                    curr_url = '/'.join([curr_url, url])
                    name = None
                    if len(Article.objects.filter(slug=url)) == 1:
                        name = Article.objects.filter(slug=url)[0].title
                    elif len(QA.objects.filter(slug=url)) == 1:
                        name = QA.objects.filter(slug=url)[0].question
                    elif len(TD.objects.filter(slug=url)) == 1:
                        name = TD.objects.filter(slug=url)[0].termin
                    elif len(Tool.objects.filter(slug=url)) == 1:
                        name = Tool.objects.filter(slug=url)[0].name
                        
                    if name is not None:
                        result_list.append({
                            'name': name,
                            'url': curr_url + '/',
                            'level': indx + 1
                        })
            case _:
                curr_url = '/'.join([curr_url, url])
                result_list.append({
                    'name': url.capitalize(),
                    'url': curr_url + '/',
                    'level': indx + 1
                })
    return result_list