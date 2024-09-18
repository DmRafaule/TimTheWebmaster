from itertools import chain

from django.db import models
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
import os, shutil
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
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
    # Move them later to Article
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.timeUpdated = timezone.now()
        if not self.timeCreated:
            self.timeCreated = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(self.view_name, kwargs={"post_slug": self.slug})


class QA(Post):
    view_name = "qa"
    question = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=360, blank=False, help_text="To be used in meta tag - description")
    answer = models.TextField(max_length=360, blank=False)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=True, help_text="If provided, default template not in use")
    default_template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","qa.html")
    )

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
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=True, help_text="If provided, default template not in use")
    default_template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","td.html")
    )

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="td")
        super(TD, self).save(*args, **kwargs)

    def __str__(self):
        return self.termin
    

class Article(Post):
    view_name = "article"
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=False)  # page to display
    qas = models.ManyToManyField(QA, blank=True, help_text='You only use this field to pin actualy needed qas. Other will come automatically')
    tds = models.ManyToManyField(TD, blank=True, help_text='You only use this field to pin actualy needed tds. Other will come automatically')

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="articles")
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tool(Post):
    view_name = "tool"
    INTERNAL = 'In'
    EXTERNAL = 'Ex'
    ARCHIVE = 'Ac'
    TOOL_CATEGORIES = {
        INTERNAL:   'Internal',
        EXTERNAL:   'External',
        ARCHIVE:    'Archive',
    }
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    icon = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)
    url  = models.URLField(max_length=300, blank=True, help_text='Use only if it is External type')
    archive = models.FileField(upload_to=user_directory_path, blank=True, help_text='Use only if it is Archive type')
    type = models.CharField(max_length=2, choices=TOOL_CATEGORIES, default=ARCHIVE, blank=False)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="tools")
        os.makedirs(os.path.join(S.MEDIA_ROOT, f'{self.category.slug}', f'{self.slug}'), exist_ok=True)
        super(Tool, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = ''
        match self.type:
            case self.ARCHIVE:
                url = f'/media/{self.archive}'
            case self.INTERNAL:
                url = f'/{get_language()}/tools/{self.slug}/'
            case self.EXTERNAL:
                url = self.url

        return url


class PostSitemap(Sitemap):
    i18n = True

    def items(self):
        articles = Article.objects.filter(isPublished=True)
        qa = QA.objects.filter(isPublished=True)
        td = TD.objects.filter(isPublished=True)
        tools = Tool.objects.filter(isPublished=True, type=Tool.INTERNAL)
        items = list(chain(articles, qa, td, tools))
        return items

    def lastmod(self, obj):
        return obj.timeUpdated


# Remove all loaded files before deleting on database
@receiver(pre_delete, sender=Post)
def cleanupPost(sender, instance, **kwargs):
    path = os.path.join(S.MEDIA_ROOT, f"{instance.category.slug}", f"{instance.slug}")
    if os.path.exists(path):
        shutil.rmtree(path)
