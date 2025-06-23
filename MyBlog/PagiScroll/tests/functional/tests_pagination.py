import time

from django.core.files.base import ContentFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions  as EC
from selenium.webdriver.support.ui import WebDriverWait

from Post.models import Article, Tool, Note, Category, Tag
from MyBlog.settings import LANGUAGES

class PaginationTests(StaticLiveServerTestCase):
    ''' Для тестирования функционала пагинатора/ленты прокрутки '''

    def setUp(self):
        # Настраиваем браузер
        firefox_opt = Options()
        firefox_opt.add_argument('--headless')
        firefox_opt.add_argument("--no-sandbox")
        firefox_opt.add_argument("--disable-dev-shm-usage")  
        self.browser = webdriver.Firefox(options=firefox_opt)
        # Создаём две необходимые категории для хранения статей и инструментов
        # Создаём соответствующую категорию
        self.article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        self.article_cat.categry_name = "Article"
        self.article_cat.save()
        # Создаём необходимую категорию
        self.tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        self.tool_cat.categry_name = "Tool"
        self.tool_cat.save()
        # Создаём необходимую категорию
        self.note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        self.note_cat.categry_name = "Note"
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
    
    def tearDown(self):
        self.browser.quit()
    
    def generate_article_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор статей в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            file = ContentFile('TEXT', name=f"index-{i}.html")
            article = Article(slug=f"article-{i}", template=file, title_ru=f"Article {i}", title_en=f"Article {i}")
            article.save()

        return Article.objects.all()
    
    def generate_tool_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом к-ве
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            tool = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}", h1_ru=f"Tool {i}", h1_en=f"Tool {i}")
            tool.save()

        return Tool.objects.all()
    
    def generate_note_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            note = Note(title_ru=f"Note {i}", title_en=f"Note {i}")
            note.save()
        
        return Note.objects.all()
    
    def test_sort_by_time_pub_button(self):
        ''' Тест на взаимодействие пользователя с кнопкой сортировки по времени '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                self.browser.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/")
                posts_titles_before_sort = self.browser.find_elements(By.CSS_SELECTOR, '.post_preview_title')
                articles_length = len(Article.objects.all())
                # Проверяем соответствуют ли слаги друг другу, несортированные
                time.sleep(1)        
                for indx, post in enumerate(posts_titles_before_sort):
                    self.assertEqual(post.text, f"{cat.categry_name} {articles_length - (indx + 1)}")
                # Проверяем соответствуют ли слаги друг другу, сортированные
                sort_button = self.browser.find_element(By.ID, 'onSort')
                sort_button.click()
                time.sleep(1)        
                posts_titles_after_sort = self.browser.find_elements(By.CSS_SELECTOR, '.post_preview_title')
                for indx, post in enumerate(posts_titles_after_sort):
                    self.assertEqual(post.text, f"{cat.categry_name} {indx}")
    
    def test_filter(self):
        ''' Тест на взаимодействие пользователя с кнопкой фильтрации по времени '''
        # Настраиваю дни публикации статей так, чтобы было предсказуемо определить количество выводимих статей
        art1 = Article.objects.get(slug='article-0')
        art1.timeCreated = art1.timeCreated.replace(year=2024,month=12,day=1) # Воскресенье
        art1.save()
        art2 = Article.objects.get(slug='article-1')
        art2.timeCreated = art2.timeCreated.replace(year=2024,month=12,day=8) # Воскресенье
        art2.save()
        art3 = Article.objects.get(slug='article-2')
        art3.timeCreated = art3.timeCreated.replace(year=2024,month=12,day=3)
        art3.save()
        art4 = Article.objects.get(slug='article-3')
        art4.timeCreated = art4.timeCreated.replace(year=2024,month=11,day=4)
        art4.save()
        # Настраиваю дни публикации инструментов так, чтобы было предсказуемо определить количество выводимих статей
        tool1 = Tool.objects.get(slug='tool-0')
        tool1.timeCreated = art1.timeCreated.replace(year=2024,month=12,day=1) # Воскресенье
        tool1.save()
        tool2 = Tool.objects.get(slug='tool-1')
        tool2.timeCreated = art2.timeCreated.replace(year=2024,month=12,day=8) # Воскресенье
        tool2.save()
        tool3 = Tool.objects.get(slug='tool-2')
        tool3.timeCreated = art3.timeCreated.replace(year=2024,month=12,day=3)
        tool3.save()
        tool4 = Tool.objects.get(slug='tool-3')
        tool4.timeCreated = art4.timeCreated.replace(year=2024,month=11,day=4)
        tool4.save()
        # Настраиваю дни публикации инструментов так, чтобы было предсказуемо определить количество выводимих статей
        note1 = Note.objects.all()[0]
        note1.timeCreated = art1.timeCreated.replace(year=2024,month=12,day=1) # Воскресенье
        note1.save()
        note2 = Note.objects.all()[1]
        note2.timeCreated = art2.timeCreated.replace(year=2024,month=12,day=8) # Воскресенье
        note2.save()
        note3 = Note.objects.all()[2]
        note3.timeCreated = art3.timeCreated.replace(year=2024,month=12,day=3)
        note3.save()
        note4 = Note.objects.all()[3]
        note4.timeCreated = art4.timeCreated.replace(year=2024,month=11,day=4)
        note4.save()

        for lang in LANGUAGES:
            for cat in Category.objects.all():
                message = f"In lang: {lang[0]} \t In category: {cat.categry_name}"
                self.browser.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/")
                # Находим все необходимые кнопки
                # Кнопка открытия контейнера с др. кнопками
                filter_container_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'filter_main_button'))
                )
                # Открываем контейнер
                filter_container_button.click()
                # Кнопка начала фильтрации
                filter_out_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'onFilterOut'))
                )
                # Прячем пагинатор ибо он мешает кликать)
                self.browser.execute_script("document.getElementById(arguments[0]).style.display = 'None' ", 'paginator_container')
                # Кнопка фильтрации за 2024
                year_2024_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'year-2024'))
                )
                # Кнопка фильтрации за Декабрь 2024
                month_dec_2024_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'dec'))
                )
                # Кнопка фильтрации за Декабрь, Воскресенье 2024
                day_sunday_month_dec_2024_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'sun'))
                )
                # Кнопка фильтрации за 1 число
                day_one_day_sunday_month_dec_2024_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'month-1'))
                )
                # Кнопка фильтрации за текущий год
                current_year_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'thistime-4'))
                )
                # Проверка на сортировку за год
                year_2024_button.click()
                filter_out_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 4, msg=message)
                # Проверка на сортировку за месяц
                month_dec_2024_button.click()
                filter_out_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 3, msg=message)
                # Проверка на сортировку за день недели
                day_sunday_month_dec_2024_button.click()
                filter_out_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 2, msg=message)
                # Проверка на сортировку за день месяца
                day_one_day_sunday_month_dec_2024_button.click()
                filter_out_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 1, msg=message)

        # Чтобы сохранить изолированность от других тестов в этом классе
        # нужно обнулить изменения сделанные тут. То есть сначала удалить всё, а потом пересоздать
        Article.objects.all().delete()
        Tool.objects.all().delete()
        Note.objects.all().delete()
        self.generate_article_queryset(0,20)
        self.generate_tool_queryset(0,20)
        self.generate_note_queryset(0,20)
    
    def test_paginator_buttons(self):
        ''' Тестируем кнопки пагинации '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                # Собщение для определения в какой категории и версии языка произошёл фейл
                message = f"In lang: {lang[0]} \t In category: {cat.categry_name}"
                self.browser.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/")
                # Проверяем подгрузку следующей страницы
                next_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'next_pagin_button'))
                )
                next_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 8, msg=message)
                # Проверяем загрузку предыдущей страницы
                prev_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'prev_pagin_button'))
                )
                prev_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 4, msg=message)
                # Проверяем загрузку последней страницы
                last_pagin_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#paginator_body>#paginator_last_page_example'))
                )
                last_pagin_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 4, msg=message)
                # Проверяем загрузку первой страницы
                first_pagin_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#paginator_body>#paginator_first_page_example'))
                )
                first_pagin_button.click()
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 4, msg=message)

    def test_scroll_uploading(self):
        ''' Тестируем подгрузку постов при скроллинге вниз '''
        for lang in LANGUAGES:
            for cat in Category.objects.all():
                # Собщение для определения в какой категории и версии языка произошёл фейл
                message = f"In lang: {lang[0]} \t In category: {cat.categry_name}"
                self.browser.get(f"{self.live_server_url}/{lang[0]}/{cat.slug}/")
                page = self.browser.find_element(By.TAG_NAME, 'body')
                page.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                posts = self.browser.find_elements(By.CSS_SELECTOR, ".post_preview")
                self.assertEqual(len(posts), 8, msg=message)
