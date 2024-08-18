from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField


class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=25, min_length=3, widget=forms.TextInput(attrs={'placeholder': _('Имя')}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': _('Почта')}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _('Твоё сообщение')}))
    captcha = CaptchaField()