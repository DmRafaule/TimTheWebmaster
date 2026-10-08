from django.shortcuts import render
from django.template.response import TemplateResponse

from Main.utils import initDefaults


def tool_main(request):
    context = initDefaults(request)
    
    return TemplateResponse(request, 'NumberConverter/index.html', context=context)