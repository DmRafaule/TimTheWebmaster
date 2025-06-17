from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import unittest
from django.contrib.staticfiles import finders
from MyBlog.settings import STATIC_URL, MEDIA_URL

class StaticTests(unittest.TestCase):
    ''' Проверка на доступность статических файлов '''
    def setUp(self):
        ''' Настраиваем браузер '''
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
    
    def tearDown(self):
        ''' Закрываем браузер '''
        self.browser.quit()
    
    def get_static_file_sources(self, css_selector, attr_to_get):
        statics = self.browser.find_elements(By.CSS_SELECTOR, css_selector)
        statics_must_be_loaded = []
        statics_failed_to_be_loaded = []
        statics_successfully_loaded = []
        tmp = []
        for static in statics:
            static_src = static.get_attribute(attr_to_get)
            if static_src:
                if STATIC_URL in static_src:
                    statics_must_be_loaded.append(static_src)
                    if finders.find(static_src.replace(f"http://localhost:8000",'').replace(f"{STATIC_URL}",'')) is not None:
                        statics_successfully_loaded.append(static_src)
                    else:
                        statics_failed_to_be_loaded.append(static_src)

        return statics_must_be_loaded, statics_successfully_loaded, statics_failed_to_be_loaded

    def check_static_files(self):
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

    def test_static_files_on_home_page(self):
        self.browser.get('http://localhost:8000')
        self.check_static_files()

    def test_static_files_on_contacts_page(self):
        self.browser.get('http://localhost:8000/en/contacts/')
        self.check_static_files()

    def test_static_files_on_about_page(self):
        self.browser.get('http://localhost:8000/en/about/')
        self.check_static_files()