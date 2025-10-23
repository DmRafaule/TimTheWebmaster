
from django.shortcuts import render
from django.apps import apps

from Main.utils import initDefaults
from Admin.decorators import superuser_required

@superuser_required
def admin(request):
    context = initDefaults(request)
    # Получить все доступные модели в проекте
    project_models = apps.get_models()
    models = []
    for model in project_models:
        # Определяем ко-во записей в БД
        num_records = len(model.objects.all())
        # Определяем имя приложения, которое содержит данную модель
        app_name = model.__module__
        app_name = app_name.split('.')
        app_name = app_name[0:len(app_name)-1]
        app_name = '.'.join(app_name)
        # Определяем время последней записи
        if num_records > 0:
            latest_record = model.objects.all().latest('pk')
        else:
            latest_record = None
        models.append({
            'name': model.__name__,
            'app': app_name,
            'last_edited': latest_record,
            'num_records': num_records
        })
    context.update({'models': models})

    return render(request, 'Admin/admin_home.html', context)

@superuser_required
def records(request):
    context = initDefaults(request)
    return render(request, 'Admin/admin_records.html', context)

@superuser_required
def record(request, model, pk):
    context = initDefaults(request)
    return render(request, 'Admin/admin_record.html', context)