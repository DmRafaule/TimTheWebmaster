from django.urls import path
from . import views as V
from . import models as M


urlpatterns = [
    path('like_post/', V.like_post),
    path('share_post/', V.share_post),
]
# patterns for handling home page of website
urlpatterns += [
    path(
        'load_post_preview-articles/',
        V.PostPreviewView.as_view(
            model=M.Article,
        ),
        name="article-home-preview"),
    path(
        'load_post_preview-news/',
        V.PostPreviewView.as_view(
            model=M.News,
        ),
        name="news-home-preview"),
    path(
        'load_post_preview-cases/',
        V.PostPreviewView.as_view(
            model=M.Case,
        ),
        name="cases-home-preview"),
    path(
        'load_post_preview-tools/',
        V.PostPreviewView.as_view(
            model=M.Tool,
        ),
        name="tools-home-preview"),
    path(
        'load_post_preview-td/',
        V.PostPreviewView.as_view(
            model=M.TD,
        ),
        name="td-home-preview"),
    path(
        'load_post_preview-qa/',
        V.PostPreviewView.as_view(
            model=M.QA,
        ),
        name="qa-home-preview"),
]
# Patterns for displaying posts by itself
# There is no tools because tool is a django app so it has to
#   handle it's own urls
urlpatterns += [
    path('articles/<slug:post_slug>/', V.article, name="article"),
    path('news/<slug:post_slug>/', V.news, name="news"),
    path('cases/<slug:post_slug>/', V.case, name="case"),
    path('qa/<slug:post_slug>/', V.qa, name="qa"),
    path('td/<slug:post_slug>/', V.td, name="td"),
]


# URL path for dispatching list of posts
for cat in M.Category.objects.all():
    urlpatterns.append(
        path(
            f'{cat.slug}/',
            V.PostListView.as_view(
                template_name=cat.template,
                category=cat),
            name=f"{cat.slug}-list"
        )
    )