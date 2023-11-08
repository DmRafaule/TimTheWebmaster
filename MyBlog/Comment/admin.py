from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'anonymous_user_name', 'type', 'timeCreated', 'content')
    list_display_links = ('user', 'anonymous_user_name',)
    list_editable = ('content',)
    list_filter = ('user', 'type', 'anonymous_user_name')
    search_fields = ('user', 'type', 'anonymous_user_name')


admin.site.register(Comment, CommentAdmin)
