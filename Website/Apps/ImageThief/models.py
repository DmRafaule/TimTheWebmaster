# For now it is useless piec of code.
# If for some reason this tool will be popular
# And cron could not manage all deletion
# I will have to transfer this tool on database

from django.db import models


TRY_LIMIT = 1000
EXPIRED_TIME = 1  # In hours


class ScraperUser(models.Model):
    current_try = models.IntegerField(default=0)
    name = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class ScraperImage(models.Model):
    timeCreated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ScraperUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
