from django.contrib import admin
from .models import Website, Contact, Media, CommonNotification


class ContactAdmin(admin.ModelAdmin):
    exclude = ('name', 'description')
    list_display = ('name_en', 'url')
    list_display_links = ('name_en',)
    search_fields = (
        'name_en',
    )
    fieldsets = [
        (
            None,
            {
                'fields': [('name_ru', 'name_en', 'url', 'icon'), ('description_ru', 'description_en')]
            }
        )
    ]

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('is_current', 'name')
    list_display_links = ('name',)
    filter_horizontal = (
        'categories_to_display_on_side_menu', 
        'contacts_for_orders',
    )
    search_fields = (
        'name',
    )
    fieldsets = [
        (
            None,
            {
                'fields': ['name', 'is_current']
            }
        ),
        (
            'Post list options',
            {
                'fields': [
                    'paginator_per_page_posts',
                    'articles_post_preview',
                    'tools_post_preview',
                    'notes_post_preview',
                ],
                'classes': ['collapsed'],
                'description': 'In this section you could change and edit options related to every paginator page, where you can find all of the Post object like: (Tool, Article, Category, Termin, Question)'
            }
        ),
        (
            'Home page',
            {
                'fields': [
                    (
                        'max_displayed_notes_on_home',
                    )
                ],
                'classes': ['collapsed'],
                'description': 'In this section you could change and edit options related home page'
            }
        ),
        (
            'Common data',
            {
                'fields': [
                    'categories_to_display_on_side_menu',
                    'contacts_for_orders',
                    'default_image_preview',
                ],
                'classes': ['collapsed'],
                'description': 'In this section you could change and edit options related to any blocks and elements on website that present on every page, like: side menu or footer'
            }
        )
    ]

class MediaAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'langs',
    )
    search_fields = (
        'file',
    )
    list_filter = ('lang_type', 'type')
    list_display = ('id', 'lang_type', 'type', 'file', 'timeCreated', 'timeUpdated')
    list_display_links = ('file',)
    list_editable = ('lang_type','type', 'timeCreated')
    fieldsets = [
        (
            None,
            {
                'fields': [('lang_type', 'type'), 'langs', 'file', 'text', 'timeCreated']
            }
        ),
    ]



admin.site.register(Website, WebsiteAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(CommonNotification, admin.ModelAdmin)
