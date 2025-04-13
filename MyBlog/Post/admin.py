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
    filter_horizontal = ('tags', 'termins', 'questions' )
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
                'fields': ['preview', 'timeCreated'],
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


class QAAdmin(admin.ModelAdmin):
    exclude = ('question', 'answer', 'description')
    fieldsets = [
        (
            None,
            {
                'fields': [('question_ru', 'question_en'), ('description_ru', 'description_en'),('answer_ru', 'answer_en')]
            }
        ),
    ]
    list_display = (
        'question_ru',
        'question_en',
        'answer_ru',
        'answer_en',
    )
    list_display_links = (
        'question_ru',
    )
    list_editable = (
        'question_en',
        'answer_ru',
        'answer_en',
    )
    search_fields = (
        'question_ru',
        'question_en',
    )


class TDAdmin(admin.ModelAdmin):
    exclude = ('termin', 'description', 'definition',)
    fieldsets = [
        (
            None,
            {
                'fields': [('termin_ru', 'termin_en'), ('definition_ru', 'definition_en'), ('description_ru', 'description_en'),]
            }
        ),
    ]
    list_display = (
        'termin_ru',
        'termin_en',
        'definition_ru',
        'definition_en',
    )
    list_display_links = (
        'termin_ru',
    )
    list_editable = (
        'termin_en',
        'definition_ru',
        'definition_en',
    )
    search_fields = (
        'termin_ru',
        'termin_en',
    )


class PlatformAdmin(admin.ModelAdmin):
    exclude = ('name',)
    fieldsets = [
        (
            None,
            {
                'fields': ['icon', ('name_ru', 'name_en')]
            }
        ),
    ]
    list_display = (
        'name_ru',
        'name_en',
        'icon'
    )
    list_display_links = (
        'name_en',
    )
    list_editable = (
        'name_ru',
        'icon'
    )
    search_fields = (
        'name_ru',
        'name_en',
    )

class ToolAdmin(admin.ModelAdmin):
    exclude = ('category','name', 'description', 'template')
    filter_horizontal = ('tags', 'platforms')
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
                'fields': ['icon', 'tags', 'platforms', 'price', 'type', ('template_ru', 'template_en'), 'timeCreated'],
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
        'type',
        'name_ru',
        'name_en',
        'description_ru',
        'description_en',
        'timeCreated',
    )
    search_fields = (
        'name_ru',
        'name_en',
        'tags'
    )
    list_filter = ('isPublished', 'timeCreated', 'platforms', 'type')

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


admin.site.register(M.Tag, TagAdmin)
admin.site.register(M.Category, CategoryAdmin)
admin.site.register(M.Article, ArticleAdmin)
admin.site.register(M.Question, QAAdmin)
admin.site.register(M.Termin, TDAdmin)
admin.site.register(M.Tool, ToolAdmin)
admin.site.register(M.Platform, PlatformAdmin)
admin.site.register(M.Note, NoteAdmin)
