from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from .models import Comment, Email


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': _('Твой Email адрес')}),
        }
    captcha = CaptchaField()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["url", "name", "rating", "message"]
        widgets = {
            'url': forms.HiddenInput,
            'rating': forms.HiddenInput,
            'name': forms.TextInput(attrs={'placeholder': _('Твоё имя')}),
            'message': forms.Textarea(attrs={'placeholder': _('Твоё сообщение')}),
        }
    captcha = CaptchaField()

class ReviewForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["rating", "url", "name", "message"]
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating_radiobtn', 'data-msg': _('Пожалуйста оцени мой инструмент (ಥ _ ಥ)')}),
            'url': forms.HiddenInput,
            'name': forms.TextInput(attrs={'placeholder': _('Твоё имя')}),
            'message': forms.Textarea(attrs={'placeholder': _('Твоё сообщение')}),
        }
    captcha = CaptchaField()
    