from django.urls import path
from allauth.account.views import LogoutView, PasswordResetView, PasswordResetFromKeyView
from . import views as V

urlpatterns = [
    path('browser/v1/auth/signup', V.CustomSignupView.as_view(), name="allauth_signup"),
    path('browser/v1/auth/login', V.CustomLoginView.as_view(), name="allauth_login"),
    path('browser/v1/auth/logout', LogoutView.as_view(), name="allauth_logout"),
    path('browser/v1/auth/password/change', V.CustomPasswordChangeView.as_view(), name="allauth_password_change"),
    path('browser/v1/auth/password/reset', PasswordResetView.as_view(), name="allauth_password_reset"),
]
