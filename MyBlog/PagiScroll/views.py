import json
from django.http import Http404, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse
from django.views.generic.list import ListView
from django.contrib.syndication.views import Feed
from django.utils.translation import get_language
from django.urls import reverse

import Post.models as Post_M
import Main.models as Main_M
import Main.utils as U
import PagiScroll.utils as PagiScroll_utils


class PostListView(ListView):
    ''' Класс представлени списков постов и заметок'''

    allow_empty=True
    context_object_name = "posts"
    # Текущая конфигурация сайта
    website_conf = None
    # Для сортировки по времени создания
    is_recent = "true"
    # Для сортировки по алфавиту
    is_alphabetic = "ignored"
    # Используемая категория для отображения пагинации
    category = None
    # Сколько страниц для пагинации использовать
    pages = 0
    # Стартовая страница
    page = 1
    # Теги используемые для фильтрации
    tags = None
    # Используемые теги, их имена
    tags_names = None
    # Превью вверху для страницы пагинации
    image = None
    # Контекстная переменная для хранения переменных используемых в отрисовке шаблонов
    context = {}
    # Какой шаблон используется для отрисовки блоко постов
    post_preview_template = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Update context data
        context['category'] = Post_M.Category.objects.get(slug=self.category)
        context['displayTags'] = True
        context['num_pages'] = self.pages
        context['current_page'] = self.page
        context['page'] = self.page + 1
        context['is_recent'] = self.is_recent
        context['current_tag'] = self.tags
        context['current_tag_names'] = self.tags_names
        context['tags_json'] = json.dumps(self.tags)
        context['post_list_preview'] = self.image
        context['post_preview_template'] = self.post_preview_template

        return context

    def get(self, request):
        error_response = self.fetch(request)
        if error_response is None:
            return TemplateResponse(request, 'PagiScroll/base_post_list.html', self.context)
        else:
            return error_response

    def post(self, request):
        error_response = self.fetch(request)
        if  error_response is None:
            return TemplateResponse(request, self.post_preview_template, self.context)
        else:
            return error_response
    
    def fetch(self, request):
        # Пытаемся получить текущую конфигурацию сайта
        try:
            self.website_conf = Main_M.Website.objects.get(is_current=True)
            posts_per_page = self.website_conf.paginator_per_page_posts
        except:
            posts_per_page = 4
        # Допустимы запросы GET, POST
        if request.method == "GET":
            self.page = int(request.GET.get('page', 1))
        elif request.method == "POST":
            self.page = int(request.POST.get('page', 1))
            self.is_recent = request.POST.get('is_recent', 'true')
            self.is_alphabetic = request.POST.get('is_alphabetic', 'ignored')
        else:
            return HttpResponseBadRequest()

        # Фильтруем по опубликованности
        self.object_list =  self.model.objects.filter(isPublished=True)
        # Фильтруем по порядку создания
        self.object_list = PagiScroll_utils.in_order(self.object_list, self.is_recent)
        # Фильтруем по алфавиту
        self.object_list = PagiScroll_utils.in_alphabetic(self.object_list, self.is_alphabetic)

        if request.method == "POST":
            # Фильтруем посты относительно текущего времени
            relative_this = request.POST.get('relative_this')
            match (relative_this):
                case 'this_day':
                    self.object_list = PagiScroll_utils.get_this_day_posts(self.object_list)
                case 'this_week':
                    self.object_list = PagiScroll_utils.get_this_week_posts(self.object_list)
                case 'this_month':
                    self.object_list = PagiScroll_utils.get_this_month_posts(self.object_list)
                case 'this_year':
                    self.object_list = PagiScroll_utils.get_this_year_posts(self.object_list)
            # Фильтруем посты по выбраным временым промежуткам
            week_days = json.loads(request.POST['week_day'])
            self.object_list = PagiScroll_utils.get_posts_by_week_days(week_days, self.object_list)
            month_days = json.loads(request.POST['month_day'])
            self.object_list = PagiScroll_utils.get_posts_by_month_days(month_days, self.object_list)
            months = json.loads(request.POST['month'])
            self.object_list = PagiScroll_utils.get_posts_by_months(months, self.object_list)
            years = json.loads(request.POST['year'])
            self.object_list = PagiScroll_utils.get_posts_by_years(years, self.object_list)
            letters = json.loads(request.POST['letter'])
            self.object_list = PagiScroll_utils.get_posts_by_letters(letters, self.object_list)
            platforms_id = json.loads(request.POST['platform'])
            platforms = Post_M.Platform.objects.filter(id__in=platforms_id)
            self.object_list = PagiScroll_utils.get_posts_by_platforms(platforms, self.object_list)
            # Если объекты не были найдены, возвращаем соответствующий шаблон
            if len(self.object_list) == 0:
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Ничего не нашёл.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
        # Получаем теги из запроса
        self.tags_names = []
        if request.method == "GET":
            self.tags = request.GET.getlist('tag', [])
        elif request.method == "POST":
            self.tags = json.loads(request.POST['tag'])
        else: 
            return HttpResponseBadRequest()
        # Фильтруем посты по тегам
        if len(self.tags) > 0:
            tag_obj = Post_M.Tag.objects.filter(Q(name_ru__in=self.tags) | Q(name_en__in=self.tags) | Q(slug_ru__in=self.tags)  | Q(slug_en__in=self.tags))
            if (len(self.tags) != len(tag_obj)) or tag_obj is None:
                if request.method == "GET":
                    raise Http404(_("Такого тега не существует, или он введён с ошибкой"))
                elif request.method == "POST":
                    return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Такого тега не существует, или он введён с ошибкой'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
                else:
                    return HttpResponseBadRequest()
            # Сохраняем для рендеринга в шаблоне
            for key, tag in enumerate(tag_obj):
                self.tags[key] = tag.slug
            for key, tag in enumerate(tag_obj):
                self.tags_names.append(tag.name)
            # Получаем все посты в которых присутствуют все требуемые теги 
            self.object_list = U.getAllWithTags(self.object_list, tag_obj)

        if len(self.object_list) == 0:
            if request.method == "POST":
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Ничего не нашёл.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
            elif request.method == "GET":
                raise Http404()
            else:
                return HttpResponseBadRequest()
        # Создаём пагинатор
        self.pages = PagiScroll_utils.calculate_pages(len(self.object_list), posts_per_page)
        if self.page > self.pages :
            if request.method == "GET":
                raise Http404(_("Так много страниц у меня нет."))
            elif request.method == "POST":
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Так много страниц у меня нет.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
            else:
                return HttpResponseBadRequest()
        # Пагинируемся)
        self.object_list = self.object_list[(self.page-1) * posts_per_page : self.page * posts_per_page]
        self.context = self.get_context_data()
        self.context.update(U.initDefaults(request))

        return None

class PostFeed(Feed):
    ''' Генератор RSS фидов '''

    def __init__(self, model, category_slug):
        super().__init__()
        self.model = model
        try:
            self.category = Post_M.Category.objects.get(slug=category_slug)
        except:
            self.category = None
    
    def title(self):
        return self.category.name

    def description(self):
        return self.category.description

    def link(self):
        return f"/{get_language()}/{self.category.slug}-rss/"

    def items(self):
        return self.model.objects.filter(isPublished=True).order_by("-timeCreated")[:50]

    def item_title(self, item):
        if hasattr(item, 'title'):
            return item.title
        elif hasattr(item, 'name'):
            return item.name

    def item_description(self, item):
        return item.description
    
    def item_pubdate(self, item):
        return item.timeCreated

    def item_link(self, item):
        if hasattr(item, 'get_absolute_url'):
            return item.get_absolute_url()
        else:
            return reverse(f'{self.category.slug}-list')