from django.shortcuts import render


def buffer(request):
    return render(request, 'NotebookOnMarginalia/buffer.html')
