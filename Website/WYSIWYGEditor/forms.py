from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from .models import PostTemplate


class PostTemplateForm(forms.ModelForm):
    class Meta:
        model = PostTemplate
        fields = ['filename', 'post_type', 'content', 'used_styles', 'used_scripts']
        localized_fields = ['template']
        labels = {
            "option": _("Как сохранить результат"),
        }
        widgets = {
            'filename': forms.TextInput(attrs={'placeholder': _('Название файла')}),
            'post_type': forms.RadioSelect(),
            'content': forms.HiddenInput,
            'used_styles': forms.HiddenInput,
            'used_scripts': forms.HiddenInput,
        }

    