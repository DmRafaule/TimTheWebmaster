from django.conf import settings
from django.urls import path
from . import views as V

urlpatterns = [
    path(getattr(settings, 'BTCPAY_THANKS_PAGE_URL', 'btcpay-crowdfund/thanks/'), V.thanks, name="thanks-page"),
    path('btcpay-crowdfund/request-invoice/', V.request_invoice, name='request_invoice'),
    path('btcpay-crowdfund/submit-email/', V.submit_email, name='submit_email'),
    path('btcpay-crowdfund/get-email-form/<str:project_id>/', V.get_email_form_container, name='get_email_form_container'),
    path('btcpay-crowdfund/get-procceded-invoices/<str:project_id>', V.get_accepted_invoices, name="get_accepted_invoices"),
    path('btcpay-crowdfund/get-description/<str:project_id>', V.get_description, name="get_description"),
]