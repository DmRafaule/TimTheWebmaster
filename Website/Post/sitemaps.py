from django.contrib.sitemaps import Sitemap

from .models import Article, Tool



class ArticleSitemap(Sitemap):
    ''' Для генерации XML-карты сайта для Статей '''

    i18n = True

    def items(self):
        articles = Article.objects.filter(isPublished=True)
        return articles

    def lastmod(self, obj):
        return obj.timeUpdated

class ToolSitemap(Sitemap):
    ''' Для генерации XML-карты сайта для Инструментов '''

    i18n = True

    def items(self):
        tools = Tool.objects.filter(isPublished=True)
        return tools

    def lastmod(self, obj):
        return obj.timeUpdated