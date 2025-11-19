from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.template.response import TemplateResponse 
from django.views.decorators.http import require_POST

import Main.utils as U
from Main.models import Website
from Post.models import Tool, Article, Tag, Note
from Engagement.models import Comment


def about(request):
    ''' Представление для страницы об авторе/сайте '''
    context = U.initDefaults(request)
    # Вычисляем сколько мне лет
    context.update({'me_years': U.get_how_old_human_in_years('16/07/2000', "%d/%m/%Y")})
    # Специальный тег об моём игровом прошлом
    more_about_me_tags = Tag.objects.filter(slug_en='gamedev')
    if len(more_about_me_tags) > 0:
        more_about_me_tag = more_about_me_tags[0].slug
    else:
        more_about_me_tag = None
    context.update({'more_about_me_tag': more_about_me_tag})
    return render(request, 'Main/about.html', context=context)

def home(request):
    # Из базы данных нужно взять текущие настройки сайта
    # Пытаемся получить текущую конфигурацию сайта по возможности
    try:
        website_conf = Website.objects.get(is_current=True)
        cap_notes = website_conf.max_displayed_notes_on_home
    # Если не получилось (такие настройки ещё не были добавленны) отправляем в качестве настроек
    # пустые значения, чтобы страница не вернула 500 код ошибки (ошибка сервера)
    except:
        cap_notes = 3

    # Инициализируем общие для всего сайта контекстные переменные
    # TODO: Может есть другой способ задать общие для всех представлений контекстные переменные?
    # UPD: Возможно стоит написать соответствующую мидлвари?
    context = U.initDefaults(request)
    # Так как теги на домашней странице не поддерживаются, пока, добавляем конт. переменную 
    # Чтобы они неотображались при рендеренге превью постов
    context.update({'displayTags': False})
    # Получаем тег для внутренних инструментов, или создаём его если его нет 
    internal_tool_tag, is_created = Tag.objects.get_or_create(slug_en='internal-tool')
    if is_created:
        internal_tool_tag.slug_ru = 'vnutrenij-instrument'
        internal_tool_tag.name_ru = 'Внутренний инструмент'
        internal_tool_tag.name_en = 'Internal tool'
        internal_tool_tag.save()
    context.update({'internal_tool_tag': internal_tool_tag.slug})

    # Получаем и сохраняем внутренние инструменты, которые выбираются в общей конфигурации сайта
    context.update({'popular_tools': U.get_posts_by_popularity(3, Tool)})
    context.update({'recent_tools': U.get_latest_post(3, Tool.objects.all())})
    # Получаем и сохраняем комментарии про статьи на текущем языке 
    comments_in_tools = Comment.objects.filter(url__startswith=f"/{get_language()}/tools/").order_by('-time_published')[:10]
    context.update({'comments_in_tools': comments_in_tools})

    # Получаем самые последние статьи
    context.update({'popular_articles': U.get_posts_by_popularity(3, Article)})
    context.update({'recent_articles': U.get_latest_post(3, Article.objects.all())})
    # Получаем и сохраняем комментарии про статьи на текущем языке 
    comments_in_articles = Comment.objects.filter(url__startswith=f"/{get_language()}/articles/").order_by('-time_published')[:10]
    context.update({'comments_in_articles': comments_in_articles})

    # Получаем самые последние заметки
    context.update({'recent_notes': U.get_latest_post(cap_notes, Note.objects.all())})
    
    return TemplateResponse(request, 'Main/home.html', context=context)

def about_website(request):
    import django
    import sys
    # Из базы данных нужно взять текущие настройки сайта
    # Пытаемся получить текущую конфигурацию сайта по возможности
    try:
        website_conf = Website.objects.get(is_current=True)
    # Если не получилось (такие настройки ещё не были добавленны) отправляем в качестве настроек
    # пустые значения, чтобы страница не вернула 500 код ошибки (ошибка сервера)
    except:
        cap_notes = 3
    context = U.initDefaults(request)
    context.update({'website_years': U.get_how_old_human_in_years('09/10/2023', "%d/%m/%Y")})
    context.update({'django_version': django.get_version()})
    context.update({'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"})
    return render(request, 'Main/about-website.html', context=context)


def bad_request(request, exception):
    ''' Специальный хендлер для 400 ответов '''
    context = U.initDefaults(request)
    return render(request, 'Main/400.html', context=context, status=400)

def forbidden(request, exception):
    ''' Специальный хендлер для 403 ответов '''
    context = U.initDefaults(request)
    return render(request, 'Main/403.html', context=context, status=403)

def page_not_found(request, exception):
    ''' Специальный хендлер для 404 ответов '''
    context = U.initDefaults(request)
    return render(request, 'Main/404.html', context=context, status=404)

def server_error(request):
    ''' Специальный хендлер для 500 ответов '''
    context = U.initDefaults(request)
    return render(request, 'Main/500.html', context=context, status=500)