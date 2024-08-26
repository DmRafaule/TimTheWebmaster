from django.db import models
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from Post.models import Post
import os, shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from MyBlog.settings import MEDIA_ROOT


def user_directory_path_forImageAndDownloadabel(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "{0}/{1}/{2}".format(instance.type.category.slug, instance.type.slug, filename)


class Image(models.Model):
    ART = 'Ar'
    RESOURCE = 'Re'
    IMAGE_CATEGORIES = {
        ART: "Art",
        RESOURCE: "Resource"
    }
    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.ImageField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)
    category = models.CharField(max_length=2, choices=IMAGE_CATEGORIES, default=RESOURCE, blank=True)
    timeCreated = models.DateTimeField(auto_now=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/media/{0}'.format(self.file)


class Downloadable(models.Model):
    VIDEO = 'Vi'
    SCRIPT = 'Sc'
    ARCHIVE = 'Ac'
    TG_BOT = 'Tb'
    PARSER = 'Pr'
    DOWNLOADABLE_CATEGORIES = {
        VIDEO: "Video",
        SCRIPT: "Script",
        ARCHIVE: "Archive",
        TG_BOT: "Telegram bot",
        PARSER: "Parser",
    }

    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.FileField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)
    category = models.CharField(max_length=2, choices=DOWNLOADABLE_CATEGORIES, default=ARCHIVE, blank=True)
    timeCreated = models.DateTimeField(auto_now=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/media/{0}'.format(self.file)

class VideosSitemap(Sitemap):
    def items(self):
        videos = Downloadable.objects.filter(category=Downloadable.VIDEO)
        return list(videos)

    def lastmod(self, obj):
        return obj.timeUpdated

class StaticSitemap(Sitemap):
    i18n = True

    def items(self):
        return ["about", "contacts", "home"]

    def location(self, item):
        return reverse(item)


# Remove loaded file before deleting on database
@receiver(pre_delete, sender=Image)
def deleteImage(sender, instance, **kwargs):
    os.remove(os.path.join(MEDIA_ROOT, f"{instance.file}"))


# Remove loaded file before deleting on database
@receiver(pre_delete, sender=Downloadable)
def deleteDownloadable(sender, instance, **kwargs):

    os.remove(os.path.join(MEDIA_ROOT, f"{instance.file}"))
