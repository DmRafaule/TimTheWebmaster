import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from django.template import loader
from django.core.files.base import ContentFile
from django.test.testcases import TestCase

from MyBlog.settings import LANGUAGES
from Post.models import Article, Tool, Note, Category

class MobileFriendlyTest(TestCase):
    ''' Проверяем дружелюбность мобильного интерфейса '''    

    def setUp(self):
        ''' Настраиваем браузер '''
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
        # Создаём необходимую категорию
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        # Создаём необходимую категорию
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        # Создаём необходимую категорию
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
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

    def test_visit_pages_mobile_friendly(self):
        ''' Проверка на гибкость (mobile friendly) интерфейса '''
        for lang in LANGUAGES:
            pages = []
            for cat in Category.objects.all():
                pages.append(f'http://localhost:8000/{lang[0]}/{cat.slug}/')

            for page in pages:
                self.browser.get(page)
                # Разрешение экранов, которые я бы хотел поддерживать
                sizes = [1600, 1200, 992, 768, 480, 300]
                for win_size in sizes:
                    self.browser.set_window_size(win_size, 800)
                    win_width = self.browser.get_window_rect()['width']
                    time.sleep(1)
                    body_width = self.browser.find_element(By.TAG_NAME, 'body').size['width']
                    self.assertAlmostEqual(win_width, body_width, delta=20, msg=f"In page: {page} | In size: {win_size}")