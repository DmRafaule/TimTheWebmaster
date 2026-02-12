from modeltranslation.translator import translator, TranslationOptions
import Post.models as Post_M
import Main.models as Main_M


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

class ToolTranslationOptions(TranslationOptions):
    fields = ('name', 'h1', 'description', 'meta_keywords', 'template')
    
class ScraperTranslationOptions(TranslationOptions):
    fields = ('name', 'h1', 'description', 'meta_keywords', 'template', 'target')


translator.register(Post_M.Category, CategoryTranslationOptions)
translator.register(Post_M.Article, ArticleTranslationOptions)
translator.register(Post_M.Question, QATranslationOptions)
translator.register(Post_M.Termin, TDTranslationOptions)
translator.register(Post_M.Note, NoteTranslationOptions)
translator.register(Post_M.Tag, TagTranslationOptions)

translator.register(Post_M.Tool, TranslationOptions)
translator.register(Post_M.WebTool, ToolTranslationOptions)
translator.register(Post_M.TelegramBot, ToolTranslationOptions)
translator.register(Post_M.DjangoApp, ToolTranslationOptions)
translator.register(Post_M.Scraper, ScraperTranslationOptions)
translator.register(Post_M.Script, ToolTranslationOptions)

translator.register(Main_M.Contact, ContactTranslationOptions)
