import random

from django.test import TestCase
from django.core.files.base import ContentFile

from Post.models import Article, Tool, Note, Category
from Main.sitemaps import PostSitemap, PaginationSitemap

class SitemapTest(TestCase):
    ''' Проверка генерации карт сайта '''

    def setUp(self):
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()

        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()

        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()

        self.categories = Category.objects.all()

        self.articles = self.generate_article_queryset(0, 10)
        self.tools = self.generate_tool_queryset(0, 10)
        self.notes = self.generate_note_queryset(0, 10)

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

        return Article.objects.all()
    
    def generate_note_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            note = Note()
            note.save()
        
        return Note.objects.all()
    
    def test_PostSitemap(self):
        ''' Проверка карты сайта, которая генерируется для постов (инструменты и статьи) '''
        sitemap = PostSitemap()
        # Было сгенерированно 10 инструментов и 10 статей, значит в карте сайта должно
        # быть 20 элементов
        self.assertEqual(len(sitemap.items()), 20)
        # Проверяем есть ли там то что нам нужно
        self.assertIn(self.articles[random.randint(0, 9)], sitemap.items())
    
    def test_PaginationSitemap(self):
        ''' Проверка карты сайта, которая генерируется для страниц пагинации '''
        sitemap = PaginationSitemap()
        # Было сгенерированно 10 инструментов, 10 статей и 10 заметок.
        # На одной странице вмещается 4 элемента.
        # Соответственно имеем по три страницы на каждую модель
        self.assertEqual(len(sitemap.items()), 9)