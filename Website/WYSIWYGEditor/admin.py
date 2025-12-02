from django.contrib import admin
from .models import PostTemplate


class PostTemplateAdmin(admin.ModelAdmin):
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': ['template']
            }
        ),
        (
            'Filled by form',
            {
                'fields': ['filename', 'content', 'used_styles', 'used_scripts',],
                'classes': ['collapse'],
            }
        ),
    ]
    list_display = (
        'filename',
        'timeCreated',
        'timeUpdated',
    )
    list_display_links = (
        'filename',
    )
    list_filter = ('timeCreated',)
    search_fields = (
        'filename',
    )

admin.site.register(PostTemplate, PostTemplateAdmin)