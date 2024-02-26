from django.shortcuts import render


def main(request):
    return render(request, 'Space091/main.html')
