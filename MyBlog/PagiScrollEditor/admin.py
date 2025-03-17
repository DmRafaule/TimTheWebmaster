from django.contrib import admin
from .models import PagiScrollPage

class PagiScrollEditorAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ['regex_slug', 'title', 'description', 'h1', 'lead']
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


admin.site.register(PagiScrollPage, PagiScrollEditorAdmin)