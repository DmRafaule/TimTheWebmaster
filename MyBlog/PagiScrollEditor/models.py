from django.db import models


def filter_pages_path(instance, filename):
    return "filter_pages"

class PagiScrollPage(models.Model):
    regex_slug = models.CharField(max_length=512, blank=False, unique=True, help_text="A regex expression, which represents urls")
    preview = models.ImageField(max_length=300, upload_to=filter_pages_path ,blank=True)
    title = models.CharField(max_length=256, blank=True, default='', help_text="Will be used only if provided with description")
    h1 = models.CharField(max_length=256, blank=True, default='')
    description = models.TextField(max_length=256, blank=True, help_text="Will be used only if provided with title")
    lead = models.TextField(max_length=768, blank=True)