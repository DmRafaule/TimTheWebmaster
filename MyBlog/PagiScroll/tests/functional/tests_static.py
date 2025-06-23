import os
import unittest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.template import loader
from django.test.testcases import TestCase
from django.utils import translation
from django.core.files.base import ContentFile

from MyBlog.settings import STATIC_URL, LANGUAGES
from Post.models import Article, Tool, Note, Category

class StaticTests(StaticLiveServerTestCase):
    ''' Проверка на доступность статических файлов, и правильность отрисовки для пользователя соответственно '''

    def setUp(self):
        # Настраиваем браузер 
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
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
    
    def tearDown(self):
        self.browser.quit()

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
    
    def get_static_file_sources(self, css_selector, attr_to_get):
        ''' Занимается тем, что генерирует списки всех медиа путей:
         
         1) которые должны быть загружены 
         2) которые были успешно загружены
         3) которые не удалось загрузить
         '''
        statics = self.browser.find_elements(By.CSS_SELECTOR, css_selector)
        statics_must_be_loaded = []
        statics_failed_to_be_loaded = []
        statics_successfully_loaded = []
        for static in statics:
            static_src = static.get_attribute(attr_to_get)
            # Если у статического элемента есть необходимое поле
            if static_src:
                # Если статический УРЛ в самом поле присутствует
                if STATIC_URL in static_src:
                    statics_must_be_loaded.append(static_src)
                    if finders.find(static_src.replace(f"{self.live_server_url}",'').replace(f"{STATIC_URL}",'')) is not None:
                        statics_successfully_loaded.append(static_src)
                    else:
                        statics_failed_to_be_loaded.append(static_src)

        return statics_must_be_loaded, statics_successfully_loaded, statics_failed_to_be_loaded

    def check_static_files(self):
        ''' Проверка всех возможных статических файлов '''
        # Все скрипты загрузились и доступны
        scripts_must_be_loaded, scripts_successfully_loaded, scripts_failed_to_be_loaded = self.get_static_file_sources('body>script', 'src')
        self.assertEqual(len(scripts_must_be_loaded), len(scripts_successfully_loaded))
        self.assertEqual(len(scripts_failed_to_be_loaded), 0)
        # Все стили загрузились и доступны
        styles_must_be_loaded, styles_successfully_loaded, styles_failed_to_be_loaded = self.get_static_file_sources('head>link[rel=stylesheet]', 'href')
        self.assertEqual(len(styles_must_be_loaded), len(styles_successfully_loaded))
        self.assertEqual(len(styles_failed_to_be_loaded), 0)
        # Все изображения загрузились и доступны
        images_must_be_loaded, images_successfully_loaded, images_failed_to_be_loaded = self.get_static_file_sources('img[src]', 'src')
        self.assertEqual(len(images_must_be_loaded), len(images_successfully_loaded))
        self.assertEqual(len(images_failed_to_be_loaded), 0)

    def test_static_files_on_pagination_pages(self):
        ''' Получает статические файлы со страниц пагинации '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                self.browser.get(f'{self.live_server_url}/{lang[0]}/{cat.slug}/')
                self.check_static_files()