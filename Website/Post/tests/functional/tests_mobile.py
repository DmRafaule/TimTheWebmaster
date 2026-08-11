import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from django.template import loader
from django.core.files.base import ContentFile
from django.test.testcases import TestCase

from Website.settings import LANGUAGES
from Post.models import Article, Tool, Category

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
    
    def tearDown(self):
        self.browser.quit()
    
    def generate_article(self, indx, content: str, styles: str, scripts: str):
        ''' Генерирует статью из шаблона по умолчанию с кастомным контекстом'''
        context = {
            "content": content,
            "styles": styles,
            "scripts": scripts,
        }
        # Предварительно нужно будет отрендерить шаблон и превратить его в строку
        template_file_not_rendered = loader.get_template(os.path.join('Post','article_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
        # Сохраняем статью
        article = Article(slug=f"article-{indx}", template=file)
        article.save()
        return article
    
    def generate_tool_default(self, indx):
        ''' Генерирует инструмент по умолчанию '''
        tool = Tool(slug=f"tool-{indx}", name_ru="", name_en="", description_ru="", description_en="")
        tool.save()
        return tool
    
    def generate_tool_custom_template(self, indx, content: str, styles: str, scripts: str):
        ''' Генерирует инструмент из шаблона по умолчанию с кастомным контекстом'''
        context = {
            "content": content,
            "styles": styles,
            "scripts": scripts,
        }
        # Предварительно нужно будет отрендерить шаблон и превратить его в строку
        template_file_not_rendered = loader.get_template(os.path.join('Post','tool_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        # Я не знаю по какой причине, но Django просто не может декодировать русские буквы
        # По этому просто удаляю их
        template_file_rendered = template_file_rendered.replace('Описание', '')
        # Сохраняем инструмент
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
        tool = Tool(slug=f"tool-{indx}", template=file,  name_ru=f"Инструмент {indx}", name_en=f"Tool {indx}", description_ru=f"Описание {indx}", description_en=f" Descript {indx}")
        tool.save()
        return tool
    
    def test_visit_pages_mobile_friendly(self):
        ''' Проверка на гибкость (mobile friendly) интерфейса '''
        self.generate_article(1, '', '', '')
        self.generate_tool_custom_template(1, '', '', '')
        self.generate_tool_default(2)
        for lang in LANGUAGES:
            pages = [
                f'http://localhost:8000/{lang[0]}/articles/article-1/'
                f'http://localhost:8000/{lang[0]}/tools/tool-1/'
                f'http://localhost:8000/{lang[0]}/tools/tool-2/'
            ]
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