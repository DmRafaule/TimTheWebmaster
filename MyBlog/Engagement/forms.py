from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["url", "name", "message"]
        widgets = {
            'url': forms.HiddenInput,
            'name': forms.TextInput(attrs={'placeholder': _('Твоё имя')}),
            'message': forms.Textarea(attrs={'placeholder': _('Твоё сообщение')}),
        }
    captcha = CaptchaField()
    