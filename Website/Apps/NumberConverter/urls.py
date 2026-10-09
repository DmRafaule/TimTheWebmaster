from django.urls import path
from .views import tool_main 


urlpatterns = [
    path('number-converter/', tool_main, name='number-converter'),
    path('number-converter/<slug:from_base>-<slug:to_base>/', tool_main, name='number-converter-specified'),
]
