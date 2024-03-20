from django.contrib import admin
from .models import Feed

# Register your models here.
class FeedAdmin(admin.ModelAdmin):
    list_display = (
            'group',
            'source',
            'date_updated'
    )
    list_display_links = ('source',)
    list_editable = ('group',)
    search_fields = ('group',)

admin.site.register(Feed, FeedAdmin)