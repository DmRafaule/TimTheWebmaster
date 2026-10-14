from django.urls import reverse
from django.contrib.sitemaps import Sitemap

from Main.urls import urlpatterns


class StaticSitemap(Sitemap):
    ''' Генератор XML-карты сайта для статическх(build-in) страниц на сайте '''
    i18n = True

    def items(self):
        pattern_names = []
        for pattern in urlpatterns:
            pattern_names.append(pattern.name)
        return pattern_names

    def location(self, item):
        return reverse(item)