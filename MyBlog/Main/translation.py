from modeltranslation.translator import translator, TranslationOptions
import Post.models as Post_M
import Main.models as Main_M


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'template')


class QATranslationOptions(TranslationOptions):
    fields = (
            'question',
            'description',
            'answer',
            'template',
    )


class TDTranslationOptions(TranslationOptions):
    fields = (
            'termin',
            'description',
            'key_phrases',
            'definition',
            'template',
    )


class ToolTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ImageTranslationOptions(TranslationOptions):
    fields = ('text',)


class DownloadableTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(Post_M.Category, CategoryTranslationOptions)
translator.register(Post_M.Article, ArticleTranslationOptions)
translator.register(Post_M.QA, QATranslationOptions)
translator.register(Post_M.TD, TDTranslationOptions)
translator.register(Post_M.Tool, ToolTranslationOptions)
translator.register(Main_M.Image, ImageTranslationOptions)
translator.register(Main_M.Downloadable, DownloadableTranslationOptions)
