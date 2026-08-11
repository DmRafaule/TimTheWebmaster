from django.urls import path
from .views import PostListView, PostFeed
from Post.models import Article, Tool, Note, Service


urlpatterns = [
    path('articles/', PostListView.as_view(model=Article, post_preview_template='Post/basic--post_preview-article.html', category='articles'), name='articles-list'),
    path('tools/', PostListView.as_view(model=Tool, post_preview_template='Post/basic--post_preview-tool.html', category='tools'), name='tools-list'),
    path('notes/', PostListView.as_view(model=Note, post_preview_template='Post/basic--post_preview-note.html', category='notes'), name='notes-list'),
    path('services/', PostListView.as_view(model=Service, post_preview_template='Post/basic--post_preview-service.html', category='services'), name='services-list'),
    path("articles-rss/", PostFeed(Article, 'articles'), name=f"articles-rss"),
    path("tools-rss/", PostFeed(Tool, 'tools'), name=f"tools-rss"),
    path("notes-rss/", PostFeed(Note, 'notes'), name=f"notes-rss"),
    path("services-rss/", PostFeed(Service, 'service'), name=f"services-rss"),
]