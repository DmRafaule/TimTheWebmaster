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
    exclude = ('category', 'template', 'description', 'title')
    filter_horizontal = ('tags', )
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': ['slug', 'isPublished', ('title_ru', 'title_en'), ('description_ru', 'description_en'), ('template_ru', 'template_en')]
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['preview', ('likes', 'shares', 'viewed'), 'timeCreated'],
                'classes': ['collapse'],
                'description': 'In this fieldset you can switch type of tool and configure other options.'
            }
        ),
        (
            'Relations',
            {
                'fields': ['tags', ],
                'classes': ['collapse'],
                'description': 'In this fieldset you can link this article to others post models (TD, QA, Tags)'
            }
        )
    ]
    list_display = (
        'slug',
        'isPublished',
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'isPublished',
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    list_filter = ('isPublished', 'timeCreated')
    search_fields = (
        'title_ru',
        'title_en',
        'description_ru',
        'description_en',
    )


class QAAdmin(admin.ModelAdmin):
    exclude = ('category', 'question', 'answer', 'description', 'template')
    ordering = ['-timeCreated']
    filter_horizontal = ('tags',)
    fieldsets = [
        (
            None,
            {
                'fields': ['slug', 'isPublished', ('question_ru', 'question_en'),('answer_ru', 'answer_en')]
            }
        ),
        (
            'Advanced options',
            {
                'fields': [('template_ru', 'template_en'), 'description_ru', 'description_en', 'tags', 'timeCreated'],
                'classes': ['collapse']
            }
        )
    ]
    list_display = (
        'isPublished',
        'slug',
        'question_ru',
        'question_en',
        'answer_ru',
        'answer_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'question_ru',
        'question_en',
        'answer_ru',
        'answer_en',
        'isPublished',
        'timeCreated',
    )
    search_fields = (
        'question_ru',
        'question_en',
    )
    list_filter = ('isPublished', 'timeCreated')


class TDAdmin(admin.ModelAdmin):
    exclude = ('category', 'termin', 'description', 'definition', 'template', 'key_phrases',)
    ordering = ['-timeCreated']
    filter_horizontal = ('tags',)
    fieldsets = [
        (
            None,
            {
                'fields': ['slug', 'isPublished', ('termin_ru', 'termin_en'),('definition_ru', 'definition_en'), ('key_phrases_ru', 'key_phrases_en')]
            }
        ),
        (
            'Advanced options',
            {
                'fields': [('template_ru', 'template_en'), 'description_ru', 'description_en', 'tags', 'timeCreated'],
                'classes': ['collapse']
            }
        )
    ]
    list_display = (
        'isPublished',
        'slug',
        'termin_ru',
        'termin_en',
        'definition_ru',
        'definition_en',
        'key_phrases_ru',
        'key_phrases_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'termin_ru',
        'termin_en',
        'definition_ru',
        'definition_en',
        'key_phrases_ru',
        'key_phrases_en',
        'isPublished',
        'timeCreated',
    )
    search_fields = (
        'termin_ru',
        'termin_en',
    )
    list_filter = ('isPublished', 'timeCreated')


class ToolAdmin(admin.ModelAdmin):
    exclude = ('category','name', 'description', 'likes', 'shares', 'viewed')
    filter_horizontal = ('tags',)
    ordering = ['-timeCreated']
    fieldsets = [
        (
            None,
            {
                'fields': ['slug', 'isPublished', ('name_ru', 'name_en'), ('description_ru', 'description_en')]
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['type', ('icon', 'archive', 'url'), 'tags', 'timeCreated'],
                'classes': ['collapse'],
                'description': 'In this fieldset you can switch type of tool and configure other options.'
            }
        )
    ]
    list_display = (
        'slug',
        'isPublished',
        'type',
        'name_ru',
        'name_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    list_display_links = (
        'slug',
    )
    list_editable = (
        'isPublished',
        'name_ru',
        'name_en',
        'description_ru',
        'description_en',
        'timeCreated',
        'type',
    )
    search_fields = (
        'name_ru',
        'name_en',
        'tags'
    )
    radio_fields = {'type': admin.HORIZONTAL}
    list_filter = ('isPublished', 'type', 'timeCreated')


admin.site.register(M.Tag, TagAdmin)
admin.site.register(M.Category, CategoryAdmin)
admin.site.register(M.Article, ArticleAdmin)
admin.site.register(M.QA, QAAdmin)
admin.site.register(M.TD, TDAdmin)
admin.site.register(M.Tool, ToolAdmin)
