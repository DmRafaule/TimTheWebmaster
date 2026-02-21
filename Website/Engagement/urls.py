from django.urls import path
from . import views as V

urlpatterns = [
    path('like_post/', V.like_post),
    path('share_post/', V.share_post),
    path('bookmark_post/', V.bookmark_post),
    
    path('email_subscription/', V.email_post),
    path('email_subscription_form/', V.email_form_get),

    path('load_comments/', V.load_comments),
    path('load_replies/', V.load_replies),
    path('send_comment/', V.send_comment),
]