from django.urls import path
from .views import post, load_post_preview, article_list, news_list, proj_list, case_list, load_case, like_post, share_post


urlpatterns = [
    path('load_post_preview/', load_post_preview),
    path('articles/<slug:post_slug>/', post, name='Articles'),
    path('articles/', article_list, name='article_list'),
    path('news/<slug:post_slug>/', post, name='News'),
    path('news/', news_list, name='news_list'),
    path('projects/<slug:post_slug>/', post, name='Projects'),
    path('projects/', proj_list, name='proj_list'),
    path('cases/<slug:post_slug>/', post, name='Cases'),
    path('cases/', case_list, name='case_list'),
    path('load_case/', load_case, name='load_case'),
    path('like_post/', like_post),
    path('share_post/', share_post),
]
