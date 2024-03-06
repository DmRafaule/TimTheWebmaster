from django.shortcuts import render


def main(request):
    return render(request, 'WebGLEngine/main.html')


def geometry_bg(request):
    return render(request, 'WebGLEngine/geometry_bg.html')


def home_gik(request):
    return render(request, 'WebGLEngine/home_gik.html')


def testing(request):
    return render(request, 'WebGLEngine/testing.html')
