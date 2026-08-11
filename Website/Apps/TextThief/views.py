import json
from uuid import uuid4

import text_thief.text_thief as TH
import link_thief.link_thief as LT

from django.utils.translation import gettext as _
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.template.response import TemplateResponse

from Main.utils import initDefaults
from .forms import TextThiefForm
from .models import TextThiefRecord

def tool_start(urls, selector, ways_to_crawl, ways_to_save):
    text = ""
    messages = []

    match(ways_to_crawl):
        case 'single-url':
            if LT._is_valid_url(urls[0]):
                text = TH.get_page_text(urls[0], selector)
            else:
                messages.append(_("Некоректный адрес"))
        case 'list-url':
            if len(urls) > 0 and len(urls) < 100:
                text = TH.get_page_text_list(urls, selector)
            else:
                messages.append(_("Слишком много адресов"))
        case 'whole-website':
            if len(urls) > 1:
                messages.append(_("Пожалуйста, укажи только один адрес"))
            else:
                text = TH.get_page_text_website(urls[0], selector)
    
    result = {
        'length': {'data': len(text), 'name': _("Общая длина текста с пробелами")},
        'length-without-spaces': { 'data': len(text.replace(' ', '')), 'name': _("Общая длина текста без пробелов")},
        'words-length': { 'data': 0, 'name': _("Количество слов")},
        'unique-words-length': { 'data': 0, 'name': _("Количество уникальных слов")},
        'tags-length': { 'data': 0, 'name': _("Количество слов с частотностью")},
        'text': { 'data': "", 'name': _("Полученый текст")},
        'words': { 'data': [], 'name': _("Список всех слов")},
        'unique-words': { 'data': [], 'name': _("Список уникальных слов")},
        'tags': { 'data': [], 'name': _("Слова с частотностью")},
    }

    # Proccesed a text and save result in dict
    proccesed_text_obj = TH.procced_text(text)
    for option in ways_to_save:
        match option:
            case 'text':
                result['text']['data'] = text
            case 'words':
                result['words']['data'] = proccesed_text_obj.all_words
                result['words-length']['data'] = len(proccesed_text_obj.all_words)
            case 'unique_words':
                result['unique-words']['data'] = list(proccesed_text_obj.unique_words)
                result['unique-words-length']['data'] = len(proccesed_text_obj.unique_words)
            case 'tags':
                result['tags']['data'] = proccesed_text_obj.tags
                result['tags-length']['data'] = len(proccesed_text_obj.tags)
    
    new_file = ContentFile(json.dumps(result), name=f"text-{uuid4()}.json")
    new_file_obj = TextThiefRecord(file=new_file)
    new_file_obj.save()
    
            
    return result, new_file_obj.get_path(), messages 

def tool_main(request):
    context = initDefaults(request)

    if request.method == "GET":
        form = TextThiefForm()
        context.update({'text_thief_form': form})
        return TemplateResponse(request, 'TextThief/text-scraper-main.html', context=context)
    elif request.method == "POST":
        form = TextThiefForm(request.POST)
        if form.is_valid():
            urls_str = form.cleaned_data['urls']
            urls = urls_str.split(' ')
            selector = form.cleaned_data['selector']
            ways_to_crawl = form.cleaned_data['ways_to_crawl']
            ways_to_save = form.cleaned_data['ways_to_save']
            data, file_path, messages = tool_start(urls, selector, ways_to_crawl, ways_to_save)
            messages = []
            messages.append(_('✔ Вы успешно спарсили ссылки'))
            context.update({'messages': messages,
                            'data': data,
                            'file_path': file_path
            })
        else:
            context.update({'messages': [_('✗ Возникла ошибка при отправке формы')]})
        
        context.update({'text_thief_form': form})
        return TemplateResponse(request, 'TextThief/text-thief-form-result.html', context=context)

