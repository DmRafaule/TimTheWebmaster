from django.urls import path
from . import views as V


# Patterns for displaying posts by itself
# There is no tools because tool is a django app so it has to
#   handle it's own urls
urlpatterns = [
    path('articles/<slug:post_slug>/', V.article, name="article"),
    path('qa/<slug:post_slug>/', V.qa, name="qa"),
    path('td/<slug:post_slug>/', V.td, name="td"),
    path('tools/<slug:post_slug>/', V.tool, name="tool"),
]

urlpatterns += [
    path('articles/', V.article_list, name='articles-list'),
    path('td/', V.td_list, name='td-list'),
    path('qa/', V.qa_list, name='qa-list'),
    path('tools/', V.tools_list, name='tools-list'),
    path('notes/', V.notes_list, name='notes-list'),
]