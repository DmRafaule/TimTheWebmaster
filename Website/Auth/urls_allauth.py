from django.urls import path
from allauth.account.views import LogoutView
from . import views as V

urlpatterns = [
    path('browser/v1/auth/signup', V.CustomSignupView.as_view(), name="allauth_signup"),
    path('browser/v1/auth/login', V.CustomLoginView.as_view(), name="allauth_login"),
    path('browser/v1/auth/logout', LogoutView.as_view(), name="allauth_logout"),
]
