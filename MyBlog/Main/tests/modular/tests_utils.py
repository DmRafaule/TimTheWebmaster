import math
import json

from django.urls import reverse
from django.test import TestCase, RequestFactory
from datetime import datetime
from django.core.files.base import ContentFile

from Main.utils import *
from Post.models import Tag, Article, Tool, Category
from Main.models import Contact
from MyBlog.settings import ALLOWED_HOSTS

class UtilsTests(TestCase):
    ''' Проверка функций-утилит '''

    def setUp(self):
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()

        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()

        self.categories = Category.objects.all()

    def generate_article_queryset(self, max_el_in):
        ''' Генерирует набор статей в заданом количестве '''
        for i in range(max_el_in):
            file = ContentFile('TEXT', name=f"index-{i}.html")
            article = Article(slug=f"article-{i}", template=file)
            article.save()

        return Article.objects.all()
    
    def generate_tool_queryset(self, max_el_in):
        ''' Генерирует набор инструментов в заданом к-ве'''
        for i in range(max_el_in):
            tool = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
            tool.save()

        return Article.objects.all()
    
    def apply_tag_to_queryset(self, tag, queryset):
        ''' Присваивается тек ко всем элементав в наборе запросов '''
        for article in queryset:
            article.tags.add(tag)
            article.save()

    def test_get_how_old_human_in_years(self):
        ''' Сколько лет вернёт данная функция '''
        years = get_how_old_human_in_years('16/07/1900', "%d/%m/%Y")
        day_of_birth = datetime.strptime('16/07/1900', "%d/%m/%Y").date()
        today = datetime.today().date()
        self.assertEqual(years, math.trunc((today-day_of_birth).days/365))

    def test_get_posts_by_tag(self):
        ''' Как много вернёт постов в зависимотси от отправляемого тега '''
        # Создаём тег
        tag = Tag(slug_en="tag1_en", slug_ru="teg1_ru", name_en="First tag", name_ru="Первый тег")
        tag.save()
        # Генерируем группу запросов
        articles = self.generate_article_queryset(10)
        # Применяем один тег к первым двум элементам в группе
        self.apply_tag_to_queryset(tag, articles[:2])
        # Находим элементы с искомым тегом в модели Article
        articles_by_tag = get_posts_by_tag('tag1_en', Article)
        self.assertEqual(len(articles_by_tag), 2)

    def test_getAllWithTags(self):
        ''' Как много вернёт постов в зависимотси от отправляемых тегов '''
        # Создаём теги
        tag1 = Tag(slug_en="tag1_en", slug_ru="teg1_ru", name_en="First tag", name_ru="Первый тег")
        tag1.save()
        tag2 = Tag(slug_en="tag2_en", slug_ru="teg2_ru", name_en="Second tag", name_ru="Второй тег")
        tag2.save()
        # Генерируем группу запросов
        articles = self.generate_article_queryset(10)
        # Применяем первый тег к первой половине группы элементов
        # Второй тег применяем ко второй половине группы элементов
        self.apply_tag_to_queryset(tag1, articles[:5])
        self.apply_tag_to_queryset(tag2, articles[5:10])
        # Находим только те элементы в которых присутствуют оба тега
        # Их должно быть 0
        articles_with_all_tags_in = getAllWithTags(articles, [tag1, tag2], 2)
        self.assertEqual(len(articles_with_all_tags_in), 0)
        # Применяем первый тег уже ко второй половине группы элементов
        self.apply_tag_to_queryset(tag1, articles[5:10])
        # Находим только те элементы в которых присутствуют оба тега
        # Их должно быть 5
        articles_with_all_tags_in = getAllWithTags(articles, [tag1, tag2], 2)
        self.assertEqual(len(articles_with_all_tags_in), 5)

    def test_get_latest_post(self):
        ''' Как много вернёт последних постов '''
        articles = self.generate_article_queryset(10)
        # Должен вернуть три последних статьи
        latest_articles = get_latest_post(3, articles)
        self.assertEqual(len(latest_articles), 3)
        # Я удаляю все записи в БД, потому что потребуется
        # пересоздать немного меньше элементов, чуть ниже в коде
        articles.all().delete()
        # Должен вернуть 0 постов ибо минимально допустимое к-во 3, 
        # а в группе есть только 2
        articles = self.generate_article_queryset(2)
        latest_articles = get_latest_post(3, articles)
        self.assertEqual(len(latest_articles), 0)

    def test_get_tool(self):
        ''' Вернёт ли инструмент по URL '''
        # Генерируем группу инструментов 
        self.generate_tool_queryset(10)
        # Пытаемся получить не существующий инструмент
        tool = get_tool('http://localhost:8000/en/tools/tool-11/')
        self.assertIsNone(tool)
        # Пытаемся получить уже существующий инструмент
        tool = get_tool('http://localhost:8000/en/tools/tool-1/')
        self.assertIsNotNone(tool)

    def test_getNotEmptyCategories(self):
        ''' Как много категорий вернёт в которых есть посты '''
        # Так как никаких постов ещё не было опубликованно не вернётся ни одна категория
        categories = getNotEmptyCategories(self.categories)
        self.assertEqual(len(categories), 0)
        # Так как есть статьи вернётся одна категория
        self.generate_article_queryset(10)
        categories = getNotEmptyCategories(self.categories)
        self.assertEqual(len(categories), 1)
        # Так как есть, и инструменты, и статьи вернётся 2 категории
        self.generate_tool_queryset(10)
        categories = getNotEmptyCategories(self.categories)
        self.assertEqual(len(categories), 2)

    def test_getSpecialTopLevelCategories(self):
        ''' Как много категорий вернёт, которые были указаны в настройках сайта '''
        # Мы не добавили ни одной статьи и ни одного инструмента
        # Плюс в модели Website мы не указали избранные категории
        # Значит вернётся 0
        categories = getSpecialTopLevelCategories(self.categories)
        self.assertEqual(len(categories), 0)

    def test_initDefaults(self):
        ''' Какие контекстные данные вернёт '''
        # Генерируем запрос
        url = reverse('home')
        request = RequestFactory().get(url)
        # Генерируем статьи, инструменты и контакт для проверки
        self.generate_article_queryset(10)
        self.generate_tool_queryset(10)
        icon = ContentFile('TEXT', name=f"icon.svg")
        Contact(icon=icon, name_en="Icon1", name_ru="Иконка1", url="https://google.com").save()
        # Получаем и проверяем вернувшиеся контекстные данные
        context_data = initDefaults(request)
        self.assertEqual(len(context_data['categories_special']), 2)
        self.assertIn(context_data['domain_name'], ALLOWED_HOSTS)
        self.assertEqual(len(context_data['contacts']), 1)
        self.assertEqual(len(context_data['popular_posts']), 0)
        self.assertIsNone(context_data['default_post_preview'])