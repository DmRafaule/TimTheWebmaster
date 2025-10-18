from django.urls import path, re_path
from . import views as V

urlpatterns = [
    path('profile/', V.profile, name="profile"),
    path('login/', V.login, name="login"),
    path('logout/', V.logout, name="logout"),
    path('signup/', V.signup, name="signup"),
    path('password_change/', V.password_change, name="password_change"),
    path('email_verify/', V.email_verify, name="email_verify"),
    path('email_verify/<str:verification_code>', V.email_verify, name="email_verify_with_code"),
    path('send_email_verify/', V.send_email_verify, name="send_email_verify"),
]