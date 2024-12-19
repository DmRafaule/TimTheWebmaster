from django.shortcuts import render
from ShaderToy.models import Shader
from django.http import JsonResponse
from django.template.response import TemplateResponse
import Main.utils as U
import json


def tool_main(request):
    context = U.initDefaults(request)
    # Upload all examples shaders
    # Upload all user shaders
    return TemplateResponse(request, 'ShaderToy/main.html', context=context)


def save_shader(request):
    context = U.initDefaults(request)
    if request.method == 'POST':
        shader = Shader(
                user_id=request.session.session_key,
                name=request.POST['name'],
                shader_id=request.POST['shader_id'],
                fragment_src=request.POST['fragment_src'],
                vertex_src=request.POST['vertex_src'],
                default_geometry_data_indx=request.POST['default_geometry_data_indx'],
                render_mode=request.POST['render_mode'],
                bg=json.loads(request.POST['bg']),
                buffers=json.loads(json.dumps(request.POST['buffers'])),
                sizes=json.loads(json.dumps(request.POST['sizes'])),
        )
        shader.save()
        context = {
            'saves': [shader],
        }

    return render(request, 'ShaderToy/save.html', context=context)


def load_shader(request):
    context = U.initDefaults(request)
    if request.method == 'POST':
        shaders = Shader.objects.filter(user_id=request.session.session_key, is_for_library=False)
        context = {
            'saves': shaders,
        }

    return render(request, 'ShaderToy/save.html', context=context)


def load_library(request):
    context = U.initDefaults(request)
    if request.method == 'POST':
        shaders = Shader.objects.filter(is_for_library=True)
        context = {
            'saves': shaders,
        }

    return render(request, 'ShaderToy/save.html', context=context)


def remove_shader(request):
    if request.method == 'POST':
        shader_id = request.POST['shader_id']
        try:
            Shader.objects.get(shader_id=shader_id).delete()
        except ValueError:
            return JsonResponse({"message": "Не смог удалить"}, status=500)

    return JsonResponse({"message": "Удалено"}, status=200)


def get_shader(request):
    if request.method == 'POST':
        shader_id = request.POST['shader_id']
        shader = Shader.objects.get(shader_id=shader_id)
        if shader is None:
            return JsonResponse({"message": "Не могу найти шейдер"}, status=406)
        return JsonResponse({
            'fragment_src': shader.fragment_src,
            'vertex_src': shader.vertex_src,
            'dgd_indx': shader.default_geometry_data_indx,
            'render_mode': shader.render_mode,
            'bg': shader.bg,
            'buffers': shader.buffers,
            'sizes': shader.sizes,
        }, status=200)
