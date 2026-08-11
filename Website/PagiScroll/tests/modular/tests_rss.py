import time

from django.test import TestCase
from django.utils.translation import get_language
from django.core.files.base import ContentFile

from Post.models import Article, Tool, Note, Category
from Website.settings import LANGUAGES
from PagiScroll.views import PostFeed


class RSSFeedTest(TestCase):
    ''' Тесты для проверки правильности генерации RSS-фидов '''

    def setUp(self):
        # Создаём категории
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        # Создаём категорию
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        # Создаём категорию
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
        # Генерируем rss фиды
        self.rss_generators = []
        self.rss_generators.append(PostFeed(Article, 'articles'))
        self.rss_generators.append(PostFeed(Tool, 'tools'))
        self.rss_generators.append(PostFeed(Note, 'notes'))
        # Генерируем посты различных типов
        self.generate_article_queryset(0,5)
        self.generate_tool_queryset(0,5)
        self.generate_note_queryset(0,5)

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
    
    def test_rss_feed(self):
        ''' Тест на правильность создания элементов фида '''
        for generator, category in zip(self.rss_generators, Category.objects.all()):
            self.assertEqual(generator.title(), category.name)
            self.assertEqual(generator.description(), category.description)
            self.assertEqual(generator.link(), f"/{get_language()}/{category.slug}-rss/")
            for indx, item in enumerate(generator.items()):
                self.assertIsNotNone(generator.item_title(item))
                self.assertIsNotNone(generator.item_description(item))
                self.assertIsNotNone(generator.item_pubdate(item))


