from django.shortcuts import render

import Main.utils as U


def admin(request):
    context = U.initDefaults(request)
    return render(request, 'Admin/admin.html', context=context)