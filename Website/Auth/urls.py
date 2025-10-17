from django.urls import path
from . import views as V

urlpatterns = [
    path('login/', V.login, name="login"),
    path('logout/', V.logout, name="logout"),
    path('signup/', V.signup, name="signup"),
]