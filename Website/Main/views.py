from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.template.response import TemplateResponse 

import Main.utils as U
from .models import Website
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

def get_latest_post_by_tag(min, cont, Model):
    ''' Получаем последние посты по контейнерам тегов '''
    res = []
    for tag in cont:
        objs = U.get_posts_by_tag(tag.name, Model)
        latest_objs = U.get_latest_post(min, objs)
        if len(latest_objs) > 0:
            res.append({
                'tag': tag.slug,
                'title': tag.name,
                'objs': latest_objs,
            })
    return res

def home(request):
    # Из базы данных нужно взять текущие настройки сайта
    # Пытаемся получить текущую конфигурацию сайта по возможности
    try:
        website_conf = Website.objects.get(is_current=True)
        cap_choosen_tools = website_conf.max_displayed_inner_tools_on_home
        choosen_tools = website_conf.choosen_tools.all()[:cap_choosen_tools]
        cap_notes = website_conf.max_displayed_notes_on_home
        choosen_tools_by_tags = website_conf.my_resources_choosen_tags_on_home.all()
        min_choosen_tools_by_tags = website_conf.min_displayed_my_resources
        choosen_articles_by_tag = website_conf.other_articles_choosen_tags_on_home.all()
        min_choosen_articles_by_tag = website_conf.min_displayed_other_articles
        tools_post_preview = website_conf.tools_post_preview
        articles_post_preview = website_conf.articles_post_preview
        notes_post_preview = website_conf.notes_post_preview
    # Если не получилось (такие настройки ещё не были добавленны) отправляем в качестве настроек
    # пустые значения, чтобы страница не вернула 500 код ошибки (ошибка сервера)
    except:
        choosen_tools = []
        cap_notes = 3
        choosen_tools_by_tags = []
        min_choosen_tools_by_tags = 0
        choosen_articles_by_tag = []
        min_choosen_articles_by_tag = 0
        tools_post_preview = None
        articles_post_preview = None
        notes_post_preview = None

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
    context.update({'internal_tools_posts': choosen_tools})
    context.update({'internal_tools_preview': tools_post_preview})
    context.update({'internal_tools_length': len(choosen_tools)})
    # Получаем самые последние статьи
    context.update({'most_popular_article_posts': U.get_latest_post(3, Article.objects.all())})
    context.update({'articles_preview': articles_post_preview})
    # Получаем самые последние заметки
    context.update({'latest_notes_posts': U.get_latest_post(cap_notes, Note.objects.all())})
    context.update({'notes_preview': notes_post_preview})
    # Получаем все последние Инструменты по выбранным тегам с минимальным порогом для отображения 
    context.update({'my_resources': get_latest_post_by_tag(min_choosen_tools_by_tags, choosen_tools_by_tags, Tool)})
    # Получаем все последние Статьи по выбранным тегам с минимальным порогом для отображения 
    context.update({'other_articles': get_latest_post_by_tag(min_choosen_articles_by_tag, choosen_articles_by_tag, Article)})
    # Получаем и сохраняем последние комментарии
    comments_all = Comment.objects.filter(url__startswith=f"/{get_language()}/").order_by('-time_published')[:10]
    context.update({'comments': comments_all})
    
    return TemplateResponse(request, 'Main/home.html', context=context)

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