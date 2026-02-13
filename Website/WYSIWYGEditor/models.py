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

    class PostType(models.IntegerChoices):
        Article = 1, "article_exmpl.html"
        Tool    = 2, "tool_exmpl.html"
        Note    = 3, "note_exmpl.html"
    post_type = models.IntegerField(default=PostType.Article, choices=PostType.choices)