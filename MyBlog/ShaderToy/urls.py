from django.urls import path
from .views import main, save_shader, load_shader, remove_shader, get_shader, load_library


urlpatterns = [
    path('shader-toy/', main, name='shader-toy'),
    path('shader-toy/save_shader/', save_shader, name='save_shader'),
    path('shader-toy/load_shader/', load_shader, name='load_shader'),
    path('shader-toy/load_library/', load_library, name='load_library'),
    path('shader-toy/remove_shader/', remove_shader, name='remove_shader'),
    path('shader-toy/get_shader/', get_shader, name='get_shader'),
]
