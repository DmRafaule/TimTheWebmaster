from django.test import RequestFactory, LiveServerTestCase
from django.core.files.base import ContentFile

from Post.models import Category, Tool, Article, Note
from PagiScroll.middleware import PostFilterMiddleware
from PagiScroll.views import PostListView


class MiddlewareTest(LiveServerTestCase):
    ''' Проверка программной прослойки для фильтров инструментов '''

    def setUp(self):
        # Создаём необходимые категории
        self.categories = []
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        self.categories.append(article_cat)
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        self.categories.append(tool_cat)
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
        self.categories.append(note_cat)
        # Генерируем посты различных типов
        self.generate_article_queryset(0,10)
        self.generate_tool_queryset(0,10)
        self.generate_note_queryset(0,10)

    def generate_article_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор статей в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            file = ContentFile('TEXT', name=f"index-{i}.html")
            article = Article(slug=f"article-{i}", template=file)
            article.save()

        return Article.objects.all()
    
    def generate_tool_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом к-ве
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            tool = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
            tool.save()

        return Tool.objects.all()
    
    def generate_note_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            note = Note()
            note.save()
        
        return Note.objects.all()

    def test_middleware_on_customized_tool(self):
        ''' Тест мидлвари для страниц пагинации Article, Tool, Note '''
        # Имитирую работу программной прослойки, для проверки результатов в возвращаемом контексте
        models = (Article, Tool, Note)
        for cat, mod in zip(self.categories, models):
            # Конструируем запрос
            request = RequestFactory().get(f"{self.live_server_url}{cat.get_absolute_url()}")
            # Конструируем функцию представления для определённой модели + категории
            view_func = PostListView.as_view(model=mod, post_preview_template='Post/basic--post_preview-article.html', category=cat.slug)
            # Конструируем мидлвари
            middleware = PostFilterMiddleware(view_func(request))
            # Имитируем вызов функции обработчика шаблонных запросов
            middleware.process_template_response(request, middleware.get_response)
            # Проверяем контекстную переменную
            data = middleware.get_response.context_data
            self.assertTrue(data.get('isPostFilterMiddlewareConnected'))