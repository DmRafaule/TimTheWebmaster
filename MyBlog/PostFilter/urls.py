from django.urls import path
from .views import PostFeed
from Post.models import Article, Note, Tool


urlpatterns = [
    path("articles-rss/", PostFeed(Article, 'articles'), name=f"articles-rss"),
    path("tools-rss/", PostFeed(Tool, 'tools'), name=f"tools-rss"),
    path("notes-rss/", PostFeed(Note, 'notes'), name=f"notes-rss"),
]