from django.shortcuts import render
import Main.utils as U
from .forms import PostTemplateForm
from .models import PostTemplate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template import loader
from MyBlog.settings import MEDIA_ROOT, MEDIA_URL
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse
from Post.models import Tag
import os
from django.contrib.auth.decorators import login_required


def _initPostEditorContext(request):
    context = U.initDefaults(request)
        
    form = PostTemplateForm()
    context.update({'form_save': form})
    
    return context

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
        existed_obj.option = record.option
        existed_obj.save()
    else:
        record.save()

def _update_record_template(request, record, path_to_template):
    loaded_template = loader.get_template(path_to_template)
    context = {
        'content': record.content,
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

def _get_option_name(option):
        return PostTemplate.OPTIONS[option]

def tool_main(request):
    context = _initPostEditorContext(request)
    quilljs_tag = Tag.objects.get(slug_en='quilljs')
    quilljs_module_tag = Tag.objects.get(slug_en='quill-module')
    context.update({'quilljs_tag': quilljs_tag.slug})
    context.update({'quilljs_module_tag': quilljs_module_tag.slug})
    return TemplateResponse(request, 'PostEditor/editor_home.html', context)
    
@login_required
def templates_list(request):
    user = User.objects.get(username=request.user)
    msg = _('✗ Возникла ошибка при получении списка')
    status = 503
    templates = []
    templates_query = PostTemplate.objects.filter(user=user)
    if len(templates_query) > 0:
        templates_query = templates_query.order_by('-timeUpdated')
        templates_values = templates_query.values('filename', 'template', 'option')
        templates = list(templates_values)
        for template in templates:
            path = os.path.join(MEDIA_URL, 'tools', PostTemplate.ROOT_DIR, template['filename'])
            template['template'] =  path
            template['option'] = _get_option_name(template['option'])
        status = 200
        msg = _('✔ Список шаблонов успешно получен')
    else:
        msg = _('✗ Список шаблонов пуст')

    return JsonResponse({'templates': templates, 'msg': msg}, status=status)

@login_required
def delete_template(request):
    msg = _('✗ Не удалось удалить шаблон')
    status = 503
    if request.method == 'POST':
        filename = request.POST.get('filename')
        template = PostTemplate.objects.get(filename=filename)
        template.delete()
        status = 200
        msg = _('✔ Шаблон успешно удалён')
    else:
        msg = _('✗ Только POST запросы обрабатываются')
    
    return JsonResponse({'msg': msg}, status=status)

@login_required
def upload_template(request):
    user = User.objects.get(username=request.user)
    msg = _('✗ Не удалось загрузить шаблон')
    status = 503
    if request.method == 'POST':
        try:
            filename = request.POST.get('filename')
            template = PostTemplate.objects.get(user=user, filename=filename)
            status = 200
            msg = _('✔ Шаблон получен')
        except PostTemplate.DoesNotExist:
            msg = _('✗ Такого файла больше не существует')
    else:
        msg = _('✗ Только POST запросы обрабатываются')

    return JsonResponse({'content': template.content, 'msg': msg}, status=status)

@login_required
def save_template(request):
    form = PostTemplateForm(request.POST)
    msg = _('✗ Возникла ошибка при сохранении')
    status = 503
    is_valid = form.is_valid()
    if is_valid and request.user.is_authenticated:
        # Send back all entered text 
        record = form.save(commit=False)
        record.user = User.objects.get(username=request.user)
        match record.option:
            case PostTemplate.RAW:
                _update_record_raw(record)
            case PostTemplate.ARTICLE_POST:
                _update_record_raw(record)
                _update_record_template(request, record, 'Post/article_exmpl.html')
            case PostTemplate.TERMIN_POST:
                _update_record_raw(record)
                _update_record_template(request, record, 'Post/td_exmpl.html')
            case PostTemplate.QUESTION_POST:
                _update_record_raw(record)
                _update_record_template(request, record, 'Post/qa_exmpl.html')
        msg = _('✔ Успешное сохранение')
        status = 200
    else:
        msg = _('✗ Форма не валидна')


    return JsonResponse({'msg': msg}, status=status)