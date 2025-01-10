import os, shutil
from django.db import models
from django.contrib.auth.models import User
from MyBlog import settings as S
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class PostTemplate(models.Model):
    ROOT_DIR = 'post-editor'
    RAW = 0
    ARTICLE_POST = 1
    TERMIN_POST = 2
    QUESTION_POST = 3
    TOOL_POST = 4
    OPTIONS = {
        RAW: _('Чистый HTML'),
        ARTICLE_POST: _('Для статей'),
        TERMIN_POST: _('Для определений'),
        QUESTION_POST: _('Для вопросов'),
        TOOL_POST: _('Для инструментов'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.FilePathField(
        path=os.path.join(S.MEDIA_ROOT, 'tools', ROOT_DIR),
    )
    timeCreated = models.DateTimeField(auto_created=True, auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=100)
    option = models.IntegerField(choices=OPTIONS, default=RAW)
    content = models.TextField(blank=True)
    used_styles = models.TextField(blank=True)
    used_scripts = models.TextField(blank=True)


# Remove all loaded files before deleting on database
@receiver(pre_delete, sender=PostTemplate)
def cleanupPost(sender, instance, **kwargs):
    path = os.path.join(S.MEDIA_ROOT, "tools", PostTemplate.ROOT_DIR, f"{instance.filename}")
    if os.path.exists(path):
        os.remove(path)