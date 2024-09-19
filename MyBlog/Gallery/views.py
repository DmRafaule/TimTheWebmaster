from django.shortcuts import render
from django.http import HttpResponse, Http404
import Main.utils as U
from Post.models import Tag
from Main.models import Website
from .utils import getLatesImagesAll
import json
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q


def filterByTag(list, tags):
    new_list = []
    for image in list:
        counter = 0
        for tag_name in tags:
            for tag in image['tags']:
                if (tag.name_ru == tag_name) or (tag.name_en == tag_name) or (tag.slug_ru == tag_name) or (tag.slug_en == tag_name):
                    counter += 1
        if counter == len(tags):
            new_list.append(image)

    if len(new_list) == 0:
        return None
    else:
        return new_list


def gallery(request):
    website_conf = Website.objects.get(is_current=True)
    context = U.initDefaults(request) 
    images = getLatesImagesAll()
    
    tags = request.GET.getlist('tag', [])
    tags_names = []
    if len(tags) > 0:
        tag_obj = Tag.objects.filter(Q(name_ru__in=tags) | Q(name_en__in=tags) | Q(slug_ru__in=tags)  | Q(slug_en__in=tags))
        images = filterByTag(images, tags)
        for key, tag in enumerate(tag_obj):
                tags[key] = tag.slug
        for key, tag in enumerate(tag_obj):
                tags_names.append(tag.name)
        if not images:
            raise Http404(images)
    # Create a paginator
    paginator = Paginator(images, website_conf.paginator_per_page_gallery)
    page = int(request.GET.get('page', 1))
    if page > paginator.num_pages:
        raise Http404() 
    page_obj = paginator.get_page(page)
    type = request.GET.get('type', 'full') 
    # Resort images for masonry
    columns = []
    for i in range(0, website_conf.paginator_per_page_gallery_columns):
        columns.append([])
    for key in range(0,len(page_obj)):
        col_id = key % website_conf.paginator_per_page_gallery_columns
        columns[col_id].append(page_obj[key])
    
    context.update({'columns': columns})
    context.update({'num_pages': paginator.num_pages})
    context.update({'current_page': page})
    context.update({'page': page + 1})
    context.update({'current_tag': tags})
    context.update({'current_tag_names': tags_names})
    context.update({'tags_json': json.dumps(tags)})
    if type == 'full':
        return render(request, 'Gallery/gallery-home.html', context=context)
    elif type == 'part':
        return render(request, 'Gallery/gallery-page.html', context=context)