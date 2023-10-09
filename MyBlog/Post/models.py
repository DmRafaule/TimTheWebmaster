from django.db import models
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
import os, shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from MyBlog.settings import MEDIA_ROOT


def user_directory_path(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "{0}/{1}/{2}".format(instance.type, instance.slug, filename)


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=256, blank=False)
    type = models.CharField(max_length=50, blank=False)
    short_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=256, unique=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)
    isPublished = models.BooleanField(default=True)
    preview = models.ImageField(upload_to=user_directory_path, blank=True)
    template = models.FileField(upload_to=user_directory_path, blank=False)  # page to display
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.type, kwargs={"post_slug": self.slug})


class PostSitemap(Sitemap):
    i18n = True

    def items(self):
        return Post.objects.filter(isPublished=True)

    def lastmod(self, obj):
        return obj.timeUpdated


# Remove all loaded files before deleting on database
@receiver(pre_delete, sender=Post)
def cleanupPost(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(MEDIA_ROOT, f"{instance.type}/{instance.slug}"))
