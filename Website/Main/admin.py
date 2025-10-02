from django.contrib import admin
from .models import Website, Contact, Media#, Image, Downloadable


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
        'choosen_tools',
        'categories_to_display_on_side_menu', 
        'popular_articles_on_footer', 
        'popular_tools_on_footer',
        'my_resources_choosen_tags_on_home', 
        'other_articles_choosen_tags_on_home',
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
            'Post options',
            {
                'fields': [
                    'threshold_similar_articles', 
                    'threshold_related_termins', 
                    'threshold_related_questions',
                    'max_displayed_similar_articles',
                    'max_displayed_termins',
                    'max_displayed_questions'],
                'classes': ['collapsed'],
                'description': 'In this section you could change and edit options related to every Post object on website(Tool, Article, Category, Termin, Question)'
            }
        ),
        (
            'Post list options',
            {
                'fields': [
                    'paginator_per_page_posts',
                    'paginator_per_page_gallery',
                    'paginator_per_page_gallery_columns',
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
                    'choosen_tools',
                    'my_resources_choosen_tags_on_home',
                    'min_displayed_my_resources',
                    'other_articles_choosen_tags_on_home',
                    'min_displayed_other_articles',
                    (
                        'max_displayed_news_on_home',
                        'max_displayed_postSeries_on_home',
                        'max_displayed_images_on_home',
                        'max_displayed_inner_tools_on_home',
                        'max_displayed_td_on_home',
                        'max_displayed_qa_on_home',
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
                    'popular_articles_on_footer',
                    'popular_tools_on_footer',
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
