from django.urls import path
from . import views as V
from . import models as M


urlpatterns = [
    path('like_post/', V.like_post),
    path('share_post/', V.share_post),
]

# Patterns for displaying posts by itself
# There is no tools because tool is a django app so it has to
#   handle it's own urls
urlpatterns += [
    path('articles/<slug:post_slug>/', V.article, name="article"),
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