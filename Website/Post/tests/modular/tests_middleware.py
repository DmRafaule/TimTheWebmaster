from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.core.files.base import ContentFile

from Main.models import Media
from Post.models import Category, Tool, Tag, Note
from Post.views import tool
from Post.middleware import ToolMiddleware


class MiddlewareTest(LiveServerTestCase):
    ''' Проверка программной прослойки для инструментов '''

    def setUp(self):
        # Создаём необходимые категории
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
        # Создаём необходимые инструменты, первому будут присвоены остальные элементы, созданые чуть ниже, второму будет присвоенно ничего
        i = 1
        self.tool_not_empty = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
        self.tool_not_empty.save()
        i = 2
        self.tool_empty = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
        self.tool_empty.save()
        i = 3
        tool2 = Tool(slug=f"tool-{i}", name_ru=f"инструмент {i}", name_en=f"tool {i}", description_ru=f"описание инстр {i}", description_en=f"tool descr {i}")
        tool2.save()
        # Создаём необходимые теги 
        i = 1
        tag1 = Tag(slug_en=f"tool-{i}", slug_ru=f"tool-{i}-ru", name_en=f"First {i} tag", name_ru=f"Первый {i} тег")
        tag1.save()
        i = 2
        tag2 = Tag(slug_en=f"tag{i}_en", slug_ru=f"teg{i}_ru", name_en=f"First {i} tag", name_ru=f"Первый {i} тег")
        tag2.save()
        # Создаём платформу
        icon = ContentFile('TEXT', name=f"icon-{1}.png")
        # Создаём необходимые заметки
        note1 = Note()
        note1.save()
        note1.tags.add(tag1)
        note1.tags.add(tag2)
        note1.save()
        note2 = Note()
        note2.save()
        note2.tags.add(tag1)
        note2.save()
        note3 = Note()
        note3.save()
        # Создаём медиа файлы
        file = ContentFile('TEXT', name=f"icon.txt")
        self.downloadable = Media(file=file, type=Media.RAW_FILE)
        self.downloadable.save()
        file = ContentFile('TEXT', name=f"icon.svg")
        self.image = Media(file=file, type=Media.IMAGE)
        self.image.save()
        file = ContentFile('TEXT', name=f"icon.mp3")
        self.audio = Media(file=file, type=Media.AUDIO)
        self.audio.save()
        file = ContentFile('TEXT', name=f"icon.pdf")
        self.pdf = Media(file=file, type=Media.PDF)
        self.pdf.save()
        file = ContentFile('TEXT', name=f"icon.mp4")
        self.video = Media(file=file, type=Media.VIDEO)
        self.video.save()
        # Присваиваем всё что было ранее создано для тестового инструмента, который будет протестирован на наличность присвоенных элементов
        self.tool_not_empty.media.add(self.downloadable)
        self.tool_not_empty.media.add(self.image)
        self.tool_not_empty.media.add(self.audio)
        self.tool_not_empty.media.add(self.pdf)
        self.tool_not_empty.media.add(self.video)
        self.tool_not_empty.similar.add(self.tool_empty)
        self.tool_not_empty.similar.add(tool2)
        self.tool_not_empty.tags.add(tag1)
        self.tool_not_empty.tags.add(tag2)
        self.tool_not_empty.save()

    def test_middleware_on_customized_tool(self):
        ''' Тест для кастомизированного инструмента '''
        # Имитирую работу программной прослойки, для проверки результатов в возвращаемом контексте
        request = RequestFactory().get(f"{self.live_server_url}{self.tool_not_empty.get_absolute_url()}")
        middleware = ToolMiddleware(tool(request, self.tool_not_empty.slug))
        middleware.tool_handler(request, middleware.get_response)
        data = middleware.get_response.context_data
        # Соответствующие проверки
        self.assertEqual(data.get('url_to_share'), f'testserver{self.tool_not_empty.get_absolute_url()}')
        self.assertIn(self.downloadable, data.get('downloadables'))
        self.assertIn(self.image, data.get('images'))
        self.assertIn(self.video, data.get('videos'))
        self.assertIn(self.pdf, data.get('pdfs'))
        self.assertIn(self.audio, data.get('audios'))
        self.assertEqual(data.get('tool_tag'), self.tool_not_empty.tags.all()[0].slug)
        self.assertEqual(len(data.get('posts')), 2)
        self.assertTrue(data.get('is_notes'))

    def test_middleware_on_empty_tool(self):
        ''' Тест для пустого инструмента '''
        # Имитирую работу программной прослойки, для проверки результатов в возвращаемом контексте
        request = RequestFactory().get(f"{self.live_server_url}{self.tool_empty.get_absolute_url()}")
        middleware = ToolMiddleware(tool(request, self.tool_empty.slug))
        middleware.tool_handler(request, middleware.get_response)
        data = middleware.get_response.context_data
        # Соответствующие проверки
        self.assertEqual(data.get('url_to_share'), f'testserver{self.tool_empty.get_absolute_url()}')
        self.assertNotIn(self.downloadable, data.get('downloadables'))
        self.assertNotIn(self.image, data.get('images'))
        self.assertNotIn(self.video, data.get('videos'))
        self.assertNotIn(self.pdf, data.get('pdfs'))
        self.assertNotIn(self.audio, data.get('audios'))
        self.assertIsNone(data.get('tool_tag'))
        self.assertIsNone(data.get('posts'))
        self.assertIsNone(data.get('is_notes'))