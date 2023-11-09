from django.contrib import admin
from .models import User, Response, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'email', 'password')
    list_filter = ('name', 'email')
    search_fields = ('name', 'tags', 'email')
    prepopulated_fields = {'slug': ("name",)}


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    list_display_links = ('user',)
    list_editable = ('content',)
    list_filter = ('user', 'tags')
    search_fields = ('user',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'email')
    list_display_links = ('name',)
    list_editable = ('content', 'email')
    search_fields = ('name', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Message, MessageAdmin)
