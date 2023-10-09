from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('isPublished', 'id', 'name', 'type', 'slug', 'timeCreated', 'timeUpdated', 'preview', 'template', 'likes', 'shares', 'viewed')
    list_display_links = ('name',)
    list_editable = ('isPublished', 'likes', 'shares', 'viewed')
    list_filter = ('isPublished', 'timeUpdated', 'timeCreated', 'likes', 'shares', 'viewed')
    search_fields = ('name', 'tags')
    prepopulated_fields = {'slug': ("name",)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
