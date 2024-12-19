from django.urls import path
from . import views as V

urlpatterns = [
    path('like_post/', V.like_post),
    path('share_post/', V.share_post),
    path('bookmark_post/', V.bookmark_post),
    path('feedback_post/', V.feedback_post),
    path('load_comments/', V.load_comments),
    path('send_comment/', V.send_comment),
]