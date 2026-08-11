from django.urls import path
from .views import tool_main 


urlpatterns = [
    path('text-thief/', tool_main, name='text-thief'),
]