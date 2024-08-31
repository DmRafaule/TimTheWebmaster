from itertools import chain
from django.db import models
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
import os, shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from Post.models import Article
from Main.models import Image as ImagesMain
from MyBlog.settings import MEDIA_ROOT


def galleryFolder(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "gallery/{0}".format(filename)


class Image(models.Model):
    file = models.ImageField(upload_to=galleryFolder, blank=False)
    text = models.CharField(max_length=250, blank=True)
    tags = models.ManyToManyField('Post.Tag', blank=True)
    timeCreated = models.DateTimeField()
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/media/{0}'.format(self.file)


class ImagesSitemap(Sitemap):
    def items(self):
        images_in_gallery = Image.objects.all()
        common_images = ImagesMain.objects.filter(category=ImagesMain.ART)
        # Get all previews in articles
        images_in_post_previews = []
        for post in Article.objects.exclude(preview=''):
            images_in_post_previews.append(Image(file=post.preview, text=''))
        images = list(chain(images_in_gallery, common_images, images_in_post_previews))
        return images

    def lastmod(self, obj):
        return obj.timeUpdated


# Remove loaded file before deleting on database
@receiver(pre_delete, sender=Image)
def deleteImage(sender, instance, **kwargs):
    os.remove(os.path.join(MEDIA_ROOT, f"{instance.file}"))
