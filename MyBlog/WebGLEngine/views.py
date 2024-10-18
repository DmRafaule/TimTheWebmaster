from django.shortcuts import render
from Main import utils as U

def main(request):
    context = U.initDefaults(request)
    return render(request, 'WebGLEngine/main.html', context)


def geometry_bg(request):
    context = U.initDefaults(request)
    return render(request, 'WebGLEngine/geometry_bg.html', context)


def home_gik(request):
    context = U.initDefaults(request)
    return render(request, 'WebGLEngine/home_gik.html', context)


def testing(request):
    context = U.initDefaults(request)
    return render(request, 'WebGLEngine/testing.html', context)
