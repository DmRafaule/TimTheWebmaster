from django.contrib import admin
from .models import Comment, Interaction, Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_display_links = ('email',)
    search_fields = ('email',)

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
                'fields': ['url', 'rating', 'name', 'message', 'interaction']
            }
        ),
    ]

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('url', 'time_updated', 'views', 'likes', 'shares', 'comments', 'bookmarks')
    ordering = ['-time_updated']
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


admin.site.register(Email, EmailAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Interaction, InteractionAdmin)