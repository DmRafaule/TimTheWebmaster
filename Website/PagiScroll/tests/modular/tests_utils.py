import time

from django.test import TestCase
from django.core.files.base import ContentFile

from Post.models import Category, Article, Note, Tool, Post
from PagiScroll.utils import calculate_pages, in_alphabetic, in_order
import PagiScroll.utils as P_utils 


class UtilsCommonTest(TestCase):
    ''' Тестирование ф-ий утилит '''

    def setUp(self):
        # Создаём категории
        self.article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        self.article_cat.save()
        # Создаём категорию
        self.tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        self.tool_cat.save()
        # Создаём категорию
        self.note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        self.note_cat.save()
        # Генерируем посты различных типов
        self.generate_article_queryset(0,5)
        self.generate_tool_queryset(0,5)
        self.generate_note_queryset(0,5)

    def generate_article_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор статей в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            file = ContentFile('TEXT', name=f"index-{i}.html")
            article = Article(slug=f"article-{i}", template=file)
            article.save()
            article.timeCreated = article.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            article.save()
            time.sleep(0.1)

        return Article.objects.all()
    
    def generate_tool_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом к-ве
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            tool = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
            tool.save()
            tool.timeCreated = tool.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            tool.save()
            time.sleep(0.1)

        return Tool.objects.all()
    
    def generate_note_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            note = Note()
            note.save()
            note.timeCreated = note.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            note.save()
            time.sleep(0.1)
        
        return Note.objects.all()

    def test_calculate_page(self):
        ''' Тест того, сколько элементов(страниц) для пагинатора будет сгенерированно '''
        total_items = 20
        items_per_page = 5
        total_pages = calculate_pages(total_items, items_per_page)
        self.assertEqual(total_pages, 4)
    
    def test_in_order_article(self):
        ''' Тестируем сортировку группы элементов статей в БД '''
        queryset = Article.objects.all()
        # Не сортируем
        queryset = in_order(queryset, 'false')
        expected_values = [1,2,3,4,5]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
        # Сортируем
        queryset = in_order(queryset, 'true')
        expected_values = [5,4,3,2,1]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
    
    def test_in_order_tool(self):
        ''' Тестируем сортировку группы элементов инструментов в БД '''
        queryset = Tool.objects.all()
        # Не сортируем
        queryset = in_order(queryset.all(), 'false')
        expected_values = [6,7,8,9,10]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
        # Сортируем
        queryset = in_order(queryset.all(), 'true')
        expected_values = [10,9,8,7,6]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
    
    def test_in_order_note(self):
        ''' Тестируем сортировку группы элементов заметок в БД '''
        queryset = Note.objects.all()
        # Не сортируем
        queryset = in_order(queryset, 'false')
        expected_values = [1,2,3,4,5]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
        # Сортируем
        queryset = in_order(queryset, 'true')
        expected_values = [5,4,3,2,1]
        self.assertQuerySetEqual(queryset.all(), expected_values, transform=lambda item: item.id)
    
    def test_posts_by_letters(self):
        # На данный момент этот тип сортирвки не актуален для сайта
        pass

class UtilsRelatedTimingTest(TestCase):
    ''' Специальный класс для тестирования записей в БД, с различными таймингом создания '''
    def setUp(self):
        # Создаём категории
        self.article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        self.article_cat.save()
        # Создаём категорию
        self.tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        self.tool_cat.save()
        # Создаём категорию
        self.note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        self.note_cat.save()
        # Генерируем посты различных типов
        articles = self.generate_article_queryset(0,4)
        tools = self.generate_tool_queryset(0,4)
        notes = self.generate_note_queryset(0,4)
        self.art1 = articles[0]
        self.art1.timeCreated = self.art1.timeCreated.replace(year=2020, month=1, day=1)#wen
        self.art1.save()
        self.art2 = articles[1]
        self.art2.timeCreated = self.art2.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.art2.save()
        self.art3 = articles[2]
        self.art3.timeCreated = self.art3.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.art3.save()
        self.tool1 = tools[0]
        self.tool1.timeCreated = self.tool1.timeCreated.replace(year=2020, month=1, day=1)#wen
        self.tool1.save()
        self.tool2 = tools[1]
        self.tool2.timeCreated = self.tool2.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.tool2.save()
        self.tool3 = tools[2]
        self.tool3.timeCreated = self.tool3.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.tool3.save()
        self.note1 = notes[0]
        self.note1.timeCreated = self.note1.timeCreated.replace(year=2020, month=1, day=1)#wen
        self.note1.save()
        self.note2 = notes[1]
        self.note2.timeCreated = self.note2.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.note2.save()
        self.note3 = notes[2]
        self.note3.timeCreated = self.note3.timeCreated.replace(year=2021, month=2, day=2)#tue
        self.note3.save()

    def generate_article_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор статей в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            file = ContentFile('TEXT', name=f"index-{i}.html")
            article = Article(slug=f"article-{i}", template=file)
            article.save()
            article.timeCreated = article.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            article.save()
            time.sleep(1)

        return Article.objects.all()
    
    def generate_tool_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом к-ве
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            tool = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
            tool.save()
            tool.timeCreated = tool.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            tool.save()
            time.sleep(1)

        return Tool.objects.all()
    
    def generate_note_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            note = Note()
            note.save()
            note.timeCreated = note.timeCreated.replace(year=2024, month=12, day=12, hour=11, minute=11)
            note.save()
            time.sleep(1)
        
        return Note.objects.all()

    def test_get_articles_by_years(self):
        ''' Получение статей по году создания '''
        queryset = P_utils.get_posts_by_years([2020,2021], Article.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_articles_by_months(self):
        ''' Получение статей по месяцу создания '''
        queryset = P_utils.get_posts_by_months([1,2], Article.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_articles_by_month_days(self):
        ''' Получение статей по дню месяца создания '''
        queryset = P_utils.get_posts_by_month_days([1,2], Article.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_articles_by_week_days(self):
        ''' Получение статей по дню недели создания '''
        queryset = P_utils.get_posts_by_week_days([3, 2], Article.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_tools_by_years(self):
        ''' Получение инструментов по году создания '''
        queryset = P_utils.get_posts_by_years([2020,2021], Tool.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_tools_by_months(self):
        ''' Получение инструментов по месяцу создания '''
        queryset = P_utils.get_posts_by_months([1,2], Tool.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_tools_by_month_days(self):
        ''' Получение инструментов по дню месяца создания '''
        queryset = P_utils.get_posts_by_month_days([1,2], Tool.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_tools_by_week_days(self):
        ''' Получение инструментов по дню недели создания '''
        queryset = P_utils.get_posts_by_week_days([3, 2], Tool.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_notes_by_years(self):
        ''' Получение заметок по году создания '''
        queryset = P_utils.get_posts_by_years([2020,2021], Note.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_notes_by_months(self):
        ''' Получение заметок по месяцу создания '''
        queryset = P_utils.get_posts_by_months([1,2], Note.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_notes_by_month_days(self):
        ''' Получение заметок по дню месяца создания '''
        queryset = P_utils.get_posts_by_month_days([1,2], Note.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")

    def test_get_notes_by_week_days(self):
        ''' Получение заметок по дню недели создания '''
        queryset = P_utils.get_posts_by_week_days([3, 2], Note.objects.all())
        self.assertEqual(len(queryset), 3, msg=f"In queryset: {queryset}")
