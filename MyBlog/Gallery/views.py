from django.shortcuts import render
from django.http import HttpResponse
import Main.utils as U
from Main.models import Image
from Post.models import Article
from .models import Image as GalleryImage
import json
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from datetime import datetime, date

COLS = 2
UPLOAD_SIZE = 4

def byDate(img):
    return datetime.strptime(img.timeCreated.date().strftime('%m/%d/%Y %I:%M %p'), '%m/%d/%Y %I:%M %p')


def gallery(request):
    context = U.initDefaults(request) 
    images = []
    # Get all images marked as ART
    images += Image.objects.filter(category=Image.ART)
    # Get all previews in articles
    for post in Article.objects.exclude(preview=''):
        images.append(Image(file=post.preview,timeCreated=post.timeCreated))
    # Get all images in gallery and combine them all
    images += GalleryImage.objects.all()
    images = sorted(images, key=byDate, reverse=True)
    # Create a paginator
    paginator = Paginator(images, UPLOAD_SIZE)
    page = int(request.GET.get('page', 1))
    if page > paginator.num_pages:
        return HttpResponse(request, status=404)
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
    if type == 'full':
        return render(request, 'Gallery/gallery-home.html', context=context)
    elif type == 'part':
        return render(request, 'Gallery/gallery-page.html', context=context)