from django.urls import path
from .views import tool_main


urlpatterns = [
    path('smil-svg-animation-editor/', tool_main, name='smil-animation-editor'),
]