import os

from django.db import models
from django.urls import reverse
from django.utils.translation import get_language

from MyBlog import settings as S
from django.utils import timezone


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

    def save(self, *args, **kwargs):
        self.timeUpdated = timezone.now()
        if not self.timeCreated:
            self.timeCreated = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(self.view_name, kwargs={"post_slug": self.slug})

    def __str__(self):
        return self.slug

class QA(Post):
    view_name = "qa"
    question = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    answer = models.TextField(max_length=360, blank=False)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="qa")
        super(QA, self).save(*args, **kwargs)

    def __str__(self):
        return self.question


class TD(Post):
    view_name = "td"
    termin = models.CharField(max_length=60, blank=False)
    key_phrases = models.CharField(max_length=254, blank=True, help_text="To be used to search place for inserting a link. Use , as separator.")
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    definition = models.TextField(max_length=360,blank=False)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="td")
        super(TD, self).save(*args, **kwargs)

    def __str__(self):
        return self.termin
    

class Article(Post):
    view_name = "article"
    title = models.CharField(max_length=256, blank=False, default='')
    h1 = models.CharField(max_length=256, blank=False, default='')
    description = models.TextField(max_length=256, blank=True)
    meta_keywords = models.CharField(max_length=256, blank=True, default='')
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=False)  # page to display
    qas = models.ManyToManyField(QA, blank=True, help_text='You only use this field to pin actualy needed qas. Other will come automatically')
    tds = models.ManyToManyField(TD, blank=True, help_text='You only use this field to pin actualy needed tds. Other will come automatically')

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="articles")
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Platform(models.Model):
    name = models.CharField(max_length=256, blank=False)
    icon = models.FileField(blank=False)

    def __str__(self):
        return self.name


class Tool(Post):
    view_name = "tool"
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    icon = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=True, help_text="If provided, default template not in use. Use only if it is Internal default type")
    default_template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","tool.html")
    )
    platforms = models.ManyToManyField(Platform, blank=True)
    price = models.IntegerField(blank=True, default=0)

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
        self.category = Category.objects.get(slug="notes")
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title