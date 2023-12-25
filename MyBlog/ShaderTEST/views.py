from django.shortcuts import render
import Main.utils as U


def main_shader(request):
    context = U.initDefaults(request)
    return render(request, 'ShaderTEST/main_shader.html', context=context)
