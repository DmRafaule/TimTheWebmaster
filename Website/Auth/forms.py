from allauth.account.forms import LoginForm, SignupForm, ConfirmEmailVerificationCodeForm, ChangePasswordForm
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _

class Login(LoginForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        # Здесь можно добавить дополнительную валидацию, если нужно
        return cleaned_data

class SignUp(SignupForm):
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_again = cleaned_data.get("password2")
        if password and password_again and password != password_again:
            self.add_error('password2', _("Пароли не совпадают"))
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        # Можно здесь дополнительно сохранить поля, например:
        user.username = self.cleaned_data['username']
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

class EmailVerification(ConfirmEmailVerificationCodeForm):
    pass

class PasswordChange(ChangePasswordForm):
    captcha = CaptchaField()
    pass
