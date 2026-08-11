import os
import unittest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from django.contrib.staticfiles import finders
from django.template import loader
from django.test.testcases import TestCase
from django.utils import translation
from django.core.files.base import ContentFile

from Website.settings import STATIC_URL, MEDIA_URL, BASE_DIR
from Post.models import Article, Tool, Category

class StaticTests(TestCase):
    ''' Проверка на доступность статических файлов, и правильность отрисовки для пользователя соответственно '''

    def setUp(self):
        # Настраиваем браузер 
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        # Создаём соответствующую категорию
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
        template_file_not_rendered = loader.get_template(os.path.join('Post','article_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
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
        template_file_not_rendered = loader.get_template(os.path.join('Post','tool_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        # Я не знаю по какой причине, но Django просто не может декодировать русские буквы
        template_file_rendered = template_file_rendered.replace('Описание', '')
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
        tool = Tool(slug=f"tool-{indx}", template=file,  name_ru=f"Инструмент {indx}", name_en=f"Tool {indx}", description_ru=f"Описание {indx}", description_en=f" Descript {indx}")
        tool.save()
        return tool
    
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
                    if finders.find(static_src.replace(f"http://localhost:8000",'').replace(f"{STATIC_URL}",'')) is not None:
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

    def test_static_files_on_tools_page(self):
        ''' Получает статические файлы с страниц инструментов '''
        # Получаю статику с инструментов для которых предоставлен собственный шаблон
        tool1 = self.generate_tool_custom_template(1, "", "", "")
        self.browser.get(f'http://localhost:8000{tool1.get_absolute_url().replace('/ru/', '/en/')}')
        self.check_static_files()
        # Получаю статику с инструментов для которых не предоставлен собственный шаблон
        tool2 = self.generate_tool_default(2)
        self.browser.get(f'http://localhost:8000{tool2.get_absolute_url().replace('/ru/', '/en/')}')
        self.check_static_files()

    def test_static_files_on_articles_page(self):
        ''' Получает статические файлы со страниц статей '''
        article = self.generate_article(1, "", "", "")
        self.browser.get(f'http://localhost:8000{article.get_absolute_url().replace('/ru/', '/en/')}')
        self.check_static_files()