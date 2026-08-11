from django.urls import path
from .views import tool_main 


urlpatterns = [
    path('link-thief/', tool_main, name='link-thief'),
]
