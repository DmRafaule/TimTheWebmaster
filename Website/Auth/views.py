from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from allauth.account.views import SignupView, LoginView, PasswordChangeView, PasswordResetView, PasswordResetFromKeyView
from allauth.account.forms import ResetPasswordForm, ResetPasswordKeyForm, SetPasswordForm
from allauth.account.models import EmailAddress
from allauth.account.internal.flows.email_verification import (
    send_verification_email_to_address,
)


from Main.utils import initDefaults
from .forms import Login, SignUp, EmailVerification, PasswordChange


@login_required
@require_GET
def profile(request):
    context = initDefaults(request)
    current_user = request.user
    context.update({'username': current_user.username})
    context.update({'email': current_user.email})
    context.update({'first_name': current_user.first_name})
    context.update({'last_name': current_user.last_name})
    context.update({'is_active': current_user.is_active})
    context.update({'is_staff': current_user.is_staff})
    context.update({'is_superuser': current_user.is_superuser})
    context.update({'date_joined': current_user.date_joined})
    context.update({'last_login': current_user.last_login})
    is_verified = EmailAddress.objects.filter(user=current_user, verified=True).exists()
    context.update({'is_verified': is_verified})
    return render(request, 'Auth/profile.html', context)

@login_required
def password_change(request):
    context = initDefaults(request)
    form_password_change = PasswordChange()
    context.update({'form_password_change': form_password_change})
    return render(request, 'Auth/password_change.html', context)

@require_GET
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = initDefaults(request)
    form_login = Login()
    context.update({'form_login': form_login})
    return render(request, 'Auth/login.html', context)

@login_required
def logout(request):
    context = initDefaults(request)
    return render(request, 'Auth/logout.html', context)

@require_GET
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = initDefaults(request)
    form_signup = SignUp()
    context.update({'form_signup': form_signup})
    return render(request, 'Auth/signup.html', context)

@login_required
def email_verify(request, verification_code=None):
    context = initDefaults(request)
    if request.method == "GET":
        if verification_code:
            form_verify = EmailVerification(initial={'code': verification_code})
            context.update({'verification_code': verification_code})
        else:
            form_verify = EmailVerification()
        context.update({'form_verify': form_verify})
        return render(request, 'Auth/email_verification.html', context)
    elif request.method == "POST":
        code_from_post = request.POST.get('code', verification_code)
        form_verify = EmailVerification(request.POST, code=code_from_post, user=request.user, email=request.user.email)
        if form_verify.is_valid():
            user = request.user
            email_address = EmailAddress.objects.filter(user=user, verified=False).first()
            if email_address:
                email_address.verified = True
                email_address.save()
            return redirect("profile")
        else:
            return render(request, 'Auth/email_verification.html', context, status=400)

@login_required
def send_email_verify(request):
    user = request.user
    email_address = EmailAddress.objects.filter(user=user, primary=True).first()
    if email_address and not email_address.verified:
        send_verification_email_to_address(request, email_address)
    else:
        pass
    return redirect('email_verify')

@require_GET
def password_reset(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = initDefaults(request)
    form_password_reset = ResetPasswordForm()
    context.update({'form_password_reset': form_password_reset})
    return render(request, 'Auth/password_reset.html', context)

@require_GET
def password_reset_done(request):
    context = initDefaults(request)
    return render(request, 'Auth/password_reset_done.html', context)

@require_GET
def password_reset_from_key_done(request):
    context = initDefaults(request)
    return render(request, 'Auth/password_reset_from_key_done.html', context)
    
class CustomSignupView(SignupView):
    def get_success_url(self):
        return reverse('signup')

    def get_form_class(self):
        return SignUp
    
    def form_invalid(self, form):
        return render(self.request, 'Auth/form.html', {'form_to_render': form}, status=400)

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('login')

    def get_form_class(self):
        return Login
    
    def form_invalid(self, form):
        return render(self.request, 'Auth/form.html', {'form_to_render': form}, status=400)

class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "Auth/password_reset_from_key.html"

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('profile')

    def get_form_class(self):
        return PasswordChange
    
    def form_invalid(self, form):
        return render(self.request, 'Auth/form.html', {'form_to_render': form}, status=400)