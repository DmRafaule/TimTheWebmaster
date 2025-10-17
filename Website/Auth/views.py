from django.shortcuts import render
from Main.utils import initDefaults


def login(request):
    context = initDefaults(request)
    return render(request, 'Auth/login.html', context)

def logout(request):
    context = initDefaults(request)
    return render(request, 'Auth/logout.html', context)

def signup(request):
    context = initDefaults(request)
    return render(request, 'Auth/signup.html', context)