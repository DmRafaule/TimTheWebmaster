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
    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.ImageField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)


class Downloadable(models.Model):
    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.FileField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)


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
