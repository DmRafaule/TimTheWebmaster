from django.contrib import admin
import Post.models as M



class TagAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'name'
    )
    list_display_links = (
            'id',
            'name'
    )
    search_fields = ('name',)


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
    exclude = ('category', 'timeCreated', 'timeUpdated', 'template', 'description', 'title')
    filter_horizontal = ('tags',)
    list_display = (
            'id',
            'title',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
            'preview',
    )
    list_display_links = (
            'title',
    )
    list_editable = (
            'isPublished',
            'timeCreated',
            'preview'
    )
    list_filter = ('isPublished',)
    search_fields = (
            'title',
            'tags'
    )


class NewsAdmin(admin.ModelAdmin):
    exclude = ('category', 'timeCreated', 'timeUpdated', 'headline', 'description', 'first_sentence', 'lead', 'body', 'ending')
    list_display = (
            'id',
            'headline',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
            'preview',
    )
    list_display_links = (
            'headline',
    )
    list_editable = (
            'isPublished',
            'timeCreated',
            'preview',
    )
    search_fields = (
            'headline',
            'tags'
    )
    list_filter = ('isPublished',)


class CaseAdmin(admin.ModelAdmin):
    exclude = ('category', 'timeCreated', 'timeUpdated', 'additional', 'result', 'description', 'solution', 'goals', 'client_description', 'client_name', 'resume', 'subtitle', 'title')
    list_display = (
            'id',
            'title',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
            'preview',
    )
    list_display_links = (
            'title',
    )
    list_editable = (
            'isPublished',
            'timeCreated',
            'preview',
    )
    search_fields = (
            'title',
            'tags'
    )
    list_filter = ('isPublished',)


class QAAdmin(admin.ModelAdmin):
    exclude = ('category', 'timeCreated', 'timeUpdated', 'question', 'answer', 'description', )
    list_display = (
            'id',
            'question',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
    )
    list_display_links = (
            'question',
    )
    list_editable = (
            'isPublished',
            'timeCreated',
    )
    search_fields = (
            'question',
            'tags'
    )
    list_filter = ('isPublished',)


class TDAdmin(admin.ModelAdmin):
    exclude = ('category', 'timeCreated', 'timeUpdated', 'termin', 'description', 'definition')
    filter_horizontal = ('tags',)
    list_display = (
            'id',
            'termin',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
    )
    list_display_links = (
            'termin',
    )
    list_editable = (
            'isPublished',
            'timeCreated',
    )
    search_fields = (
            'termin',
            'tags'
    )
    list_filter = ('isPublished',)


class ToolAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ['name_ru', 'name_en', 'description_ru', 'description_en', 'slug', 'isPublished']
            }
        ),
        (
            'Advanced options',
            {
                'fields': ['type', 'icon', 'archive', 'url', 'tags'],
                'classes': ['collapse'],
                'description': 'In this fieldset you can switch type of tool and configure other options.'
            }
        )
    ]
    exclude = ('category', 'timeCreated', 'timeUpdated', 'name', 'description', 'definition', 'likes', 'shares', 'viewed')
    filter_horizontal = ('tags',)
    list_display = (
            'id',
            'name',
            'description',
            'isPublished',
            'icon',
            'type',
            'url',
            'archive',
    )
    list_display_links = (
            'name',
    )
    list_editable = (
            'isPublished',
            'description',
            'icon',
            'type',
            'url',
            'archive'
    )
    search_fields = (
            'name',
            'tags'
    )
    radio_fields = {'type': admin.HORIZONTAL}
    list_filter = ('isPublished', 'type')


admin.site.register(M.Tag, TagAdmin)
admin.site.register(M.Category, CategoryAdmin)
admin.site.register(M.Article, ArticleAdmin)
admin.site.register(M.News, NewsAdmin)
admin.site.register(M.Case, CaseAdmin)
admin.site.register(M.QA, QAAdmin)
admin.site.register(M.TD, TDAdmin)
admin.site.register(M.Tool, ToolAdmin)
