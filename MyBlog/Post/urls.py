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
]
# patterns for handling previews of list of objects in website categories pages
urlpatterns += [
    path(
        'articles/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.Article,
        ),
        name="article-preview"),
    path(
        'news/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.News
        ),
        name="news-preview"),
    path(
        'cases/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.Case
        ),
        name="cases-preview"),
    path(
        'td/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.TD
        ),
        name="td-preview"),
    path(
        'qa/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.QA
        ),
        name="qa-preview"),
    path(
        'tools/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.Tool
        ),
        name="tools-preview"),
    path(
        'services/load_post_preview/',
        V.PostPreviewView.as_view(
            model=M.Service
        ),
        name="service-preview"),
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
    path('services/<slug:post_slug>/', V.service, name="service"),
    path('services/<slug:post_slug>/load_message/', V.load_message),

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
