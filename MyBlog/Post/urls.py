from django.urls import path
from .views import *


urlpatterns = [
    path('load_post_preview/', load_post_preview),
    path('articles/<slug:post_slug>/', article, name='Articles'),
    path('articles/', article_list, name='article_list'),
    path('news/<slug:post_slug>/', news, name='News'),
    path('news/', news_list, name='news_list'),
    path('projects/<slug:post_slug>/', proj, name='Projects'),
    path('projects/', proj_list, name='proj_list'),
    path('cases/<slug:post_slug>/', case, name='Cases'),
    path('cases/', case_list, name='case_list'),
    path('load_case/', load_case, name='load_case'),
    path('load_comment/', load_comment),
    path('remove_comment/', remove_comment),
    path('load_comments/', load_comments),
    path('load_comments_by_user/', load_comments_by_user), 
    path('like_post/', like_post),
    path('share_post/', share_post),
]
