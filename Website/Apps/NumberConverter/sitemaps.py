from django.urls import reverse
from django.utils.translation import override
from django.contrib.sitemaps import Sitemap

from Website.settings import LANGUAGES
from .views import BASE_MAP



class NumberConverterSitemap(Sitemap):
    i18n = True

    def items(self):
        items = []
        for lang in LANGUAGES:
            with override(lang[0]):
                for key1, value1 in BASE_MAP.items():
                    for key2, value2 in BASE_MAP.items():
                        items.append(reverse('number-converter-specified', kwargs={'from_base': value1.get('short'), 'to_base': value2.get('short')}))

        return items

    def location(self, item):
        return item