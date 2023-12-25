from django.urls import path
from . import views as V
from . import models as M


urlpatterns = [
    path('main_shader/', V.main_shader),
]
