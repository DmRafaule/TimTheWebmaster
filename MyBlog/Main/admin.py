from django.contrib import admin
from .models import Image, Downloadable


class ImageAdmin(admin.ModelAdmin):
    exclude = ('text',)
    list_display = ('type', 'file')
    list_display_links = ('type',)
    list_editable = ('file',)


class DownloadableAdmin(admin.ModelAdmin):
    exclude = ('text',)
    list_display = ('type', 'file')
    list_display_links = ('type',)
    list_editable = ('file',)


admin.site.register(Downloadable, DownloadableAdmin)
admin.site.register(Image, ImageAdmin)
