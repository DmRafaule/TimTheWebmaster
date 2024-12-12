from django.contrib import admin
from .models import PostFilter

class PostFilterEditorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ['regex_slug', 'title', 'description', 'h1', 'lead', 'preview']
            }
        ),
    ]
    list_display = (
        'id',
        'title',
    )
    list_display_links = (
        'title',
    )
    search_fields = (
        'title',
    )


admin.site.register(PostFilter, PostFilterEditorAdmin)