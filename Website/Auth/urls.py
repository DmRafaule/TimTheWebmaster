from django.urls import path, re_path

from . import views as V

urlpatterns = [
    path('profile/', V.profile, name="profile"),
    path('login/', V.login, name="login"),
    path('login/', V.login, name="account_login"),
    path('logout/', V.logout, name="logout"),
    path('logout/', V.logout, name="account_logout"),
    path('signup/', V.signup, name="signup"),
    path('password_change/', V.password_change, name="password_change"),
    path('email_verify/', V.email_verify, name="email_verify"),
    path('email_verify/<str:verification_code>', V.email_verify, name="email_verify_with_code"),
    path('send_email_verify/', V.send_email_verify, name="send_email_verify"),
    path('password_reset/', V.password_reset, name="password_reset"),
    path('password_reset/done/', V.password_reset_done, name="account_reset_password_done"),
    re_path(r'^password_reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>[-\w]+)/$', V.CustomPasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    path('password_reset/key/done/', V.password_reset_from_key_done, name="account_reset_password_from_key_done"),
]