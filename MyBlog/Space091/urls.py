from django.urls import path
from .views import main


urlpatterns = [
    path('space-main/', main, name='space-main'),
]
