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
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self, *args, **kwargs):
        print(args)
        print(kwargs)
        return reverse(f'articles-list')


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","post_list.html")
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


class Article(Post):
    view_name = "article"
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FileField(max_length=300, upload_to=user_directory_path, blank=False)  # page to display

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="articles")
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class News(Post):
    view_name = "news"
    headline = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    first_sentence = models.CharField(max_length=256, blank=False)
    lead = models.TextField(blank=False)
    body = models.TextField(blank=False, help_text="Render markdown")
    ending = models.TextField(blank=False, help_text="Render markdown")
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","news.html")
    )

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="news")
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline


class Case(Post):
    view_name = "case"
    title = models.CharField(max_length=256, blank=False)
    subtitle = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    resume = models.TextField(blank=False, help_text="Render markdown")
    client_name = models.CharField(max_length=256, blank=True)
    client_description = models.TextField(blank=True, help_text="Render markdown")
    goals = models.TextField(blank=False, help_text="Render markdown")
    solution = models.TextField(blank=False, help_text="Render markdown")
    result = models.TextField(blank=False, help_text="Render markdown")
    preview = models.ImageField(max_length=300, upload_to=user_directory_path, blank=True)
    additional = models.TextField(blank=True, help_text="Render markdown")

    template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","case.html")
    )

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="cases")
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class QA(Post):
    view_name = "qa"
    question = models.CharField(max_length=512, blank=False)
    description = models.TextField(blank=False)
    answer = models.TextField(blank=False, help_text="Render markdown")
    template = models.FilePathField(
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
    termin = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=False)
    definition = models.TextField(blank=False, help_text="Render markdown")
    template = models.FilePathField(
            path=os.path.join(S.BASE_DIR,"Post","templates","Post"),
            default=os.path.join(S.BASE_DIR,"Post","templates","Post","td.html")
    )

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="td")
        super(TD, self).save(*args, **kwargs)

    def __str__(self):
        return self.termin


class Tool(Post):
    view_name = "tool"
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=False)
    icon = models.FileField(max_length=300, upload_to=user_directory_path, blank=True)

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(slug="tools")
        super(Tool, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{get_language()}/tools/{self.slug}/'


class PostSitemap(Sitemap):
    i18n = True

    def items(self):
        articles = Article.objects.filter(isPublished=True)
        news = News.objects.filter(isPublished=True)
        cases = Case.objects.filter(isPublished=True)
        qa = QA.objects.filter(isPublished=True)
        td = TD.objects.filter(isPublished=True)
        tools = Tool.objects.filter(isPublished=True)
        items = list(chain(articles, news, cases, qa, td, tools))
        return items

    def lastmod(self, obj):
        return obj.timeUpdated


# Remove all loaded files before deleting on database
@receiver(pre_delete, sender=Post)
def cleanupPost(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(S.MEDIA_ROOT, f"{instance.category.slug}/{instance.slug}"))
