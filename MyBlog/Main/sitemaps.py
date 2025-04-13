from itertools import chain

from django.db import models
from django.urls import reverse
from django.core import paginator
from django.contrib.sitemaps import Sitemap

from Post.models import Article, Tool, Note



class StaticSitemap(Sitemap):
    i18n = True

    def items(self):
        return ["about", "contacts", "home"]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    i18n = True

    def items(self):
        articles = Article.objects.filter(isPublished=True)
        tools = Tool.objects.filter(isPublished=True)
        items = list(chain(articles, tools))
        return items

    def lastmod(self, obj):
        return obj.timeUpdated


class PaginationSitemap(Sitemap):
    i18n = True

    def items(self):
        items = []
        
        articles = Article.objects.filter(isPublished=True)
        pagi = paginator.Paginator(articles, per_page=4)
        for page in pagi.page_range:
            items.append({
                "path": "articles-list",
                "page": page
            })

        tools = Tool.objects.filter(isPublished=True)
        pagi = paginator.Paginator(tools, per_page=4)
        for page in pagi.page_range:
            items.append({
                "path": "tools-list",
                "page": page
            })

        notes = Note.objects.filter(isPublished=True)
        pagi = paginator.Paginator(notes, per_page=4)
        for page in pagi.page_range:
            items.append({
                "path": "notes-list",
                "page": page
            })

        return items

    def location(self, item):
        if item['page'] == 1:
            return f"{reverse(item['path'])}"
        else:
            return f"{reverse(item['path'])}?page={item['page']}"
