import os
from django.db import models
from django.utils.translation import get_language


def user_directory_path_forImageAndDownloadabel(instance, filename):
    ''' Для указания путя по сохранению файлов для постов типа Статей и инструментов 
    
    arguments:
    ----------
        instance: Объект модели Post
        filename: Имя файла для сохранения

    returns:
    --------
        Путь типа str до файла
    '''
    return "{0}/{1}/{2}".format(instance.type.category.slug, instance.type.slug, filename)


class Website(models.Model):
    ''' Модель для хранения глобальных конфигураций сайта '''
    class Meta:
         verbose_name = 'Website'
         verbose_name_plural = 'Website'
    # Имя конфигурации
    name = models.CharField(max_length=256, blank=False, unique=True)
    # Текущая ли конфигурация TODO: нужно сделать специальную функцию для автоматического переключения текущей конф.
    # То есть, только одна запись в этой модели может быть "текущей"
    is_current = models.BooleanField(default=False, help_text='Should be checked only for one record of Website databse')
    # Часть настроек для отображения постов
    NO_THRESHOLD = 1
    MINIMAL_THRESHOLD = 2
    TOLERATED_THRESHOLD = 3
    MAXIMAL_THRESHOLD = 5
    THRESHOLDS = {
        NO_THRESHOLD: 'No threshold (1)',
        MINIMAL_THRESHOLD: 'Minimal threshold (2)',
        TOLERATED_THRESHOLD: 'Tolerated threshold (3)',
        MAXIMAL_THRESHOLD: 'Maximal threshold (5)',
    }

    NO_DISPLAY = 0
    MINIMAL_DISPLAY = 2
    TOLERATED_DISPLAY = 3
    MAXIMAL_DISPLAY = 5
    MAX_DISPLAYS = {
        NO_DISPLAY: 'Do not display',
        MINIMAL_DISPLAY: 'Minimal display (2)',
        TOLERATED_DISPLAY: 'Tolerate display (3)',
        MAXIMAL_DISPLAY: 'Maximal display (5)',
    }
    # Часть настроек для отображения страниц пагинации 
    paginator_per_page_posts = models.IntegerField(verbose_name='Posts per page', default=4, blank=False, help_text='This field sets how many posts should be loaded while scrolling or paginating')
    # Общая часть настроек
    categories_to_display_on_side_menu = models.ManyToManyField('Post.Category', verbose_name='Categories to display on side menu', blank=False)
    contacts_for_orders = models.ManyToManyField('Main.Contact', verbose_name="Contacts to use for ordering", blank=True)

    # Домашняя часть настроек
    max_displayed_notes_on_home = models.IntegerField(verbose_name='Limit to display notes', default=5, blank=False)
    articles_post_preview = models.FileField(upload_to='common', blank=True)
    tools_post_preview = models.FileField(upload_to='common', blank=True)
    notes_post_preview = models.FileField(upload_to='common', blank=True)
    default_image_preview = models.FileField(upload_to='common', blank=True)

class Contact(models.Model):
    ''' Модель для хранения контактов автора этого сайта '''
    icon = models.FileField(upload_to='common/contacts', blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=512, blank=False)

class LanguageType(models.TextChoices):
    ''' Специальный класс для определения языка той или иной записи в БД '''

    LANG_TYPE_RU = 'ru'
    LANG_TYPE_EN = 'en'
    LANG_TYPE_UNI = 'XX' # Специальный тип, чтобы обозначить что запись в БД может быть отображена на всех языках 

class LangManager(models.Manager):
    ''' Класс менеджер для фильтрации записей в БД по языку '''

    def filter_by_lang(self):
        ''' Возвращает только те записи, которые универсальны для любого языка + записи на текущем языке сайта '''
        uni_records = self.filter(lang_type=LanguageType.LANG_TYPE_UNI)
        cur_lang_records = self.filter(lang_type=get_language())
        return uni_records | cur_lang_records

class Media(models.Model):
    ''' Модель для хранения файлов с разделением их по типу '''
    objects = LangManager()
    RAW_FILE = 1
    PDF = 2
    IMAGE = 3
    AUDIO = 4
    VIDEO = 5
    FILE_TYPE = {
        RAW_FILE: 'files',
        PDF: 'pdfs',
        IMAGE: 'images',
        AUDIO: 'audios',
        VIDEO: 'videos',
    }

    def media_save_to(instance, filename):
        ''' Для указания путя по сохранению файлов для постов типа Статей и инструментов 
        
        arguments:
        ----------
            instance: Объект модели Post
            filename: Имя файла для сохранения

        returns:
        --------
            Путь типа str до файла
        '''
        return f"{Media.FILE_TYPE[instance.type]}/{instance.lang_type}/{filename}"
    # Тип языка (Русский, Английский ...) 
    lang_type = models.CharField(max_length=2, choices=LanguageType, null=True, default=LanguageType.LANG_TYPE_UNI)
    # Те же файлы только на другом языке
    langs = models.ManyToManyField('self', blank=True)
    # Тип файла
    type = models.IntegerField(choices=FILE_TYPE, default=RAW_FILE, blank=False )
    file = models.FileField(upload_to=media_save_to, blank=False)
    text = models.CharField(max_length=250, blank=True)
    timeCreated = models.DateTimeField(default=None, null=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        ''' Получение абсолютного путя до файла  '''
        #TODO: импортируй из настроек 
        return '/media/{0}'.format(self.file)
    
    def get_filename(self):
        ''' Получить имя файла '''
        return os.path.basename(self.file.name)
    
    def __str__(self):
        also_in = ""
        for rel in self.langs.all():
            also_in += rel.lang_type + ','
        return f"({also_in})[{Media.FILE_TYPE[self.type].capitalize()}]{self.lang_type} -> {self.file}"

class CommonNotification(models.Model):
    regex_slug = models.CharField(max_length=512, blank=False, unique=True, help_text="A regex expression, which represents urls")
    message = models.TextField(max_length=256, blank=False, help_text="You can also use an HTML tags.")

    def __str__(self):
        return self.regex_slug