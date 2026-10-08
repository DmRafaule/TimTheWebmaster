from django.urls import path
from .views import tool_main 


urlpatterns = [
    path('number-converter/', tool_main, name='number-converter'),
]
