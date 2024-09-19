from django.db import models
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from Post.models import Post
import os, shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from MyBlog.settings import MEDIA_ROOT


def user_directory_path_forImageAndDownloadabel(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "{0}/{1}/{2}".format(instance.type.category.slug, instance.type.slug, filename)


class Website(models.Model):
    class Meta:
         db_table_comment = "This is a general model of the site. It is created to manage all elements of the site, with the ability to switch between them (Different records of the model)"
         verbose_name = 'Website'
         verbose_name_plural = 'Website'

    name = models.CharField(max_length=256, blank=False)
    is_current = models.BooleanField(default=False, help_text='Should be checked only for one record of Website databse')
    # Post part
    NO_THRESHOLD = 1
    MINIMAL_THRESHOLD = 2
    TOLERATED_THRESHOLD = 3
    MAXIMAL_THRESHOLD = 5
    THRESHOLDS = {
        NO_THRESHOLD: 'No threshold (1)',
        MINIMAL_THRESHOLD: 'Minimal threshold (2)',
        TOLERATED_THRESHOLD: 'Tolerated threshold (3)',
        MAXIMAL_THRESHOLD: 'Maximal threshold (5)',
    }

    threshold_similar_articles = models.IntegerField(verbose_name='Threshold for tag matching between articles', default=TOLERATED_THRESHOLD, choices=THRESHOLDS, help_text='This field sets the threshold for tag matching between current viewed article and others articles.')
    threshold_related_termins = models.IntegerField(verbose_name='Threshold for tag matching between articles and termins', default=MINIMAL_THRESHOLD, choices=THRESHOLDS, help_text='This field sets the threshold for tag matching between current viewed article and termins.')
    threshold_related_questions = models.IntegerField(verbose_name='Threshold for tag matching between articles and questions', default=MINIMAL_THRESHOLD, choices=THRESHOLDS, help_text='This field sets the threshold for tag matching between current viewed article and questions.')

    NO_DISPLAY = 0
    MINIMAL_DISPLAY = 2
    TOLERATED_DISPLAY = 3
    MAXIMAL_DISPLAY = 5
    MAX_DISPLAYS = {
        NO_DISPLAY: 'Do not display',
        MINIMAL_DISPLAY: 'Minimal display (2)',
        TOLERATED_DISPLAY: 'Tolerate display (3)',
        MAXIMAL_DISPLAY: 'Maximal display (5)',
    }
    max_displayed_similar_articles = models.IntegerField(verbose_name='How many sim. articles to display', default=MINIMAL_DISPLAY, choices=MAX_DISPLAYS, help_text='This field sets how many similar articles to display on the current viewed article.')
    max_displayed_termins = models.IntegerField(verbose_name='How many related termins to display', default=MAXIMAL_DISPLAY, choices=MAX_DISPLAYS, help_text='This field sets how many related termins to display on the current viewed article.')
    max_displayed_questions = models.IntegerField(verbose_name='How many related questions to display', default=TOLERATED_DISPLAY, choices=MAX_DISPLAYS, help_text='This field sets how many related questions to display on the current viewed article.')
    # Post list part
    paginator_per_page_posts = models.IntegerField(verbose_name='Posts per page', default=4, blank=False, help_text='This field sets how many posts should be loaded while scrolling or paginating')
    paginator_per_page_gallery = models.IntegerField(verbose_name='Images per page', default=4, blank=False, help_text='This field sets how many images should be loaded while scrolling or paginating')
    paginator_per_page_gallery_columns = models.IntegerField(verbose_name='Columns to use for masonry', default=2, blank=False, help_text='This field sets how many columns should be used for masonry')
    # Common part
    categories_to_display_on_side_menu = models.ManyToManyField('Post.Category', verbose_name='Categories to display on side menu', blank=False)
    popular_articles_on_footer = models.ManyToManyField('Post.Article', verbose_name='Articles to display on footer', blank=False)
    popular_tools_on_footer = models.ManyToManyField('Post.Tool', verbose_name='Tools(Archives) to display on footer', blank=False)

    # Home page part
    my_resources_choosen_tags_on_home = models.ManyToManyField('Post.Tag', verbose_name='Choosen tags for My resources part', blank=False, related_name='my_resouces')
    min_displayed_my_resources = models.IntegerField(verbose_name='Minimum el in My resources part to be displayed if present', default=3, blank=False)
    other_articles_choosen_tags_on_home = models.ManyToManyField('Post.Tag', verbose_name='Choosen tags for Other articles part', blank=False, related_name='other_articles')
    min_displayed_other_articles = models.IntegerField(verbose_name='Minimum el in Other articles part to be displayed if present', default=2, blank=False)
    max_displayed_news_on_home = models.IntegerField(verbose_name='Limit to display Latest news', default=3, blank=False)
    max_displayed_postSeries_on_home = models.IntegerField(verbose_name='Limit to display post series', default=2, blank=False)
    max_displayed_images_on_home = models.IntegerField(verbose_name='Limit to display images', default=3, blank=False)


class Image(models.Model):
    ART = 'Ar'
    RESOURCE = 'Re'
    IMAGE_CATEGORIES = {
        ART: "Art",
        RESOURCE: "Resource"
    }
    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.ImageField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)
    # disable related name for tag field by setting related_name field to '+'
    tags = models.ManyToManyField('Post.Tag', blank=True, related_name='+')
    category = models.CharField(max_length=2, choices=IMAGE_CATEGORIES, default=RESOURCE, blank=True)
    timeCreated = models.DateTimeField(auto_now=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/media/{0}'.format(self.file)


class Downloadable(models.Model):
    VIDEO = 'Vi'
    SCRIPT = 'Sc'
    ARCHIVE = 'Ac'
    TG_BOT = 'Tb'
    PARSER = 'Pr'
    DOWNLOADABLE_CATEGORIES = {
        VIDEO: "Video",
        SCRIPT: "Script",
        ARCHIVE: "Archive",
        TG_BOT: "Telegram bot",
        PARSER: "Parser",
    }

    type = models.ForeignKey(Post, on_delete=models.CASCADE)  # Which category this have to be put in
    file = models.FileField(upload_to=user_directory_path_forImageAndDownloadabel, blank=False)
    text = models.CharField(max_length=250, blank=True)
    category = models.CharField(max_length=2, choices=DOWNLOADABLE_CATEGORIES, default=ARCHIVE, blank=True)
    timeCreated = models.DateTimeField(auto_now=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/media/{0}'.format(self.file)

class VideosSitemap(Sitemap):
    def items(self):
        videos = Downloadable.objects.filter(category=Downloadable.VIDEO)
        return list(videos)

    def lastmod(self, obj):
        return obj.timeUpdated

class StaticSitemap(Sitemap):
    i18n = True

    def items(self):
        return ["about", "contacts", "home"]

    def location(self, item):
        return reverse(item)


# Remove loaded file before deleting on database
@receiver(pre_delete, sender=Image)
def deleteImage(sender, instance, **kwargs):
    os.remove(os.path.join(MEDIA_ROOT, f"{instance.file}"))


# Remove loaded file before deleting on database
@receiver(pre_delete, sender=Downloadable)
def deleteDownloadable(sender, instance, **kwargs):

    os.remove(os.path.join(MEDIA_ROOT, f"{instance.file}"))
