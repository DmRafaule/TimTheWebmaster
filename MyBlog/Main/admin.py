from django.contrib import admin
from .models import Image, Downloadable


class ImageAdmin(admin.ModelAdmin):
    exclude = ('text',)
    list_display = ('id', 'type', 'file', 'category', 'timeCreated', 'timeUpdated')
    list_display_links = ('type',)
    list_editable = ('file', 'category')


class DownloadableAdmin(admin.ModelAdmin):
    exclude = ('text',)
    list_display = ('id', 'type', 'file', 'category', 'timeCreated', 'timeUpdated')
    list_display_links = ('type',)
    list_editable = ('file','category')


admin.site.register(Downloadable, DownloadableAdmin)
admin.site.register(Image, ImageAdmin)
