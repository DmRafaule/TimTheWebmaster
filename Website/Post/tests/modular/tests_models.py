from django.test import TestCase
from django.core.files.base import ContentFile
from django.test import RequestFactory, LiveServerTestCase

from Post.models import Article, Tool, Note, Category, Tag, Platform, Termin, Question 


class ModelsTest(LiveServerTestCase):
    ''' Тесты для тестирования моделей приложения '''
    #TODO: 
    # * Написать тесты для проверок миграций
    # * Написать тесты для проверок валидации полей

    def setUp(self):
        # Создаём две необходимые категории для хранения статей, инструментов, заметок
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
        self.categories = Category.objects.all()
        # Генерируем необходимый пул объектов проверяемых моделей
        self.articles = self.generate_article_queryset(0,10)
        self.tools = self.generate_tool_queryset(0,10)
        self.notes = self.generate_note_queryset(0,10)
        self.tags = self.generate_tag_queryset(0,10)
        self.questions = self.generate_question_queryset(0,5)
        self.termins = self.generate_termin_queryset(0,5)
        self.platform1 = self.create_platform(1)
        self.platform2 = self.create_platform(2)

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

    def generate_tag_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор инструментов в заданом количестве 
            с заданного индекса'''
        for i in range(start_indx, start_indx + max_el_in):
            tag = Tag(slug_en=f"tag{i}_en", slug_ru=f"teg{i}_ru", name_en=f"First {i} tag", name_ru=f"Первый {i} тег")
            tag.save()
        
        return Tag.objects.all()

    def create_platform(self, indx):
        ''' Создаёт платформы с указаным индексом '''
        icon = ContentFile('TEXT', name=f"icon-{indx}.png")
        platform = Platform(name_ru="платформа", name_en="platform", icon=icon)
        platform.save()
        return platform
    
    def generate_question_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор вопросов в указанном диапазоне '''
        for i in range(start_indx, start_indx + max_el_in):
            question1 = Question(id=i, question_ru=f"q{i}", question_en=f"q{i}", description_ru=f"q{i} d", description_en=f"q{i} d", answer_ru=f"q{i} def", answer_en=f"q{i} def")
            question1.save()
        return Question.objects.all()
            
    def generate_termin_queryset(self, start_indx, max_el_in):
        ''' Генерирует набор определений в указанном диапазоне '''
        for i in range(start_indx, start_indx + max_el_in):
            termin1 = Termin(id=i, termin_ru=f"t{i}", termin_en=f"t{i}", description_ru=f"t{i} d", description_en=f"t{i} d", definition_ru=f"t{i} def", definition_en=f"t{i} def")
            termin1.save()
        return Termin.objects.all()
    
    def test_Article_model(self):
        ''' Проверка модели Article '''
        # Проверяем значения заданные по умолчанию, 
        # Связи с другими моделями
        for article in self.articles:
            self.assertEqual(len(article.similar.all()), 0)
            self.assertEqual(len(article.termins.all()), 0)
            self.assertEqual(len(article.questions.all()), 0)
            self.assertEqual(len(article.tags.all()), 0)
            self.assertEqual(len(article.media.all()), 0)
        
        # Задаём новые значения
        # Связи с другими моделями
        custom_article = self.articles[0]
        custom_article.similar.add(self.articles[2])
        custom_article.similar.add(self.articles[1])
        custom_article.termins.add(self.termins[0])
        custom_article.termins.add(self.termins[1])
        custom_article.questions.add(self.questions[0])
        custom_article.questions.add(self.questions[1])
        custom_article.tags.add(self.tags[0])
        custom_article.tags.add(self.tags[1])
        custom_article.save()

        # Проверяем значения заданные после
        # Связи с другими моделями
        self.assertEqual(len(self.articles[0].similar.all()), 2)
        self.assertEqual(len(self.articles[0].termins.all()), 2)
        self.assertEqual(len(self.articles[0].questions.all()), 2)
        self.assertEqual(len(self.articles[0].tags.all()), 2)
        self.assertEqual(len(self.articles[0].media.all()), 0)
    
    def test_Tool_model(self):
        ''' Проверка модели Tool '''
        # Проверяем значения заданные по умолчанию
        # Связи с другими моделями
        for tool in self.tools:
            self.assertEqual(len(tool.similar.all()), 0)
            self.assertEqual(len(tool.tags.all()), 0)
            self.assertEqual(len(tool.platforms.all()), 0)

        # Задаём новые значения
        # Связи с другими моделями
        custom_tool = self.tools[0]
        custom_tool.similar.add(self.tools[1])
        custom_tool.similar.add(self.tools[2])
        custom_tool.tags.add(self.tags[0])
        custom_tool.tags.add(self.tags[1])
        custom_tool.platforms.add(self.platform1)
        custom_tool.platforms.add(self.platform2)
        custom_tool.save()

        # Проверяем значения заданные после
        # Связи с другими моделями
        self.assertEqual(len(self.tools[0].similar.all()), 2)
        self.assertEqual(len(self.tools[0].tags.all()), 2)
        self.assertEqual(len(self.tools[0].platforms.all()), 2)
    
    def test_Note_model(self):
        ''' Проверка модели Note '''
        # Проверяем значения заданные по умолчанию
        # Связи с другими моделями
        for tool in self.notes:
            self.assertEqual(len(tool.tags.all()), 0)

        # Задаём новые значения
        # Связи с другими моделями
        custom_note = self.notes[0]
        custom_note.tags.add(self.tags[0])
        custom_note.tags.add(self.tags[1])
        custom_note.save()

        # Проверяем значения заданные после
        # Связи с другими моделями
        self.assertEqual(len(self.notes[0].tags.all()), 2)