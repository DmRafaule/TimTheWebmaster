from django.urls import reverse
from django.utils.translation import override
from django.contrib.sitemaps import Sitemap

from Website.settings import LANGUAGES
from Main.utils import get_subcategories
from Post.models import Article, Tool



class SubcategorySitemap(Sitemap):
    ''' Для генерации XML-карты сайта для подкатегорий '''

    def items(self):
        items = []
        subcategories_articles = get_subcategories(Article.objects.all())
        for subc in subcategories_articles:
            for lang in LANGUAGES:
                with override(lang[0]):
                    items.append({'category': 'articles', 'slug': subc.slug, 'code': lang[0]})

        subcategories_tools = get_subcategories(Tool.objects.all())
        for subc in subcategories_tools:
            for lang in LANGUAGES:
                with override(lang[0]):
                    items.append({'category': 'tools', 'slug': subc.slug, 'code': lang[0]})

        return items
    
    def location(self, item):
        return f"/{item.get('code')}/{item.get('category')}/{item.get('slug')}/"