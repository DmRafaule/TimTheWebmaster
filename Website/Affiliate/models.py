from django.db import models

from Main.models import Media, LangManager, LanguageType
from Post.models import Tag, Post


class AffiliateLink(models.Model):
    objects = LangManager()
    # Тип языка (Русский, Английский ...) 
    lang_type = models.CharField(max_length=2, choices=LanguageType, null=True, default=LanguageType.LANG_TYPE_UNI)
    # Те же файлы только на другом языке
    langs = models.ManyToManyField('self', blank=True)
    brand_name = models.CharField(max_length=100, blank=False, null=True)
    brand_logo = models.ForeignKey(Media, on_delete=models.CASCADE, blank=False)
    brand_description = models.TextField(max_length=500, blank=False, null=True)
    brand_link = models.URLField(blank=False, null=True)

    def __str__(self):
        also_in = ""
        for rel in self.langs.all():
            also_in += rel.lang_type + ','
        return f"({also_in}){self.lang_type} -> {self.brand_name}"

class AffiliateLinkConnection(models.Model):
    affiliate =  models.ForeignKey(AffiliateLink, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.affiliate}"

class AffiliateLinkConnectionTag(AffiliateLinkConnection):
    tags = models.ManyToManyField(Tag, blank=False)

    def __str__(self):
        name = ""
        for tag in self.tags.all():
            name += tag.name + "::"
        return f"{name} -> {self.affiliate}"

class AffiliateLinkConnectionSlug(AffiliateLinkConnection):
    slugs = models.ManyToManyField(Post, blank=False)

    def __str__(self):
        name = ""
        for slug in self.slugs.all():
            name += slug.slug + "::"
        return f"{name} -> {self.affiliate}"

class AffiliateLinkConnectionSpecial(AffiliateLinkConnection):
    class SpecialPages(models.TextChoices):
        NONE = "None"
        HOME = "Home page"
        ABOT = "About page"
    special = models.CharField(max_length=50, choices=SpecialPages, default=SpecialPages.NONE, blank=False)

    def __str__(self):
        return f"{self.special} -> {self.affiliate}"
    