from django.urls import path
from . import views as V

urlpatterns = [
    path('', V.MainView.as_view(template_name="Main/home.html"), name='home'),
    path('contacts/', V.MainView.as_view(template_name="Main/contacts.html"), name='contacts'),
    path('about/',  V.MainView.as_view(template_name="Main/about.html"), name='about'),
    path('contacts/load_message/', V.load_message, name='load_message'),
    path('about/load_message/', V.load_message, name='load_message'),
    path('load_table_of_content/', V.load_table_of_content),
]
