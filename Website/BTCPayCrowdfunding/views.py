import json
import requests
import hmac
import hashlib

from django.apps import apps
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import get_email_form
from .models import BTCPayCrowdfundApp, BTCPayCrowdfundDonation


@require_POST
def submit_email(request):
    BindedEmailForm = get_email_form()
    form = BindedEmailForm(request.POST)
    if form.is_valid():
        # Save the email
        email = form.cleaned_data.get("email")
        record, isCreated = BindedEmailForm._meta.model.objects.get_or_create(email=email)
        if isCreated:
            record.save()
            status = 200
        else:
            status = 201

        # Get the app
        app_id = form.cleaned_data.get("app_id")
        amount = form.cleaned_data.get("donation_choice")
        currency = form.cleaned_data.get("donation_currency")
        email = form.cleaned_data.get(getattr(settings, 'BTCPAY_CROWDFUND_EMAIL_MODEL_FIELD', 'email'))
        context = {
            'email_form_crowdfund': BindedEmailForm(),
            'BTCPayCrowdfundAPP_ID': app_id,
            'BTCPayCrowdfundAMOUNT': amount,
            'BTCPayCrowdfundCURRENCY': currency,
            'BTCPayCrowdfundEMAIL': email,
        }
        loaded_template = 'BTCPayCrowdfunding/email-form-next.html'
    else:
        context = {'email_form_crowdfund': form}
        loaded_template = 'BTCPayCrowdfunding/email-form.html'
        status = 400

    return TemplateResponse(request, template=loaded_template, context=context, status=status)

@require_POST
def request_invoice(request):
    amount = request.POST.get('amount', '10') 
    currency = request.POST.get('currency', 'USD') 
    app_id = request.POST.get('app_id', None) 
    
    url = f"https://{settings.BTCPAY_DOMAIN}/api/v1/stores/{settings.BTCPAY_STORE_ID}/invoices"

    allowed_amounts = [str(choice[0]) for choice in getattr(settings, 'BTCPAY_CROWDFUND_DONATION_CHOICES', [])]
    if amount not in allowed_amounts:
        return HttpResponse(_("Недопустимое значение суммы ￣へ￣"), status=400)
    
    if not BTCPayCrowdfundApp.objects.filter(app_id=app_id).exists():
        return HttpResponse(_("Приложения с таким ID не существует. ┗|｀O′|┛"), status=404)
    
    redirect_url = BTCPayCrowdfundApp.objects.filter(app_id=app_id).first().project.get_absolute_url()
    #redirect_url = request.build_absolute_uri(reverse('thanks-page'))

    headers = {
        "Authorization": f"token {settings.BTCPAY_AUTHORIZATION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "amount": amount,
        "currency": currency,
        "metadata": {
            "orderId": f"app_{app_id}",
        },
        "checkout": {
            "redirectURL": redirect_url, 
            "redirectAutomatically": True,
        }
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Получаем прямую ссылку на оплату
        invoice_url = data.get('checkoutLink')
        # Создаём запись в БД
        raw_email = request.POST.get('email', None) 
        EmailModel = apps.get_model(settings.BTCPAY_CROWDFUND_EMAIL_MODEL_TO_BIND)
        email_field = getattr(settings, 'BTCPAY_CROWDFUND_EMAIL_MODEL_FIELD', 'email')
        email, is_created = EmailModel.objects.get_or_create(**{email_field: raw_email})
        invoice_id = data.get('id')
        app = BTCPayCrowdfundApp.objects.filter(app_id=app_id).first()

        donation = BTCPayCrowdfundDonation(app=app, email=email, invoice_id=invoice_id)
        donation.save()

        response = HttpResponse(status=204)
        response['HX-Redirect'] = invoice_url
        return response

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Ошибка BTCPay: {str(e)}", status=500)

def thanks(request):
    context = {}
    callback_path = getattr(settings, 'BTCPAY_CROWDFUND_THANKS_CONTEXT_CALLBACK', None)
    
    if callback_path:
        try:
            context_callback = import_string(callback_path)
            additional_context = context_callback(request)
            
            if isinstance(additional_context, dict):
                context.update(additional_context)
        except ImportError:
            raise ValueError('Invalid path for a callback. Please check your BTCPAY_CROWDFUND_THANKS_CONTEXT_CALLBACK constant.')
        
    template = getattr(settings, 'BTCPAY_THANKS_PAGE', 'BTCPayCrowdfunding/thanks-page.html')
    return render(request, template, context)

def get_app_id(project_id, code):
    current_language = code
    lookup_field = getattr(settings, 'BTCPAY_CROWDFUND_APP_LOOKUP_FIELD', 'project__slug')
    filter_kwargs = {lookup_field: project_id}
    apps = BTCPayCrowdfundApp.objects.filter(**filter_kwargs)
    if len(apps) > 0:
        app = apps.filter(language_code=current_language).first()
        return app.app_id
    else:
        return None

def get_email_form_container(request, project_id):
    BindedEmailForm = get_email_form()
    # Get the app
    app_id = get_app_id(project_id, request.LANGUAGE_CODE)
    if app_id:
        status = 200
    else:
        status = 404

    form = BindedEmailForm(initial={'app_id': app_id})
    return render(request, 'BTCPayCrowdfunding/email-form-container.html', context = {
        'email_form_crowdfund': form
    }, status=status)

def get_accepted_invoices(request, project_id):
    app_id = get_app_id(project_id, request.LANGUAGE_CODE)
    headers = {
        "Authorization": f"token {settings.BTCPAY_AUTHORIZATION_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"https://{settings.BTCPAY_DOMAIN}/api/v1/stores/{settings.BTCPAY_STORE_ID}/invoices?textSearch=app_{app_id}&status=Settled"
    totalPaid = 0
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Will return a list of the "Settled" invoices
        data = response.json()
        for invoice in data:
            totalPaid += float(invoice['paidAmount'])
    
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Ошибка BTCPay: {str(e)}", status=500)
    
    app_url = f"https://{settings.BTCPAY_DOMAIN}/api/v1/apps/crowdfund/{app_id}"
    targetAmount = 0
    targetCurrency = 'USD'
    try:
        response = requests.get(app_url, headers=headers, timeout=10)
        response.raise_for_status()
        # Will return an app data
        data = response.json()
        targetAmount = data['targetAmount']
        targetCurrency = data['targetCurrency']
    
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Ошибка BTCPay: {str(e)}", status=500)
    
    return render(request, getattr(
        settings, 
        'BTCPAY_CROWDFUND_STATUS_PAGE', 'BTCPayCrowdfunding/crowdfunding-status.html'),
        context={
            'totalPaid': totalPaid,
            'targetAmount': targetAmount,
            'targetCurrency': targetCurrency
        })

def get_description(request, project_id):
    app_id = get_app_id(project_id, request.LANGUAGE_CODE)
    url = f"https://{settings.BTCPAY_DOMAIN}/api/v1/apps/crowdfund/{app_id}"
    headers = {
        "Authorization": f"token {settings.BTCPAY_AUTHORIZATION_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Will return an app data
        data = response.json()
        description = data['description']
    
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Ошибка BTCPay: {str(e)}", status=500)
    
    return render(request, getattr(
        settings, 
        'BTCPAY_CROWDFUND_DESCRIPTION_PAGE', 'BTCPayCrowdfunding/crowdfunding-description.html'),
        context={
            'app_description': description,
        })

@csrf_exempt
@require_POST
def update_invoice(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    # Проверка подписи 
    webhook_secret = getattr(settings, 'BTCPAY_WEBHOOK_SECRET', None)
    if webhook_secret:
        signature = request.headers.get('BTCPay-Sig')
        expected_sig = 'sha256=' + hmac.new(
            webhook_secret.encode(), 
            request.body, 
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            return HttpResponse("Invalid signature", status=403)

    invoice_id = data.get('invoiceId')
    new_status_str = data.get('type')

    # 2. Маппинг статусов BTCPay к вашей модели
    status_mapping = {
        'InvoiceCreated': BTCPayCrowdfundDonation.DonationStatus.NEW,
        'InvoiceProcessing': BTCPayCrowdfundDonation.DonationStatus.PROCESSING,
        'InvoiceExpired': BTCPayCrowdfundDonation.DonationStatus.EXPIRED,
        'InvoiceInvalid': BTCPayCrowdfundDonation.DonationStatus.INVALID,
        'InvoiceSettled': BTCPayCrowdfundDonation.DonationStatus.SETTLED,
    }

    # 3. Поиск и обновление записи
    try:
        donation = BTCPayCrowdfundDonation.objects.get(invoice_id=invoice_id)
        
        if new_status_str in status_mapping:
            donation.status = status_mapping[new_status_str]
            donation.save()
            return HttpResponse(status=200)
        
        return HttpResponse("Status not recognized", status=200) # Игнорируем неизвестные
        
    except BTCPayCrowdfundDonation.DoesNotExist:
        # Если инвойс не найден, возможно он был создан вне этой системы
        return HttpResponse("Donation not found", status=404)