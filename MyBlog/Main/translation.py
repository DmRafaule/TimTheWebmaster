from modeltranslation.translator import translator, TranslationOptions
from Post.models import Post
from Main.models import Image, Downloadable


class PostTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'template')


class ImageTranslationOptions(TranslationOptions):
    fields = ('text',)


class DownloadableTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(Post, PostTranslationOptions)
translator.register(Image, ImageTranslationOptions)
translator.register(Downloadable, DownloadableTranslationOptions)
