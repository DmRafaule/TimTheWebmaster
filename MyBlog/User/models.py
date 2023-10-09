from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from Post.models import Post, Tag, user_directory_path
import os, shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from MyBlog.settings import MEDIA_ROOT


class User(models.Model):
    type = "users"
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, unique=True)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(type, kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(User, self).save(*args, **kwargs)


# Messages that displayed under Projects, Articles, News
class Comment(models.Model):
    content = models.TextField(blank=False)
    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)


# This is my ansver to Messages from guests and users
class Response(models.Model):
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    forAll = models.BooleanField(default=False)


# This is a questions or suggestions or offers for work or other types of matter.
class Message(models.Model):
    name = models.CharField(max_length=256, blank=True)
    content = models.TextField(blank=False)
    email = models.EmailField(blank=False)


# Remove all loaded files before deleting on database
@receiver(pre_delete, sender=User)
def cleanupUser(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(MEDIA_ROOT, f"{instance.type}/{instance.slug}"))
