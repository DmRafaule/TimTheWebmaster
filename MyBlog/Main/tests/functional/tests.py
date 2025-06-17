from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as EC

import unittest
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.staticfiles import finders
from MyBlog.settings import STATIC_URL, MEDIA_URL

class NewVisitorTest(unittest.TestCase):
    ''' Проверяем поведение нового пользователя '''    
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
    
    def test_visit_home_page_and_see_all_stuff(self):
        ''' Проверяем на доступность контента на домашней странице '''
        # Посетитель заходит на страницу
        self.browser.get('http://localhost:8000')
        # Смотрит на тайтл таба
        self.assertIn('Tim the Webmaster', self.browser.title)
        # Смотрит на то, что ему доступно на данной странице
        tabs = self.browser.find_elements(By.CLASS_NAME, 'tabs')
        self.assertEqual(len(tabs), 5)
        # Одновременно на странице должны быть видны только три таба
        active_body_tabs = self.browser.find_elements(By.CLASS_NAME, 'tab_element__active')
        self.assertEqual(len(active_body_tabs), 3)
        # Изначально на странице пользователь может увидеть только 3 кнопки табов
        active_buttons_tabs = self.browser.find_elements(By.CLASS_NAME, 'tab_active')
        self.assertEqual(len(active_buttons_tabs), 3)
    
    def test_visit_contacts_page_to_send_form(self):
        # Посетитель заходит на страницу
        self.browser.get('http://localhost:8000/en/contacts/')
        # Посетитель заполняет форму
        form = self.browser.find_element(By.TAG_NAME, 'form')
        username = form.find_element(By.ID, 'id_username')
        email = form.find_element(By.ID, 'id_email')
        message = form.find_element(By.ID, 'id_message')
        captcha = form.find_element(By.ID, 'id_captcha_1')
        send = form.find_element(By.ID, 'feedback')
        username.send_keys('selenium')
        email.send_keys('some@gmail.com')
        message.send_keys('This message was send by selenium')
        captcha.send_keys('KRKDS')
        # Посетитель отправляет заведомо неправильную форму
        send.click()
        # Получает соответствующий элемент с ошибкой
        invalid = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'form_error'))
        )
        # Вводит правильные данные
    
    def test_visit_contacts_page_to_see_contacts(self):
        # Посетитель заходит на страницу
        self.browser.get('http://localhost:8000/en/contacts/')
        # Смотрит варианты, как связаться с автором
        contacts = self.browser.find_elements(By.CSS_SELECTOR, 'ul.list_without_sign>div>li')
        self.assertGreaterEqual(len(contacts), 2)

class StaticTests(StaticLiveServerTestCase):
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
                if STATIC_URL in static_src or MEDIA_URL in static_src:
                    statics_must_be_loaded.append(static_src)
                    if finders.find(static_src.replace(self.live_server_url,'')) is not None:
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
        self.browser.get(self.live_server_url)
        self.check_static_files()

    def test_static_files_on_contacts_page(self):
        self.browser.get(f'{self.live_server_url}/en/contacts/')
        self.check_static_files()

    def test_static_files_on_about_page(self):
        self.browser.get(f'{self.live_server_url}/en/about/')
        self.check_static_files()