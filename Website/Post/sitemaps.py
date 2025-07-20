from itertools import chain

from django.contrib.sitemaps import Sitemap

from .models import Article, Tool



class PostSitemap(Sitemap):
    ''' Для генерации XML-карты сайта для постов типа Статей и Инструментов '''

    i18n = True

    def items(self):
        articles = Article.objects.filter(isPublished=True)
        tools = Tool.objects.filter(isPublished=True)
        items = list(chain(articles, tools))
        return items

    def lastmod(self, obj):
        return obj.timeUpdated