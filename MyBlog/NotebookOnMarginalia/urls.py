from django.urls import path
from .views import buffer


urlpatterns = [
    path('notebook/', buffer, name='image_thief'),
]
