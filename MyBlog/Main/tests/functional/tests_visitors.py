import unittest
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as EC

from MyBlog.settings import LANGUAGES

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
        ''' Проверка на возможность отправки формы пользователем '''
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
        ''' Проверка на минимально необходимые контакты '''
        # Посетитель заходит на страницу
        self.browser.get('http://localhost:8000/en/contacts/')
        # Смотрит варианты, как связаться с автором
        contacts = self.browser.find_elements(By.CSS_SELECTOR, 'ul.list_without_sign>div>li')
        self.assertGreaterEqual(len(contacts), 2)
    
    def test_visit_pages_mobile_friendly(self):
        ''' Проверка на гибкость (mobile friendly) интерфейса '''
        for lang in LANGUAGES:
            pages = [
                f'http://localhost:8000/{lang[0]}/'
                f'http://localhost:8000/{lang[0]}/about/'
                f'http://localhost:8000/{lang[0]}/contacts/'
                f'http://localhost:8000/{lang[0]}/some-not-existing-page/'
            ]
            for page in pages:
                self.browser.get(page)
                sizes = [1600, 1200, 992, 768, 480, 300]
                for win_size in sizes:
                    self.browser.set_window_size(win_size, 800)
                    win_width = self.browser.get_window_rect()['width']
                    time.sleep(1)
                    body_width = self.browser.find_element(By.TAG_NAME, 'body').size['width']
                    self.assertAlmostEqual(win_width, body_width, delta=20, msg=f"In page: {page} | In size: {win_size}")