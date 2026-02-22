import os

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __
from django.db.models.signals import m2m_changed, pre_save
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from modeltranslation.manager import MultilingualManager

from Website import settings as S
from Main.models import Media, LangManager, LanguageType


def user_directory_path(instance, filename):
    ''' Для указания путя по сохранению файлов для постов типа Статей и инструментов 
    
    arguments:
    ----------
        instance: Объект модели Post
        filename: Имя файла для сохранения

    returns:
    --------
        Путь типа str до файла
    '''
    return "{0}/{1}/{2}".format(instance.category.slug, instance.slug, filename)

def service_path(instance, filename):
    return "{0}/{1}".format(instance.category.slug, filename)


class Tag(models.Model):
    ''' Модель тегов, для фильтрации других моделей у которых есть соответствующие отношения с этой моделью '''
    slug = models.SlugField(unique=True, max_length=60, blank=False, default='')
    name = models.CharField(max_length=256, unique=True, blank=False)

    def __str__(self):
        return self.name
    
    #TODO: Эта функция ошибочна, исправь
    def get_absolute_url(self, *args, **kwargs):
        return reverse(f'articles-list')

class Category(models.Model):
    ''' Модель для определения и кастомизации категорий-деревиативов от Post модели (Например Article, Tool, Note) '''

    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    categry_name = models.SlugField(max_length=50, unique=False, blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f'{self.slug}-list')

class Post(models.Model):
    ''' Базовая модель для создания деревиативов, которые будут доступны пользователям '''
    view_name = "post"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    slug = models.SlugField(max_length=256, unique=True)
    timeCreated = models.DateTimeField()
    timeUpdated = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    media = models.ManyToManyField(Media, blank=True, help_text="Obsolete for articles, do not use")

    def save(self, *args, **kwargs):
        self.timeUpdated = timezone.now()
        if not self.timeCreated:
            self.timeCreated = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(self.view_name, kwargs={"post_slug": self.slug})

    def __str__(self):
        return self.slug

class Question(models.Model):
    ''' Модель для создания вопросов относящихся к тому или иному посту '''
    question = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    answer = models.TextField(max_length=360, blank=False)

    def __str__(self):
        return self.question

class Termin(models.Model):
    ''' Модель для создания определений относящихся к тому или иному посту '''
    termin = models.CharField(max_length=60, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    definition = models.TextField(max_length=360,blank=False)

    def __str__(self):
        return self.termin
    
class Article(Post):
    ''' Модель-деривиатив от модели Post, для хранения контента сайта (Статьи) '''
    view_name = "article"
    max_similar = 3
    title = models.CharField(max_length=256, blank=False, default='')
    h1 = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(max_length=256, blank=True)
    meta_keywords = models.CharField(max_length=256, blank=True, default='')
    preview = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)
    # Шаблон для отрисовки пользователю
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=False)  # page to display
    # Относящиеся по смыслу вопросы
    questions = models.ManyToManyField(Question, blank=True, help_text='You only use this field to pin actualy needed qas. Other will come automatically')
    # Относящиеся по смыслу определения 
    termins = models.ManyToManyField(Termin, blank=True, help_text='You only use this field to pin actualy needed tds. Other will come automatically')
    # Похожие по тематике другие посты
    similar = models.ManyToManyField('self', blank=True, help_text="Up to 3 choises", symmetrical=False)

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Article)
def _post_save_category_article(sender, instance, **kwargs): 
    # Задаём соответствующую категорию, а если её нет, то создаём основу
    category, is_created = Category.objects.get_or_create(slug="articles")
    if is_created:
        category.name_ru = "Статьи"
        category.name_en = "Articles"
        category.description_ru = "Описание статей"
        category.description_en = "Articles\' description"
        category.categry_name = "Article"
        category.save()
    instance.category = category

def similar_articles_changed(sender, **kwargs):
    ''' Определяет то, сколько похожих статей можно будет назначить '''
    if kwargs['instance'].similar.count() > Article.max_similar:
        raise ValidationError("You can't assign more than three articles", code="invalid")

m2m_changed.connect(similar_articles_changed, sender=Article.similar.through)


# Создаем гибридный менеджер, для того чтобы пакет переводов не 
# Не мешал получать необходимые модели
class ToolManager(PolymorphicManager, MultilingualManager):
    pass
# Базовый класс для создания различных типов инструментов, смотри ниже
class Tool(Post, PolymorphicModel):
    ''' Модель-деривиатив от модели Post, для хранения шаблонных инструментов (то есть те инструменты, которые не работают в вебе, онлайн) '''
    view_name = "tool"
    max_similar = 3
    objects = ToolManager()
    name = models.CharField(max_length=256, blank=False)
    h1 = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(blank=False)
    meta_keywords = models.CharField(max_length=256, blank=True, default='')
    icon = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)
    # Шаблон который будет отрисовываться вместо шаблона по умолчанию
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=True, help_text="If provided, default template not in use. Use only if it is Internal default type")

    # Похожие инструменты
    similar = models.ManyToManyField('self', blank=True, help_text="Up to 3 choises", symmetrical=False)
    
    # Тип инструмента, используется в разметке
    class ToolType(models.TextChoices):
        GameApplication = "GameApplication"
        SocialNetworkingApplication = "SocialNetworkingApplication"
        TravelApplication = "TravelApplication"
        ShoppingApplication = "ShoppingApplication"
        SportsApplication = "SportsApplication"
        LifestyleApplication = "LifestyleApplication"
        BusinessApplication = "BusinessApplication"
        DesignApplication = "DesignApplication"
        DeveloperApplication = "DeveloperApplication"
        DriverApplication = "DriverApplication"
        EducationalApplication = "EducationalApplication"
        HealthApplication = "HealthApplication"
        FinanceApplication = "FinanceApplication"
        SecurityApplication = "SecurityApplication"
        BrowserApplication = "BrowserApplication"
        CommunicationApplication = "CommunicationApplication"
        DesktopEnhancementApplication = "DesktopEnhancementApplication"
        EntertainmentApplication = "EntertainmentApplication"
        MultimediaApplication = "MultimediaApplication"
        HomeApplication = "HomeApplication"
        UtilitiesApplication = "UtilitiesApplication"
        ReferenceApplication = "ReferenceApplication"
        VideoGame = "VideoGame"
        MobileApplication = "MobileApplication"
        WebApplication = "WebApplication"
    type = models.CharField(max_length=100, choices=ToolType, default=ToolType.WebApplication)

    def save(self, *args, **kwargs):
        super(Tool, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{get_language()}/tools/{self.slug}/'
    
class TelegramBot(Tool):
    common_icon_path = "Post/img/telegram.svg"

    @property
    def common_name(self):
        return _("Телеграм бот")
    
    bot_name = models.CharField(max_length=256, blank=False)
    bot_qr   = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True, help_text="QR code of your TG bot")

    class BotType(models.TextChoices):
        ChatBot = "Chat bot"
        InlineBot = "Inline bot"
        WebBot = "Web bot"
    bot_type = models.CharField(max_length=100, choices=BotType, default=BotType.ChatBot)
    @property
    def get_bot_type(self):
        match self.bot_type:
            case TelegramBot.BotType.ChatBot:
                return _("Чат бот")
            case TelegramBot.BotType.InlineBot:
                return _("Инлайн бот")
            case TelegramBot.BotType.WebBot:
                return _("Веб бот")

class WebTool(Tool):
    common_icon_path = "Post/img/webtool.svg"
    
    @property
    def common_name(self):
        return _("Веб инструмент")

    landscape_preview = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)

class DjangoApp(Tool):
    common_icon_path = "Post/img/django.svg"
    
    @property
    def common_name(self):
        return _("Джанго приложение")
    
    use_cases = models.ManyToManyField(Media, blank=True, help_text="Use cases of this app. Only images.")
    
    class AppKind(models.TextChoices):
        StandaloneApp = "Standalone App"
        Middleware = "Middleware"
        APIHotspot = "API Hotspot"
    app_type = models.CharField(max_length=100, choices=AppKind, default=AppKind.StandaloneApp)
    @property
    def get_app_type(self):
        match self.app_type:
            case DjangoApp.AppKind.StandaloneApp:
                return _("Приложение")
            case DjangoApp.AppKind.Middleware:
                return _("Мидлвари")
            case DjangoApp.AppKind.APIHotspot:
                return _("API")

class Scraper(Tool):
    common_icon_path = "Post/img/scraper.svg"
    
    @property
    def common_name(self):
        return _("Парсер")
    
    target = models.CharField(max_length=256, help_text="What the main target of this scraper.", blank=False)
    
    class HowManyThreads(models.TextChoices):
        SingleThreaded = "Single Threaded"
        MultiThreaded = "Multi Threaded"
    how_many_threads = models.CharField(max_length=100, choices=HowManyThreads, default=HowManyThreads.SingleThreaded)
    @property
    def get_threading(self):
        match self.how_many_threads:
            case Scraper.HowManyThreads.SingleThreaded:
                return _("Однопоточный")
            case Scraper.HowManyThreads.MultiThreaded:
                return _("Многопоточный")
    
    class WhatType(models.TextChoices):
        Static = "Static"
        Dynamic = "Dynamic"
        API     = "API"
    what_type = models.CharField(max_length=100, choices=WhatType, default=WhatType.Static)
    @property
    def get_what_type(self):
        match self.what_type:
            case Scraper.WhatType.Static:
                return _("Статический")
            case Scraper.WhatType.Dynamic:
                return _("Динамический")
            case Scraper.WhatType.API:
                return _("Через API")

    class LanguageUsed(models.TextChoices):
        Python = "Python"
        JS = "JS"
    language_used = models.CharField(max_length=100, choices=LanguageUsed, default=LanguageUsed.Python)
    @property
    def get_language_used(self):
        return self.language_used

    class WithProxies(models.TextChoices):
        WithProxies = "With Proxies"
        NoProxies = "No Proxies"
    with_proxies = models.CharField(max_length=100, choices=WithProxies, default=WithProxies.NoProxies)
    @property
    def get_with_proxies(self):
        match self.with_proxies:
            case Scraper.WithProxies.WithProxies:
                return _("С прокси")
            case Scraper.WithProxies.NoProxies:
                return _("Без прокси")

    class WithSwapping(models.TextChoices):
        WithSwapping = "With Swapping"
        NoSwapping = "No Swapping"
    with_swapping = models.CharField(max_length=100, choices=WithSwapping, default=WithSwapping.NoSwapping)
    @property
    def get_with_swapping(self):
        match self.with_swapping:
            case Scraper.WithSwapping.WithSwapping:
                return _("С ротацией агентов")
            case Scraper.WithSwapping.NoSwapping:
                return _("Без ротации агентов")

class Script(Tool):
    common_icon_path = "Post/img/script.svg"
    
    @property
    def common_name(self):
        return _("Скрипт")
    
    most_valuable_action = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True, help_text="Only gif type of image are allowed.")

    class ScriptInterface(models.TextChoices):
        OneRunner = "Only one command to run"
        CommandLineInterface = "Command line interface"
        TerminalUserInterface = "Terminal user interface"
    interface_type = models.CharField(max_length=100, choices=ScriptInterface, default=ScriptInterface.OneRunner)
    @property
    def get_interface_type(self):
        match self.interface_type:
            case Script.ScriptInterface.OneRunner:
                return _("Однокоммандный")
            case Script.ScriptInterface.CommandLineInterface:
                return _("Интерфейс коммандной строки")
            case Script.ScriptInterface.TerminalUserInterface:
                return _("Терминальный интерфейс")


@receiver(pre_save)
def _post_save_category_tool(sender, instance, **kwargs): 
    # Не регистрируем отправителя, значит нужно проверить инстанс
    if isinstance(instance, Tool):
        # Задаём соответствующую категорию, а если её нет, то создаём основу
        category, is_created = Category.objects.get_or_create(slug="tools")
        if is_created:
            category.name_ru = "Инструменты"
            category.name_en = "Tools"
            category.description_ru = "Описание инструментов"
            category.description_en = "Tools\' description"
            category.categry_name = "Tool"
            category.save()
        instance.category = category
        # Так же нужно создать соответствующую директорию для инструмента
        os.makedirs(os.path.join(S.MEDIA_ROOT, f'{instance.category.slug}', f'{instance.slug}'), exist_ok=True)

def similar_tools_changed(sender, **kwargs):
    ''' Определяет то, сколько похожих инструментов можно будет назначить'''
    if kwargs['instance'].similar.count() > Tool.max_similar:
        raise ValidationError("You can't assign more than three tools", code="invalid")

m2m_changed.connect(similar_tools_changed, sender=Tool.similar.through)


class Note(models.Model):
    ''' Модель для хранения заметок '''
    view_name = "note"
    title = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(max_length=512, blank=False, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    timeCreated = models.DateTimeField()
    timeUpdated = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        self.timeUpdated = timezone.now()
        if not self.timeCreated:
            self.timeCreated = timezone.now()
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Note)
def _post_save_category_note(sender, instance, **kwargs): 
    # Задаём соответствующую категорию, а если её нет, то создаём основу
    category, is_created = Category.objects.get_or_create(slug="notes")
    if is_created:
        category.name_ru = "Заметки"
        category.name_en = "Notes"
        category.description_ru = "Описание заметок"
        category.description_en = "Notes\' description"
        category.categry_name = "Note"
        category.save()
    instance.category = category

class ExternalVideo(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    video_id = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"{self.video_id}"

class ExternalPodcast(models.Model):
    objects = LangManager()
    langs = models.ManyToManyField('self', blank=True)
    lang_type = models.CharField(max_length=2, choices=LanguageType, null=True, default=LanguageType.LANG_TYPE_UNI)

    podcast_id = models.IntegerField(help_text="An ID for podcast", unique=True, blank=False)

    def __str__(self):
        return f"({self.lang_type}) {self.podcast_id}"

class ExternalPodcastEpisode(models.Model):
    podcast = models.ForeignKey(ExternalPodcast, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    podcast_episode_id = models.IntegerField(help_text="Ad ID for podcast's episode", unique=True, blank=False)
    podcast_url = models.URLField(help_text="Full source path to podcast episode", unique=True, blank=False)

    def __str__(self):
        return f"({self.podcast.lang_type}) {self.podcast_episode_id}"