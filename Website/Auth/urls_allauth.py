from django.urls import path
from allauth.account.views import LogoutView, PasswordChangeView
from . import views as V

urlpatterns = [
    path('browser/v1/auth/signup', V.CustomSignupView.as_view(), name="allauth_signup"),
    path('browser/v1/auth/login', V.CustomLoginView.as_view(), name="allauth_login"),
    path('browser/v1/auth/logout', LogoutView.as_view(), name="allauth_logout"),
    path('browser/v1/auth/logout', PasswordChangeView.as_view(), name="allauth_password_change"),
]
