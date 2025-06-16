from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

import unittest

class NewVisitorTest(unittest.TestCase):
    ''' Проверяем поведение нового пользователя на домашней странице '''    
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


if __name__ == "__main__":
    unittest.main(warnings='ignore')
