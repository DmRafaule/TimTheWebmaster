from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    i18n = True

    def items(self):
        return ["about", "contacts", "home"]

    def location(self, item):
        return reverse(item)