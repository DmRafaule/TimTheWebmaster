from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'anonymous_user_name', 'type', 'timeCreated')
    list_display_links = ('user',)


admin.site.register(Comment, CommentAdmin)
