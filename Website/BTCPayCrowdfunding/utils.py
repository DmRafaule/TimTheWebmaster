import hmac
import hashlib
from functools import wraps

from django.db import transaction
from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.module_loading import import_string

from .models import BTCPayCrowdfundDonation, BTCPayCrowdfundApp

def get_hash(token, email):
    """Создает безопасный хеш из токена и почты."""
    data = f"{token}{email}" # Добавляем SECRET_KEY как "соль"
    return hashlib.sha256(data.encode()).hexdigest()

@transaction.atomic
def validate_and_activate(raw_token, user_email):
    input_hash = get_hash(raw_token, user_email)

    # Блокируем строку в базе 
    try:
        donation = BTCPayCrowdfundDonation.objects.select_for_update().get(
            receipt_id=input_hash,
            status=BTCPayCrowdfundDonation.DonationStatus.SETTLED
        )
        
        # Сравнение хешей на атомарном времени (Timing Attack protection)
        if not hmac.compare_digest(donation.receipt_id, input_hash):
            return False, "Invalid hash"

        if donation.is_used:
            return False, "Already used"

        # Активируем
        donation.is_used = True
        donation.used_at = timezone.now()
        donation.save()
        
        return True, "Success"
        
    except BTCPayCrowdfundDonation.DoesNotExist:
        return False, "Not found"

def ratelimit_check(seconds=60, max_attempts=3):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Используем IP как ключ
            ip = request.META.get('REMOTE_ADDR')
            cache_key = f"ratelimit_login_{ip}"
            
            attempts = cache.get(cache_key, 0)
            
            if attempts >= max_attempts:
                return HttpResponseForbidden(_("Слишком много попыток, повтори в следующий раз"))
            
            # Увеличиваем счетчик
            cache.set(cache_key, attempts + 1, seconds)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def send_email(request, user_email, receipt_id, project_id):
    subject = _(f'Чек оплаты проекта {project_id}')
    from_email = settings.DEFAULT_FROM_EMAIL

    context = {
        'subject': subject,
        'request': request,
        'receipt_id': receipt_id,
        'project_id': project_id,
    }

    callback_path = getattr(settings, 'BTCPAY_CROWDFUND_MAIL_RECEIPT_CONTEXT_CALLBACK', None)
    
    if callback_path:
        try:
            context_callback = import_string(callback_path)
            additional_context = context_callback(request)
            
            if isinstance(additional_context, dict):
                context.update(additional_context)
        except ImportError:
            raise ValueError('Invalid path for a callback. Please check your BTCPAY_CROWDFUND_MAIL_RECEIPT_CONTEXT_CALLBACK constant.')


    html_content = render_to_string(getattr(settings, 'BTCPAY_CROWDFUND_MAIL_RECEIPT_PAGE', 'BTCPayCrowdfunding/receipt-email.html'), context)
    text_content = strip_tags(html_content)
    send_mail(
        subject,
        text_content,
        from_email,
        [user_email], # Учитывая вашу связь ForeignKey
        fail_silently=False,
        html_message=html_content
    )


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