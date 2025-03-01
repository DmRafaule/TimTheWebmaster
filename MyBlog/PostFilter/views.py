from django.contrib.syndication.views import Feed
from django.utils.translation import get_language
from django.urls import reverse


class PostFeed(Feed):

    def __init__(self, model, category):
        super().__init__()
        self.model = model
        self.category = category
    
    def title(self):
        return self.category.name

    def description(self):
        return self.category.description

    def link(self):
        return f"/{get_language()}/{self.category.slug}-rss/"

    def items(self):
        return self.model.objects.filter(isPublished=True).order_by("-timeCreated")[:50]

    def item_title(self, item):
        if hasattr(item, 'title'):
            return item.title
        elif hasattr(item, 'name'):
            return item.name

    def item_description(self, item):
        return item.description
    
    def item_pubdate(self, item):
        return item.timeCreated

    def item_link(self, item):
        if hasattr(item, 'get_absolute_url'):
            return item.get_absolute_url()
        else:
            return reverse(f'{self.category.slug}-list')