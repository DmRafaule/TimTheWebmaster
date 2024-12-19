from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Interaction(models.Model):
    url = models.CharField(max_length=512, blank=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)

class Comment(models.Model):
    COMMENTS_PER_PAGE = 5
    url = models.CharField(max_length=512, blank=False)
    name = models.CharField(max_length=20, blank=False)
    time_published = models.DateTimeField(auto_now=True, auto_created=True)
    message = models.TextField(max_length=1024,blank=False)
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE, default=None)


# Update a number of comments in Interaction 
def updateInteractionCommentsLength(url: str):
    interaction_tulpe = Interaction.objects.get_or_create(url=url)
    interaction = interaction_tulpe[0]
    interaction.comments = len(Comment.objects.filter(url=url))
    interaction.save()

@receiver(post_save, sender=Comment)
def _post_save_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)

@receiver(post_delete, sender=Comment)
def _post_delete_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)