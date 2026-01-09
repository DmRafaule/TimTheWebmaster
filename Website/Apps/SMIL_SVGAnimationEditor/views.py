from django.shortcuts import render
from django.template.response import TemplateResponse
import Main.utils as U

# Create your views here.
def tool_main(request):
    context = U.initDefaults(request)
    # Upload all examples shaders
    # Upload all user shaders
    return TemplateResponse(request, 'SMIL_SVGAnimationEditor/main.html', context=context)
