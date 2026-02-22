from django.contrib import admin
import Post.models as M



class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_ru": ("name_ru",), "slug_en": ("name_en",)}
    exclude = ('name', 'slug')
    list_display = (
            'slug_ru',
            'slug_en',
            'name_ru',
            'name_en'
    )
    list_display_links = (
            'slug_ru',
    )
    search_fields = ('name_ru', 'name_en',)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('name', 'description')
    list_display = (
            'name',
            'slug',
            'description'
    )
    list_display_links = ('name',)
    list_editable = ('description',)
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):

    #def formfield_for_manytomany(self, db_field, request, **kwargs):     
    #    if db_field.name == "similar":
    #        id = int(request.resolver_match.kwargs['object_id'])
    #        category_id = db_field.model.objects.get(id=id).category.id
    #        kwargs["queryset"] = M.Article.objects.filter(category=category_id)
    #    return super(ArticleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    exclude = ('category', 'template', 'description', 'title', 'h1', 'meta_keywords')
    filter_horizontal = ('tags', 'termins', 'questions', 'similar', 'media' )
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': [('title_ru', 'title_en'), ('h1_ru', 'h1_en'), ('description_ru', 'description_en'), ('meta_keywords_ru', 'meta_keywords_en'), ('template_ru', 'template_en'), 'slug', 'isPublished']
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['media', ('preview', 'timeCreated')],
                'classes': ['collapse'],
                'description': 'In this fieldset you can switch type of tool and configure other options.'
            }
        ),
        (
            'Relations',
            {
                'fields': ['tags', 'similar', 'termins', 'questions'],
                'classes': ['collapse'],
                'description': 'In this fieldset you can link this article to others post models (Termin, Question, Tags)'
            }
        )
    ]
    list_display = (
        'slug',
        'isPublished',
        'title_ru',
        'title_en',
        'h1_ru',
        'h1_en',
        'description_ru',
        'description_en',
        'meta_keywords_ru',
        'meta_keywords_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'isPublished',
        'title_ru',
        'title_en',
        'h1_ru',
        'h1_en',
        'description_ru',
        'description_en',
        'meta_keywords_ru',
        'meta_keywords_en',
        'timeCreated',
    )
    list_filter = ('isPublished', 'timeCreated')
    search_fields = (
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
    )


class ToolAdmin(admin.ModelAdmin):
    exclude = ('category','name', 'description', 'template', 'h1', 'meta_keywords')
    filter_horizontal = ('tags', 'media', 'similar')
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': ['slug', 'isPublished', ('name_ru', 'name_en'), ('h1_ru', 'h1_en'), ('description_ru', 'description_en'), ('meta_keywords_ru', 'meta_keywords_en'), 'timeCreated']
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['icon', 'type', 'media', ('template_ru', 'template_en')],
                'classes': ['collapse'],
                'description': 'In this fieldset you can switch type of tool and configure other options.'
            }
        ),
        (
            'Relations',
            {
                'fields': ['tags', 'similar'],
                'classes': ['collapse'],
                'description': 'Fieldset for setting up relationship'
            }
        )
    ]
    list_display = (
        'slug',
        'isPublished',
        'type',
        'name_ru',
        'name_en',
        'h1_ru',
        'h1_en',
        'description_ru',
        'description_en',
        'meta_keywords_ru',
        'meta_keywords_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'isPublished',
        'type',
        'name_ru',
        'name_en',
        'h1_ru',
        'h1_en',
        'description_ru',
        'description_en',
        'meta_keywords_ru',
        'meta_keywords_en',
        'timeCreated',
    )
    search_fields = (
        'name_ru',
        'name_en',
        'tags'
    )
    list_filter = ('isPublished', 'timeCreated', 'type')

class WebappAdmin(ToolAdmin):
     fieldsets = [
        *ToolAdmin.fieldsets,
        (
            'TooltypeSpecific',
            {
                'fields': ['landscape_preview',]
            }
        ),
    ]

class TelegramBotAdmin(ToolAdmin):
     fieldsets = [
        *ToolAdmin.fieldsets,
        (
            'TooltypeSpecific',
            {
                'fields': ['bot_name', 'bot_type', 'bot_qr']
            }
        ),
    ]

class ScraperAdmin(ToolAdmin):
     exclude = ('target', *ToolAdmin.exclude)
     fieldsets = [
        *ToolAdmin.fieldsets,
        (
            'TooltypeSpecific',
            {
                'fields': [('target_en', 'target_ru'), 'how_many_threads', 'what_type', 'language_used', 'with_proxies', 'with_swapping']
            }
        ),
    ]

class ScriptAdmin(ToolAdmin):
     fieldsets = [
        *ToolAdmin.fieldsets,
        (
            'TooltypeSpecific',
            {
                'fields': ['most_valuable_action', 'interface_type']
            }
        ),
    ]

class DjangoAppAdmin(ToolAdmin):
    filter_horizontal = ('use_cases', *ToolAdmin.filter_horizontal)
    fieldsets = [
        *ToolAdmin.fieldsets,
        (
            'TooltypeSpecific',
            {
                'fields': ['use_cases', 'app_type']
            }
        ),
    ]


class NoteAdmin(admin.ModelAdmin):
    exclude = ('category','title', 'description')
    filter_horizontal = ('tags',)
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': [('title_ru', 'title_en'), ('description_ru', 'description_en'), 'isPublished']
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['tags', 'timeCreated'],
                'classes': ['collapse'],
            }
        )
    ]
    list_display = (
        'id',
        'isPublished',
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    list_display_links = (
        'id',
    )
    list_editable = (
        'isPublished',
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    search_fields = (
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
        'tags'
    )

class ExternalVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_id')
    list_display_links = ('id',)
    list_editable = ('video_id',)

class ExternalPodcastAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'langs',
    )
    list_filter = ('lang_type',)
    list_display = ('id', 'lang_type', 'podcast_id')
    list_display_links = ('podcast_id',)
    list_editable = ('lang_type',)
    fieldsets = [
        (
            None,
            {
                'fields': ['lang_type', 'langs', 'podcast_id']
            }
        ),
    ]

class ExternalPodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'podcast_episode_id', 'podcast', 'podcast_url', 'related_post')
    list_display_links = ('podcast_episode_id',)
    list_editable = ('podcast_url',)


admin.site.register(M.Tag, TagAdmin)
admin.site.register(M.Category, CategoryAdmin)
admin.site.register(M.Article, ArticleAdmin)
admin.site.register(M.WebTool, WebappAdmin)
admin.site.register(M.TelegramBot, TelegramBotAdmin)
admin.site.register(M.Scraper, ScraperAdmin)
admin.site.register(M.Script, ScriptAdmin)
admin.site.register(M.DjangoApp, DjangoAppAdmin)
admin.site.register(M.Note, NoteAdmin)
admin.site.register(M.ExternalPodcast, ExternalPodcastAdmin)
admin.site.register(M.ExternalPodcastEpisode, ExternalPodcastEpisodeAdmin)
admin.site.register(M.ExternalVideo, ExternalVideoAdmin)