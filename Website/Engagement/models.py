from django.db import models
from django.db.models.signals import post_delete, post_save
from django.db.models import Q
from django.dispatch import receiver
from Website.settings import LANGUAGES
from Post.models import Post, Tool
from django.utils.translation import gettext as _


class Interaction(models.Model):
    url = models.CharField(max_length=512, blank=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    time_updated = models.DateTimeField(auto_now=True, auto_created=True)

class Email(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Comment(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        ZERO = 0
    COMMENTS_PER_PAGE = 5
    url = models.CharField(max_length=512, blank=False)
    name = models.CharField(max_length=20, blank=False)
    time_published = models.DateTimeField(auto_now_add=True, auto_created=True)
    message = models.TextField(max_length=1024,blank=False)
    rating = models.IntegerField(choices=Rating, blank=True, default=Rating.ZERO)
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE, default=None)
    is_root = models.BooleanField(default=True)
    replies = models.ManyToManyField('self', blank=True, symmetrical=False)

    def get_score(_url):
        scores = Comment.objects.filter(url=_url).exclude(rating=Comment.Rating.ZERO).values_list('rating', flat=True)
        number_of_scores = len(scores)
        common_score = 0 
        for score in scores:
            common_score += score
        result = common_score/number_of_scores
        # Replace , to . because it will break Rich markup
        result = str(result).replace(',','.')
        return result
    
    def __str__(self):
        is_root = ''
        if self.is_root:
            is_root = 'Root'

        return f"{is_root}|{self.url} ->  {self.name} : {self.message[:15]}"
    

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
@receiver(post_save)
def _post_save_interaction(sender, instance, **kwargs): 
    if isinstance(instance, Post):
        for lang_code in LANGUAGES:
            code = lang_code[0]
            category = instance.category.slug
            field_name = f"slug_{code}"
            
            if instance.subcategory:
                subcategory_slug = getattr(instance.subcategory, field_name, instance.subcategory.slug)
                new_url = f"/{code}/{category}/{subcategory_slug}/{instance.slug}/"
            else:
                new_url = f"/{code}/{category}/{instance.slug}/"

            old_url = f"/{code}/{category}/{instance.slug}/"

            # Ищем Interaction по новому URL, старому URL или по совпадению slug в конце пути
            interaction = Interaction.objects.filter(
                Q(url=new_url) | Q(url=old_url) | Q(url__endswith=f"/{instance.slug}/")
            ).first()

            if interaction:
                if interaction.url != new_url:
                    # Перевязываем комментарии на новый URL
                    Comment.objects.filter(url=interaction.url).update(url=new_url)
                    interaction.url = new_url
                    interaction.save()
            else:
                Interaction.objects.create(url=new_url)

@receiver(post_delete)
def _post_delete_interaction(sender, instance, **kwargs): 
    if isinstance(instance, Post):
        for lang_code in LANGUAGES:
            code = lang_code[0]
            category = instance.category.slug
            slug = instance.slug
            url = f"/{'/'.join([code,category,slug])}/"
            interaction_qs = Interaction.objects.filter(url=url)
            if len(interaction_qs) > 0:
                interaction_qs[0].delete()

@receiver(post_save, sender=Comment)
def _post_save_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)

@receiver(post_delete, sender=Comment)
def _post_delete_comment(sender, instance, **kwargs): 
    updateInteractionCommentsLength(instance.url)