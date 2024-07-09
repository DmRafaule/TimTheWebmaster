from django.db import models


class Feed(models.Model):
    user_id = models.CharField(max_length=100, null=True)
    group = models.CharField(blank=True, max_length=256, null=True)
    source = models.URLField(blank=False)
    date_updated = models.DateTimeField(auto_now=True)