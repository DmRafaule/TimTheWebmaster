from modeltranslation.translator import translator, TranslationOptions
from Post.models import Post


class PostTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'template')


translator.register(Post, PostTranslationOptions)
