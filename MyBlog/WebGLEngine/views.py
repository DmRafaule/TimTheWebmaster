from django.shortcuts import render


def main(request):
    return render(request, 'WebGLEngine/main.html')


def geometry_bg(request):
    return render(request, 'WebGLEngine/geometry_bg.html')


def testing(request):
    return render(request, 'WebGLEngine/testing.html')
