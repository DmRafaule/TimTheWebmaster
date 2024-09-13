from django.shortcuts import render
from django.http import HttpResponse, Http404
import Main.utils as U
from .utils import getLatesImagesAll
import json
from django.utils.translation import gettext as _
from django.core.paginator import Paginator


COLS = 2
UPLOAD_SIZE = 4


def filterByTag(list, tags):
    new_list = []
    for image in list:
        counter = 0
        for tag_name in tags:
            for tag in image['tags']:
                if tag.name == tag_name:
                    counter += 1
        if counter == len(tags):
            new_list.append(image)

    if len(new_list) == 0:
        return None
    else:
        return new_list


def gallery(request):
    context = U.initDefaults(request) 
    images = getLatesImagesAll()
    
    tags = request.GET.getlist('tag', [])
    if len(tags) > 0:
        images = filterByTag(images, tags)
        if not images:
            raise Http404(images)
    # Create a paginator
    paginator = Paginator(images, UPLOAD_SIZE)
    page = int(request.GET.get('page', 1))
    if page > paginator.num_pages:
        raise Http404() 
    page_obj = paginator.get_page(page)
    type = request.GET.get('type', 'full') 
    # Resort images for masonry
    columns = []
    for i in range(0,COLS):
        columns.append([])
    for key in range(0,len(page_obj)):
        col_id = key % COLS
        columns[col_id].append(page_obj[key])
    
    context.update({'columns': columns})
    context.update({'num_pages': paginator.num_pages})
    context.update({'current_page': page})
    context.update({'page': page + 1})
    context.update({'current_tag': tags})
    context.update({'tags_json': json.dumps(tags)})
    if type == 'full':
        return render(request, 'Gallery/gallery-home.html', context=context)
    elif type == 'part':
        return render(request, 'Gallery/gallery-page.html', context=context)