import os
import time
import lxml

from django.test import RequestFactory, LiveServerTestCase
from django.core.files.base import ContentFile
from django.template import loader
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from bs4 import BeautifulSoup
import lxml.etree

from Post.models import Category, Article, Tool, Tag, Termin, Question, Note
from Post.views import article, tool
from Main.models import Media
from MyBlog.settings import LANGUAGES

class PagiScrollTest(StaticLiveServerTestCase):
    ''' Тесты для страниц пагинации'''
    def setUp(self):
        # Создаём две необходимые категории для хранения статей и инструментов
        # Создаём соответствующую категорию
        self.article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        self.article_cat.save()
        # Создаём необходимую категорию
        self.tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        self.tool_cat.save()
        # Создаём необходимую категорию
        self.note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        self.note_cat.save()
        self.generate_article_queryset(0,20)
        self.generate_tool_queryset(0,20)
        self.generate_note_queryset(0,20)
        # Генерируем тег и присваиваем его только 3-м статьям
        tag = Tag(slug_en=f"tag1", slug_ru=f"teg1", name_en=f"First tag", name_ru=f"Первый тег")
        tag.save()
        first_with_tag = Article.objects.all()[0]
        first_with_tag.tags.add(tag)
        first_with_tag.save()
        second_with_tag = Article.objects.all()[1]
        second_with_tag.tags.add(tag)
        second_with_tag.save()
        third_with_tag = Article.objects.all()[2]
        third_with_tag.tags.add(tag)
        third_with_tag.save()
        # Генерируем тег и присваиваем его только 3-м инструментам 
        first_with_tag = Tool.objects.all()[0]
        first_with_tag.tags.add(tag)
        first_with_tag.save()
        second_with_tag = Tool.objects.all()[1]
        second_with_tag.tags.add(tag)
        second_with_tag.save()
        third_with_tag = Tool.objects.all()[2]
        third_with_tag.tags.add(tag)
        third_with_tag.save()
        # Генерируем тег и присваиваем его только 3-м заметкам 
        first_with_tag = Note.objects.all()[0]
        first_with_tag.tags.add(tag)
        first_with_tag.save()
        second_with_tag = Note.objects.all()[1]
        second_with_tag.tags.add(tag)
        second_with_tag.save()
        third_with_tag = Note.objects.all()[2]
        third_with_tag.tags.add(tag)
        third_with_tag.save()
    
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

    def test_pagination_page_first_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для первой страницы пагинации '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                response = self.client.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/")
                self.assertTemplateUsed(response, 'PagiScroll/base_post_list.html')
                # Проверяем получил ли все посты за страницу
                html = response.content.decode('utf8')
                soup = BeautifulSoup(html, 'lxml')
                posts = soup.select('.post_preview')
                self.assertEqual(len(posts), 4)

    def test_pagination_page_second_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для последующей страницы пагинации '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                response = self.client.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/?page=2")
                self.assertTemplateUsed(response, 'PagiScroll/base_post_list.html')
                # Проверяем получил ли все посты за страницу
                html = response.content.decode('utf8')
                soup = BeautifulSoup(html, 'lxml')
                posts = soup.select('.post_preview')
                self.assertEqual(len(posts), 4)

    def test_pagination_page_tagged_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы пагинации с фильтрацией по тегу '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                response = self.client.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/?page=1&tag=tag1")
                self.assertTemplateUsed(response, 'PagiScroll/base_post_list.html')
                # Проверяем получил ли все посты за страницу
                html = response.content.decode('utf8')
                soup = BeautifulSoup(html, 'lxml')
                posts = soup.select('.post_preview')
                self.assertEqual(len(posts), 3)