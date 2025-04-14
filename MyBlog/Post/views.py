from bs4 import BeautifulSoup

from django.template import loader
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.template.response import TemplateResponse

import Post.models as Post_M
import Main.models as Main_M
import Main.utils as U


def article(request, post_slug):
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    downloadables = post.media.filter_by_lang().filter(type=Main_M.Media.RAW_FILE).order_by('timeCreated')
    images = post.media.filter_by_lang().filter(type=Main_M.Media.IMAGE).order_by('timeCreated')
    videos = post.media.filter_by_lang().filter(type=Main_M.Media.VIDEO).order_by('timeCreated')
    pdfs = post.media.filter_by_lang().filter(type=Main_M.Media.PDF).order_by('timeCreated')
    audios = post.media.filter_by_lang().filter(type=Main_M.Media.PDF).order_by('timeCreated')

    context = U.initDefaults(request)

    context.update({'post': post})
    # Get time to read
    with post.template.open('r') as file:
        soup = BeautifulSoup(file.read(), features="lxml")
        text = soup.get_text()
        words_in_text = len(text.split())
        time_to_read = round(words_in_text/240)
    context.update({'time_to_read': time_to_read})
    
    ### Get next and previos posts
    previous_id=Post_M.Article.objects.filter(
         id__lt=post.id,
     ).order_by("-id").values_list("id")[:1],
    next_id=Post_M.Article.objects.filter(
         id__gt=post.id,
    ).order_by("id").values_list("id")[:1]
    # Check if there is no next element
    if len(next_id) > 0:
        id = next_id[0][0]
        next_post = Post_M.Article.objects.get(id=id)
        context.update({'next_post': next_post})
    # Check if there is no prev element
    if len(previous_id[0]) > 0:
        id = previous_id[0][0][0]
        prev_post = Post_M.Article.objects.get(id=id)
        context.update({'prev_post': prev_post})
    ###
    
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    context.update({'videos': videos})
    context.update({'pdfs': pdfs})
    context.update({'audios': audios})

    return TemplateResponse(request, post.template.path, context=context)

def tool(request, post_slug):
    post = get_object_or_404(Post_M.Tool, slug=post_slug)
    downloadables = post.media.filter_by_lang().filter(type=Main_M.Media.RAW_FILE).order_by('timeCreated')
    images = post.media.filter_by_lang().filter(type=Main_M.Media.IMAGE).order_by('timeCreated')
    videos = post.media.filter_by_lang().filter(type=Main_M.Media.VIDEO).order_by('timeCreated')
    pdfs = post.media.filter_by_lang().filter(type=Main_M.Media.PDF).order_by('timeCreated')
    audios = post.media.filter_by_lang().filter(type=Main_M.Media.PDF).order_by('timeCreated')

    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    context.update({'videos': videos})
    context.update({'pdfs': pdfs})
    context.update({'audios': audios})

    sim_post_doc = None
    related_tools = list(set(U.getAllWithTags(Post_M.Tool.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())).exclude(slug=post_slug), post.tags.all(), 3)))
    if len(related_tools) > 0:
        context.update({'posts': related_tools[:3]})
        loaded_template = loader.get_template(f'Post/basic--post_preview-tool.html')
        sim_post_doc = loaded_template.render(context, request) 
    context.update({'related_tools': sim_post_doc})

    # Get latest notes about this tool
    tool_tags = Post_M.Tag.objects.filter(slug_en=post_slug)
    if len(tool_tags) > 0:
        posts = U.getAllWithTags(Post_M.Note.objects.filter(isPublished=True), [tool_tags[0]])[:3]
        context.update({'tool_tag': tool_tags[0].slug})
        context.update({'posts': posts})
        loaded_template = loader.get_template(f'Post/basic--post_preview-note.html')
        context.update({'latest_notes': loaded_template.render(context, request)})
    
    # Get used platforms
    context.update({'platforms': post.platforms.all()})

    if post.template:
        return TemplateResponse(request, post.template.path, context=context)
    else:
        return TemplateResponse(request, post.default_template, context=context)