import os, re
import string

from bs4 import BeautifulSoup

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.template import loader
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import get_random_string

from .forms import PostTemplateForm
from .models import PostTemplate
from Website.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL
from Post.models import Tag
import Main.utils as U

def is_superuser_check(user):
    return user.is_superuser

def _gen_uid():
    return f"-uid--{get_random_string(24, allowed_chars=string.ascii_uppercase + string.digits + string.ascii_lowercase)}"

def _update_record_filename(record, form):
    provided_filename: str = record.filename
    provided_filename = re.sub(r'[^a-zA-Z0-9а-яА-Я._-]', '-', provided_filename).rstrip()
    uid_pos = provided_filename.find('-uid--')
    if uid_pos == -1:
        uid = _gen_uid()
    else:
        uid = ""
    provided_filename = provided_filename.replace(uid,'')
    suffics_insert_position = provided_filename.find('.html')
    if suffics_insert_position == -1:
        provided_filename = f"{provided_filename}{uid}.html"
    else:
        provided_filename = f"{provided_filename[:suffics_insert_position]}{uid}.html"
    new_filename = f"{provided_filename}"
    record.filename = new_filename

def _update_record_raw(record):
    try:
        existed_obj = PostTemplate.objects.get(filename=record.filename)
    except PostTemplate.DoesNotExist:
        existed_obj = None

    if existed_obj is not None:
        existed_obj.filename = record.filename
        existed_obj.content = record.content
        existed_obj.used_styles = record.used_styles
        existed_obj.used_scripts = record.used_scripts
        existed_obj.save()
    else:
        record.save()

def _update_record_content(content_old: str)->str:
    img_last_pos = 0
    while True:
        img_last_pos = content_old.find('dynamic_image', img_last_pos) 
        if img_last_pos == -1:
            break
        to_replace_start = content_old.find('src=', img_last_pos) + 4
        to_replace_end = content_old.find('data-src', to_replace_start)
        content_old = content_old[:to_replace_start] + f'\"{STATIC_URL}loading.svg\"' + content_old[to_replace_end:]
        img_last_pos = to_replace_end
    return content_old

def _update_record_template(request, record, path_to_template):
    loaded_template = loader.get_template(path_to_template)
    
    context = {
        'content': _update_record_content(record.content),
        'styles': record.used_styles,
        'scripts': record.used_scripts,
    }
    doc = loaded_template.render(context, request)
    
    path_to_file = os.path.join(MEDIA_ROOT, 'tools', PostTemplate.ROOT_DIR, record.filename)
    with open(path_to_file, 'w+', encoding='utf-8') as file:
        file.write( doc )
    
    try:
        existed_obj = PostTemplate.objects.get(filename=record.filename)
    except PostTemplate.DoesNotExist:
        existed_obj = None

    if existed_obj is not None:
        existed_obj.template = path_to_file
        existed_obj.save()
    else:
        record.template = path_to_file
        record.save()

@user_passes_test(is_superuser_check)
def tool_main(request):
    filename = request.GET.get('filename', None)
    context = U.initDefaults(request)
        
    if filename:
        file, is_created = PostTemplate.objects.get_or_create(filename=filename)
        if is_created:
            pass
        else:
            pass
        context.update({'filename': file.filename})
        context.update({'filepath': f"{MEDIA_URL}tools/{PostTemplate.ROOT_DIR}/{file.filename}"})
        ## Определяем сколько времени необходимо для прочтения
    
        soup = BeautifulSoup(file.content, features="lxml")
        text = soup.get_text()
        words_in_text = len(text.split())
        time_to_read = round(words_in_text/240)
        context.update({'time_to_read': time_to_read})
        context.update({'words': words_in_text})
        context.update({'file_size': len(text)})

    return TemplateResponse(request, 'WYSIWYGEditor/editor_home.html', context)
    
@require_POST
def delete_template(request):
    filename = request.POST.get('filename')
    template =  get_object_or_404(PostTemplate, filename=filename)
    template.delete()
    status = 200
    return HttpResponse('', status=status)

@require_GET
def upload_template(request):
    filename = request.GET.get('filename')
    template = get_object_or_404(PostTemplate, filename=filename) 
    status = 200
    return HttpResponse(template.content, status=status)

@require_GET
def list_templates(request):
    templates = PostTemplate.objects.all()
    context = {
        "templates": templates
    }
    return render(request, "WYSIWYGEditor/list_form.html", context=context)

@require_POST
def save_template(request):
    form = PostTemplateForm(request.POST)
    status = 503
    is_valid = form.is_valid()
    if is_valid:
        # Send back all entered text 
        record = form.save(commit=False)
        _update_record_filename(record, form)
        _update_record_raw(record)
        _update_record_template(request, record, 'Post/article_exmpl.html')

        status = 200
    else:
        status = 400


    return render(request, 'WYSIWYGEditor/save_form.html', context={
        'form_save': PostTemplateForm(initial={
            'filename': record.filename
        })
    }, status=status)

@require_GET
def save_form(request):
    filename = request.GET.get('filename')
    if filename:
        form = PostTemplateForm(initial={
            'filename': filename
        })
    else:
        form = PostTemplateForm()
    
    return render(request, 'WYSIWYGEditor/save_form_container.html', context={
        'form_save': form,
    })
