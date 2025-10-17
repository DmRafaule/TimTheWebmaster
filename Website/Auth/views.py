from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from allauth.account.views import SignupView, LoginView, LogoutView

from Main.utils import initDefaults
from .forms import Login, SignUp

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