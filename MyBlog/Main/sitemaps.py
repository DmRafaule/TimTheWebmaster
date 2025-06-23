from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    ''' Генератор XML-карты сайта для статическх(build-in) страниц на сайте '''
    i18n = True

    def items(self):
        return ["about", "contacts", "home"]

    def location(self, item):
        return reverse(item)