from django.urls import path
from . import views as V


# Patterns for displaying posts by itself
# There is no tools because tool is a django app so it has to
#   handle it's own urls
urlpatterns = [
    path('articles/<slug:post_slug>/', V.article, name="article"),
    path('tools/<slug:post_slug>/', V.tool, name="tool"),
]