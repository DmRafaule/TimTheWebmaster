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
    exclude = ('category', 'timeCreated', 'timeUpdated', 'name', 'description', 'definition')
    list_display = (
            'id',
            'name',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
            'icon'
    )
    list_display_links = (
            'name',
    )
    list_editable = (
            'isPublished',
            'timeCreated'
    )
    search_fields = (
            'name',
            'tags'
    )
    list_filter = ('isPublished',)


class ServiceAdmin(admin.ModelAdmin):
    exclude = ('category', 'timeCreated', 'timeUpdated', 'name', 'description', 'process', 'for_who', 'for_who_not', 'benefits', 'deadline')
    list_display = (
            'id',
            'name',
            'preview',
            'price',
            'deadline',
            'isPublished',
            'slug',
            'timeCreated',
            'timeUpdated',
    )
    list_display_links = (
            'name',
    )
    list_editable = (
            'preview',
            'price',
            'deadline',
            'isPublished',
            'timeCreated'
    )
    search_fields = (
            'name',
            'tags'
    )
    list_filter = ('isPublished',)


admin.site.register(M.Tag, TagAdmin)
admin.site.register(M.Category, CategoryAdmin)
admin.site.register(M.Article, ArticleAdmin)
admin.site.register(M.News, NewsAdmin)
admin.site.register(M.Case, CaseAdmin)
admin.site.register(M.QA, QAAdmin)
admin.site.register(M.TD, TDAdmin)
admin.site.register(M.Service, ServiceAdmin)
admin.site.register(M.Tool, ToolAdmin)
