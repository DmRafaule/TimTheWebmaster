from django.db import models
from django.utils.translation import gettext_lazy as _


class PostTemplate(models.Model):
    ROOT_DIR = 'wysiwyg-editor'
    template = models.FilePathField(
        path=f'./media/tools/{ROOT_DIR}',
    )
    timeCreated = models.DateTimeField(auto_created=True, auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    used_styles = models.TextField(blank=True)
    used_scripts = models.TextField(blank=True)
