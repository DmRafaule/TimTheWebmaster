from django.test import TestCase
from django.core.files.base import ContentFile

from Main.models import Website, Contact, Media
from Post.models import Article, Tool, Note, Category, Tag

#TODO: Доделай тестирование моделей:
# * Проверку валидации полей
# * Проверку кастомной логики в моделях
class ModelsTest(TestCase):
    ''' Тесты для тестирования моделей приложения '''

    def setUp(self):
        # Создаём необходимые категории
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        note_cat = Category(slug='notes', name_ru="Заметки", name_en="Notes", description_ru="Описание заметок", description_en="Notes\' description" )
        note_cat.save()
        self.categories = Category.objects.all()
        # Генерируем группы объектов в БД
        self.articles = self.generate_article_queryset(0,10)
        self.tools = self.generate_tool_queryset(0,10)
        self.notes = self.generate_note_queryset(0,10)
        self.tags = self.generate_tag_queryset(0,10)

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

    def test_Website_model(self):
        ''' Проверяем на возможность создания, изменения, удаления в таблицу Website '''
        # Проверка создания модели Website
        website1 = Website(name='website-1')
        website1.save()
        website1.popular_articles_on_footer.add(self.articles[0])
        website1.popular_tools_on_footer.add(self.tools[0])
        website1.my_resources_choosen_tags_on_home.add(self.tags[0])
        website1.other_articles_choosen_tags_on_home.add(self.tags[1])
        website1.save()
        self.assertIn(website1, Website.objects.all())
        # Проверка изменения полей на записе в моделе Website
        website1.popular_articles_on_footer.add(self.articles[1])
        website1.popular_tools_on_footer.add(self.tools[1])
        website1.save()
        self.assertEqual(len(website1.popular_articles_on_footer.all()), 2)
        self.assertEqual(len(website1.popular_tools_on_footer.all()), 2)
        # Проверка удаления записи Website
        website1.delete()
        self.assertEqual(len(Website.objects.all()), 0)

    def test_Contact_model(self):
        ''' Проверяем на возможность создания, изменения, удаления в таблицу Contact '''
        # Проверка создания модели Contact 
        icon = ContentFile('TEXT', name=f"icon.svg")
        contact = Contact(icon=icon, name_en="Icon1", name_ru="Иконка1", url="https://google.com")
        contact.save()
        self.assertIn(contact, Contact.objects.all())
        # Проверка изменения полей на записе в моделе Contact
        new_url = "http://fivver.com"
        contact.url = new_url
        contact.save()
        self.assertEqual(len(Contact.objects.filter(url=new_url)), 1)
        # Проверка удаления записи Contact
        contact.delete()
        self.assertEqual(len(Contact.objects.all()), 0)


    def test_Media_model(self):
        ''' Проверяем на возможность создания, изменения, удаления в таблицу Media '''
        # Проверка создания модели Media
        file = ContentFile('TEXT', name=f"icon.txt")
        Media(file=file, type=Media.RAW_FILE).save()
        file = ContentFile('TEXT', name=f"icon.svg")
        Media(file=file, type=Media.IMAGE).save()
        file = ContentFile('TEXT', name=f"icon.mp3")
        Media(file=file, type=Media.AUDIO).save()
        file = ContentFile('TEXT', name=f"icon.pdf")
        Media(file=file, type=Media.PDF).save()
        file = ContentFile('TEXT', name=f"icon.mp4")
        Media(file=file, type=Media.VIDEO).save()
        self.assertEqual(len(Media.objects.all()), 5)
        # Проверка изменения полей на записе в моделе Media
        media = Media.objects.get(id=1)
        media.type = Media.VIDEO
        media.save()
        self.assertEqual(media.type, Media.VIDEO)
        # Проверка удаления записи Media 
        media.delete()
        self.assertEqual(len(Media.objects.all()), 4)