from django.urls import path
from .views import main, geometry_bg, testing, home_gik


urlpatterns = [
    path('webgl-engine/', main, name='webgl-engine'),
    path('webgl-engine/geometry-bg/', geometry_bg, name='geometry-bg'),
    path('webgl-engine/home-gik/', home_gik, name='home-gik'),
    path('webgl-engine/testing/', testing, name='testing'),
]
