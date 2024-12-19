from django.contrib import admin
from .models import Comment, Interaction


class CommentAdmin(admin.ModelAdmin):
    list_display = ('url', 'name', 'time_published')
    list_display_links = ('url',)
    list_editable = ('name',)
    search_fields = ('url', 'name')
    ordering = ['-time_published']
    fieldsets = [
        (
            None,
            {
                'fields': ['url', 'name', 'message', 'interaction']
            }
        ),
    ]

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('url', 'views', 'likes', 'shares', 'comments', 'bookmarks')
    list_display_links = ('url',)
    list_editable = ( 'views', 'likes', 'shares', 'comments', 'bookmarks')
    search_fields = ('slug',)
    fieldsets = [
        (
            None,
            {
                'fields': ['url', ('views', 'likes', 'shares', 'comments', 'bookmarks')]
            }
        ),
    ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Interaction, InteractionAdmin)