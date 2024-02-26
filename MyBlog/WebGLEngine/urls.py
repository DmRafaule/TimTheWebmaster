from django.urls import path
from .views import main, geometry_bg, testing


urlpatterns = [
    path('webgl-engine/', main, name='webgl-engine'),
    path('webgl-engine/geometry-bg/', geometry_bg, name='geometry-bg'),
    path('webgl-engine/testing/', testing, name='testing'),
]
