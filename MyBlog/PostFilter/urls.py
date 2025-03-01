from django.urls import path
from .views import PostFeed
from Post.models import Category, Article, Note, Tool


urlpatterns = [
    path(
        f"{Category.objects.get(slug='articles').slug}-rss/",
        PostFeed(
            Article, 
            Category.objects.get(slug='articles')), 
        name=f"{Category.objects.get(slug='articles').slug}-rss"),

    path(
        f"{Category.objects.get(slug='tools').slug}-rss/",
        PostFeed(
            Tool, 
            Category.objects.get(slug='tools')), 
        name=f"{Category.objects.get(slug='tools').slug}-rss"),
    path(
        f"{Category.objects.get(slug='notes').slug}-rss/",
        PostFeed(
            Note, 
            Category.objects.get(slug='notes')), 
        name=f"{Category.objects.get(slug='notes').slug}-rss"),
]