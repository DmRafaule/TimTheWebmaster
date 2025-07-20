from django.urls import path
from . import views as V

urlpatterns = [
    path('', V.home, name='home'),
    path('contacts/', V.ContactsView.as_view(template_name="Main/contacts.html"), name='contacts'),
    path('about/',  V.about, name='about'),
]
