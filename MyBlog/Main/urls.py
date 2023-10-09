from django.urls import path
from .views import about, contacts, home, load_message, services


urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('contacts/', contacts, name='contacts'),
    path('contacts/load_message/', load_message, name='load_message'),
    path('about/', about, name='about'),
]
