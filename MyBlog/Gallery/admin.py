from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('id', 'file', 'timeCreated', 'timeUpdated')
    list_display_links = ('id',)
    list_editable = ('file', 'timeCreated',)

admin.site.register(Image, ImageAdmin)
