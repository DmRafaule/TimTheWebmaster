from modeltranslation.translator import translator, TranslationOptions
import Post.models as Post_M
import Main.models as Main_M
from  PostEditor.models import PostTemplate


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ContactTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'h1', 'description', 'meta_keywords', 'template')


class TagTranslationOptions(TranslationOptions):
    fields = ('name','slug')

class QATranslationOptions(TranslationOptions):
    fields = (
            'question',
            'description',
            'answer',
    )

class TDTranslationOptions(TranslationOptions):
    fields = (
            'termin',
            'description',
            'definition',
    )

class NoteTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class PlatformTranslationOptions(TranslationOptions):
    fields = ('name',)

class ToolTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'template')

class ImageTranslationOptions(TranslationOptions):
    fields = ('text',)

class DownloadableTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(Post_M.Category, CategoryTranslationOptions)
translator.register(Post_M.Article, ArticleTranslationOptions)
translator.register(Post_M.Question, QATranslationOptions)
translator.register(Post_M.Termin, TDTranslationOptions)
translator.register(Post_M.Note, NoteTranslationOptions)
translator.register(Post_M.Tag, TagTranslationOptions)
translator.register(Post_M.Tool, ToolTranslationOptions)
translator.register(Post_M.Platform, PlatformTranslationOptions)
translator.register(Main_M.Image, ImageTranslationOptions)
translator.register(Main_M.Downloadable, DownloadableTranslationOptions)
translator.register(Main_M.Contact, ContactTranslationOptions)
