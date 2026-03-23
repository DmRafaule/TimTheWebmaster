from django.conf import settings
from django.urls import path
from . import views as V

urlpatterns = [
    path('btcpay-crowdfund/update-invoice/', V.update_invoice, name="update_invoice"),
]