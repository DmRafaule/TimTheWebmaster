from django.urls import path
from .views import send_comment_guesting, send_comment_authorized, load_comments, prepare_user, remove_comment, load_comments_by_user


urlpatterns = [
    path('send_comment_guesting/', send_comment_guesting),
    path('send_comment_authorized/', send_comment_authorized),
    path('remove_comment/', remove_comment),
    path('prepare_user/', prepare_user),
    path('load_comments/', load_comments),
    path('load_comments_by_user/', load_comments_by_user),
]
