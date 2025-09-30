import json
from uuid import uuid4

from django.core.files.base import ContentFile
from django.template.response import TemplateResponse
from django.template import loader
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404

from Main.utils import initDefaults, getAllWithTags
from Post.models import Tool, Tag, Note
from Main.models import Media
from .forms import LinkThiefForm
from .models import LinkThiefRecord


import link_thief.link_thief as LT

MAX_NOTES_ON_TOOL = 3

def save_all(links: list[LT.Url]) -> list[LT.Url]:
    return links

def save_internal(links: list[LT.Url]) -> list[LT.Url]:
    internal_links = []
    for link in links:
        if link.type == LT.LinkType.INTERNAL:
            internal_links.append(link)
    return internal_links

def save_external(links: list[LT.Url]) -> list[LT.Url]:
    external_links = []
    for link in links:
        if link.type == LT.LinkType.EXTERNAL:
            external_links.append(link)
    return external_links

def save_with_anchor(links: list[LT.Url]) -> list[LT.Url]:
    anchor_links = []
    for link in links:
        if len(link.anchor) > 0:
            anchor_links.append(link)
    return anchor_links

def save_without_anchor(links: list[LT.Url]) -> list[LT.Url]:
    anchor_links = []
    for link in links:
        if len(link.anchor) == 0:
            anchor_links.append(link)
    return anchor_links

def save_crawlable(links: list[LT.Url]) -> list[LT.Url]:
    crawlable_links = []
    for link in links:
        if link.crawlable:
            crawlable_links.append(link)
    return crawlable_links

def save_not_crawlable(links: list[LT.Url]) -> list[LT.Url]:
    crawlable_links = []
    for link in links:
        if not link.crawlable:
            crawlable_links.append(link)
    return crawlable_links

def tool_start(urls, ways_to_crawl, ways_to_save):
    links = []
    what_to_save = None
    messages = []

    match(ways_to_save):
        case 'all':
            what_to_save = save_all
        case 'internal':
            what_to_save = save_internal
        case 'external':
            what_to_save = save_external
        case 'anchor-only':
            what_to_save = save_with_anchor
        case 'anchor-without':
            what_to_save = save_without_anchor
        case 'crawlable':
            what_to_save = save_crawlable
        case 'crawlable-no':
            what_to_save = save_not_crawlable

    match(ways_to_crawl):
        case 'single-url':
            if LT._is_valid_url(urls[0]):
                links = LT.crawl_page(urls[0])
            else:
                messages.append(_("Некоректный адрес"))
        case 'list-url':
            if len(links) > 0 and len(links) < 100:
                links = LT.crawl_list(urls, LT.crawl_page)
            else:
                messages.append(_("Слишком много адресов"))
        case 'whole-website':
            if len(urls) > 1:
                messages.append(_("Пожалуйста, укажи только один адресс"))
            else:
                links = LT.crawl_website(urls[0])
    
    crawlable_links = 0
    anchor_links = 0
    for link in links:
        if link.crawlable:
            crawlable_links += 1
        if len(link.anchor) > 0:
            anchor_links += 1

    to_json_list = {
        'total-links': len(links),
        'total-internal-links': len(LT.filter_by_type(links, LT.LinkType.INTERNAL)),
        'total-external-links': len(LT.filter_by_type(links, LT.LinkType.EXTERNAL)),
        'total-crawlable-links': crawlable_links,
        'total-not-crawlable-links': len(links) - crawlable_links,
        'total-anchor-links': anchor_links,
        'total-not-anchor-links': len(links) - anchor_links,
        'links': []
    }
    for link in what_to_save(links):
        to_json_list['links'].append({
            'href': link.href,
            'anchor': link.anchor,
            'type': link.type.value,
            'crawlable': link.crawlable
        })
    
    new_file = ContentFile(json.dumps(to_json_list), name=f"links-{uuid4()}.json")
    new_file_obj = LinkThiefRecord(file=new_file)
    new_file_obj.save()
    
            
    return to_json_list, new_file_obj.get_path(), messages 

def tool_main(request):
    context = initDefaults(request)

    if request.method == "GET":
        form = LinkThiefForm()
        context.update({'link_thief_form': form})
        return TemplateResponse(request, 'LinkThief/links-scraper-main.html', context=context)
    elif request.method == "POST":
        form = LinkThiefForm(request.POST)
        if form.is_valid():
            urls_str = form.cleaned_data['urls']
            urls = urls_str.split(' ')
            ways_to_crawl = form.cleaned_data['ways_to_crawl']
            ways_to_save = form.cleaned_data['ways_to_save']
            is_table_on_page = form.cleaned_data['show_table_on_page']
            links, file_path, messages = tool_start(urls, ways_to_crawl, ways_to_save)
            messages.append(_('✔ Вы успешно спарсили ссылки'))
            context.update({'messages': messages,
                            'links': links,
                            'file_path': file_path,
                            'is_table_on_page': is_table_on_page})
        else:
            context.update({'messages': [_('✗ Возникла ошибка при отправке формы')]})
        
        context.update({'link_thief_form': form})
        return TemplateResponse(request, 'LinkThief/link-thief-form-result.html', context=context)
