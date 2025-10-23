from django.urls import path 
from . import views as V


urlpatterns = [
    path('admin/', V.admin, name="admin"),
]