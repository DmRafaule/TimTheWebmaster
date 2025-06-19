import os

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

from MyBlog import settings as S
from Main.models import Media


def user_directory_path(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "{0}/{1}/{2}".format(instance.category.slug, instance.slug, filename)


class Tag(models.Model):
    slug = models.SlugField(unique=True, max_length=60, blank=False, default='')
    name = models.CharField(max_length=256, unique=True, blank=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self, *args, **kwargs):
        return reverse(f'articles-list')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    template = models.FilePathField(
        path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
        default=os.path.join(S.BASE_DIR,"Post","templates","Post","article_list.html")
    )
    categry_name = models.SlugField(max_length=50, unique=False, blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f'{self.slug}-list')

class Post(models.Model):
    view_name = "post"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    slug = models.SlugField(max_length=256, unique=True)
    timeCreated = models.DateTimeField()
    timeUpdated = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    media = models.ManyToManyField(Media, blank=True, help_text="Will be procceed only First ones added video, pdf, audio files. On Tool model audio and pdf files has no effect.")


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
    question = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    answer = models.TextField(max_length=360, blank=False)

    def __str__(self):
        return self.question

class Termin(models.Model):
    termin = models.CharField(max_length=60, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    definition = models.TextField(max_length=360,blank=False)

    def __str__(self):
        return self.termin
    
class Article(Post):
    view_name = "article"
    max_similar = 3
    title = models.CharField(max_length=256, blank=False, default='')
    h1 = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(max_length=256, blank=True)
    meta_keywords = models.CharField(max_length=256, blank=True, default='')
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=False)  # page to display
    questions = models.ManyToManyField(Question, blank=True, help_text='You only use this field to pin actualy needed qas. Other will come automatically')
    termins = models.ManyToManyField(Termin, blank=True, help_text='You only use this field to pin actualy needed tds. Other will come automatically')
    similar = models.ManyToManyField('self', blank=True, help_text="Up to 3 choises", symmetrical=False)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="articles")
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Platform(models.Model):
    name = models.CharField(max_length=256, blank=False)
    icon = models.FileField(blank=False, upload_to="common")

    def __str__(self):
        return self.name

class Tool(Post):
    view_name = "tool"
    max_similar = 3
    name = models.CharField(max_length=256, blank=False)
    h1 = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(blank=False)
    meta_keywords = models.CharField(max_length=256, blank=True, default='')
    icon = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=True, help_text="If provided, default template not in use. Use only if it is Internal default type")
    default_template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","tool.html")
    )
    platforms = models.ManyToManyField(Platform, blank=True)
    price = models.IntegerField(blank=True, default=0)
    similar = models.ManyToManyField('self', blank=True, help_text="Up to 3 choises", symmetrical=False)

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
        self.category = Category.objects.get(slug="tools")
        os.makedirs(os.path.join(S.MEDIA_ROOT, f'{self.category.slug}', f'{self.slug}'), exist_ok=True)
        super(Tool, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{get_language()}/tools/{self.slug}/'

def similar_articles_changed(sender, **kwargs):
    if kwargs['instance'].similar.count() > Article.max_similar:
        raise ValidationError("You can't assign more than three articles", code="invalid")

def similar_tools_changed(sender, **kwargs):
    if kwargs['instance'].similar.count() > Tool.max_similar:
        raise ValidationError("You can't assign more than three tools", code="invalid")

m2m_changed.connect(similar_articles_changed, sender=Article.similar.through)
m2m_changed.connect(similar_tools_changed, sender=Tool.similar.through)

class Note(models.Model):
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
        self.category = Category.objects.get(slug="notes")
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title