from django.db import models


class FeedId(models.Model):
    user_id = models.CharField(max_length=100, null=True)
    similar_user_id = models.ManyToManyField('self', blank=True)

    class SortDirection(models.IntegerChoices):
        LATEST_FIRST = 0 
        EARLIEST_FIRST = 1

    sort = models.IntegerField(choices=SortDirection, default=SortDirection.LATEST_FIRST)
    posts_per_page= models.PositiveIntegerField(default=5)
    with_previews = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user_id}'
    
    def get_sort_direction(self):
        match self.sort:
            case self.SortDirection.LATEST_FIRST:
                return True
            case self.SortDirection.EARLIEST_FIRST:
                return False

class Feed(models.Model):
    user_id = models.ForeignKey(FeedId, blank=True, null=True, on_delete=models.CASCADE)
    name  = models.CharField(max_length=250, blank=False, null=True)
    feed = models.URLField(blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name: {self.name} src: {self.feed}'

class FeedGroup(models.Model):
    user_id = models.ForeignKey(FeedId, blank=False, on_delete=models.CASCADE)
    is_common = models.BooleanField(default=False, blank=False)
    name  = models.CharField(max_length=250, blank=False)
    feeds = models.ManyToManyField(Feed, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name: {self.name}'