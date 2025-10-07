from bs4 import BeautifulSoup

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse

import Post.models as Post_M
import Main.models as Main_M
import Main.utils as U


def article(request, post_slug):
    ''' Представление для отображения отдельных записей модели Article '''
    # Инициализируем контекстные переменные по умолчанию
    context = U.initDefaults(request)
    # Получаем соответствующую статью
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    context.update({'post': post})
    # Получаем медиа файлы относящиеся к этой статье
    downloadables = post.media.filter_by_lang().filter(type=Main_M.Media.RAW_FILE).order_by('timeCreated')
    images = post.media.filter_by_lang().filter(type=Main_M.Media.IMAGE).order_by('timeCreated')
    videos = post.media.filter_by_lang().filter(type=Main_M.Media.VIDEO).order_by('timeCreated')
    pdfs = post.media.filter_by_lang().filter(type=Main_M.Media.PDF).order_by('timeCreated')
    audios = post.media.filter_by_lang().filter(type=Main_M.Media.AUDIO).order_by('timeCreated')
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    context.update({'videos': videos})
    context.update({'pdfs': pdfs})
    context.update({'audios': audios})
    ## Определяем сколько времени необходимо для прочтения
    with post.template.open('r') as file:
        soup = BeautifulSoup(file.read(), features="lxml")
        text = soup.get_text()
        words_in_text = len(text.split())
        time_to_read = round(words_in_text/240)
    context.update({'time_to_read': time_to_read})
    # Получаем предыдущую статью
    previous_id=Post_M.Article.objects.filter(
         id__lt=post.id,
     ).order_by("-id").values_list("id")[:1],
    if len(previous_id[0]) > 0:
        id = previous_id[0][0][0]
        prev_post = Post_M.Article.objects.get(id=id)
        context.update({'prev_post': prev_post})
    # Получаем следующую статью
    next_id=Post_M.Article.objects.filter(
         id__gt=post.id,
    ).order_by("id").values_list("id")[:1]
    if len(next_id) > 0:
        id = next_id[0][0]
        next_post = Post_M.Article.objects.get(id=id)
        context.update({'next_post': next_post})

    # Возвращаем TemplateRespose, чтобы моим мидлвари было легче взаимодействовать и модифицировать шаблон
    return TemplateResponse(request, post.template.path, context)

def tool(request, post_slug):
    ''' Представление для отображения отдельных записей модели Tool '''
    post = get_object_or_404(Post_M.Tool, slug=post_slug)
    context = U.initDefaults(request)
    if post.template:
        return TemplateResponse(request, post.template.path, context=context)
    else:
        return TemplateResponse(request, post.default_template, context=context)