from django.urls import path
from .views import profile, login, signup, signup_verify, login_verify, logout


urlpatterns = [
    path('profile/<slug:user_slug>', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('login/verify-login/', login_verify, name='login_verify'),
    path('signup/', signup, name='signup'),
    path('signup/verify-signup/', signup_verify, name='signup_verify'),
]
