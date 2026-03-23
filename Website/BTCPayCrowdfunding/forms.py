from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.apps import apps
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from functools import lru_cache


@lru_cache(maxsize=None)
def get_email_form():
    """
    Возвращает класс формы EmailForm, динамически привязанный к модели,
    указанной в настройках.
    """
    try:
        model_path = getattr(settings, 'BTCPAY_CROWDFUND_EMAIL_MODEL_TO_BIND', None)
        field_name = getattr(settings, 'BTCPAY_CROWDFUND_EMAIL_MODEL_FIELD', 'email')
        binded_model = apps.get_model(model_path)
    except Exception:
        raise ValueError("You did not provide the BTCPAY_CROWDFUND_EMAIL_MODEL_TO_BIND constant. See the documentation")

    currency_choices = getattr(settings, 'BTCPAY_CROWDFUND_CURRENCY_CHOICES', None)
    if currency_choices and len(currency_choices) > 1:
        field_currency = forms.ChoiceField(
                            required=True, 
                            label=_("Валюта"), 
                            widget=forms.RadioSelect(), 
                            choices=currency_choices, 
                            initial=currency_choices[0][0], 
                            help_text="In ISO 4217 standard")
    else:
        initial_cur = currency_choices[0][0] if currency_choices else 'USD'
        field_currency = forms.CharField(widget=forms.HiddenInput(), initial=initial_cur)

    donation_choices = getattr(settings, 'BTCPAY_CROWDFUND_DONATION_CHOICES', None)
    if donation_choices and len(donation_choices) > 1:
            field_donation = forms.ChoiceField(
                                required=True, 
                                label=_("Сумма"), 
                                widget=forms.RadioSelect(), 
                                choices=donation_choices,
                                initial=donation_choices[0][0])
    else:
        initial_don = donation_choices[0][0] if donation_choices else '1'
        field_donation = forms.CharField(widget=forms.HiddenInput(), initial=initial_don)

    class EmailForm(ModelForm):
        donation_currency = field_currency
        donation_choice = field_donation
        app_id = forms.CharField(required=True, widget=forms.HiddenInput())
        captcha = CaptchaField()

        class Meta:
            model = binded_model
            fields = [field_name, 'app_id', 'donation_currency', 'donation_choice']
            widgets = {
                field_name: forms.EmailInput(attrs={'placeholder': _('Твой Email адрес')}),
            }

    return EmailForm