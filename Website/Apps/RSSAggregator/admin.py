from django.contrib import admin
from .models import Feed, FeedGroup, FeedId


class FeedIdAdmin(admin.ModelAdmin):
    list_display = (
            'user_id',
    )
    list_display_links = ('user_id',)

class FeedGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('feeds',)
    list_display = (
            'user_id',
            'is_common',
            'name',
            'date_updated'
    )
    list_display_links = ('user_id',)
    list_editable = ('name', 'is_common')
    search_fields = ('name',)

class FeedAdmin(admin.ModelAdmin):
    list_display = (
            'user_id',
            'name',
            'feed',
            'date_updated'
    )
    list_display_links = ('user_id',)
    list_editable = ('name', 'feed')
    search_fields = ('name', 'feed')

admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedGroup, FeedGroupAdmin)
admin.site.register(FeedId, FeedIdAdmin)