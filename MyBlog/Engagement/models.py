from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from MyBlog.settings import LANGUAGES
from Post.models import Post


class Interaction(models.Model):
    url = models.CharField(max_length=512, blank=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    time_updated = models.DateTimeField(auto_now=True, auto_created=True)

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

# Here is the deal. This signals can create or delete Similar Interaction records.
# But if Post of other decendents change their slugs, they will be not deleted or changed 
# Accordinally.
#
# There is a nice way out. Just make ForeingKey field in Post model. But it will destroy all
# Independence of this app.
@receiver(post_save, sender=Post)
def _post_save_interaction(sender, instance, **kwargs): 
    isNewPostCreated = kwargs['created']
    for lang_code in LANGUAGES:
        code = lang_code[0]
        category = instance.category.slug
        slug = instance.slug
        url = f"/{'/'.join([code,category,slug])}/"
        if isNewPostCreated:
            interaction = Interaction(url=url)
            interaction.save()
        else:
            interaction, isCreated = Interaction.objects.get_or_create(url=url)

@receiver(post_save, sender=Post)
def _post_delete_interaction(sender, instance, **kwargs): 
    for lang_code in LANGUAGES:
        code = lang_code[0]
        category = instance.category.slug
        slug = instance.slug
        url = f"/{'/'.join([code,category,slug])}/"
        interaction_qs = Interaction.objects.filter(url=url)
        if len(interaction_qs) > 0:
            interaction_qs[0].delete()

# connect all subclasses of base content item too
for subclass in Post.__subclasses__():
    post_save.connect(_post_save_interaction, subclass)
    post_delete.connect(_post_delete_interaction, subclass)

@receiver(post_save, sender=Comment)
def _post_save_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)

@receiver(post_delete, sender=Comment)
def _post_delete_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)