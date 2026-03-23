from django import template
from django.conf import settings
from django.utils.translation import get_language
from BTCPayCrowdfunding.models import BTCPayCrowdfundApp

register = template.Library()

@register.simple_tag
def isBTCPayCrowdfundingConnected(project_id):
    lookup_field = getattr(settings, 'BTCPAY_CROWDFUND_APP_LOOKUP_FIELD', 'project__slug')
    filter_kwargs = {lookup_field: project_id, 'language_code': get_language()}
    return BTCPayCrowdfundApp.objects.filter(**filter_kwargs).first()