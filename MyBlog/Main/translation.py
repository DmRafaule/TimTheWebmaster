from modeltranslation.translator import translator, TranslationOptions
import Post.models as Post_M
import Main.models as Main_M


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'template')


class NewsTranslationOptions(TranslationOptions):
    fields = ('headline', 'description', 'first_sentence', 'lead', 'body', 'ending', )


class CaseTranslationOptions(TranslationOptions):
    fields = (
            'title',
            'subtitle',
            'description',
            'resume',
            'client_name',
            'client_description',
            'goals',
            'solution',
            'additional',
            'result',
    )


class QATranslationOptions(TranslationOptions):
    fields = (
            'question',
            'description',
            'answer'
    )


class TDTranslationOptions(TranslationOptions):
    fields = (
            'termin',
            'description',
            'definition'
    )


class ToolTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ImageTranslationOptions(TranslationOptions):
    fields = ('text',)


class DownloadableTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(Post_M.Category, CategoryTranslationOptions)
translator.register(Post_M.Article, ArticleTranslationOptions)
translator.register(Post_M.News, NewsTranslationOptions)
translator.register(Post_M.Case, CaseTranslationOptions)
translator.register(Post_M.QA, QATranslationOptions)
translator.register(Post_M.TD, TDTranslationOptions)
translator.register(Post_M.Tool, ToolTranslationOptions)
translator.register(Main_M.Image, ImageTranslationOptions)
translator.register(Main_M.Downloadable, DownloadableTranslationOptions)
