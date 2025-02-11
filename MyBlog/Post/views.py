import Post.models as Post_M
import Main.models as Main_M
import Main.utils as U
from django.template import loader
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse


def article(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)

    context = U.initDefaults(request)

    sim_post_doc = None
    # Post model's records must have at least 3 similar tags with this post
    sim_post = U.getAllWithTags(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())).exclude(slug=post_slug), post.tags.all(), website_conf.threshold_similar_articles)
    if len(sim_post) > 0:
        context.update({'posts': sim_post[:website_conf.max_displayed_similar_articles]})
        loaded_template = loader.get_template(f'Post/basic--post_preview-article.html')
        sim_post_doc = loaded_template.render(context, request)

    context.update({'post': post})
    context.update({'sim_post_doc': sim_post_doc})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    

    with open(post.template.path, 'r', encoding='utf-8') as file:
        html_str = U.page_to_string(file.read()).lower()
    
    # TD model's record must have at leas 2 similar tags with post tags and be published
    tds = U.getAllWithTags(Post_M.TD.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_termins)
    if len(tds) > 0:
        tds_to_use = []
        for td in tds:
            phrases = td.key_phrases.split(',')
            # Procceed next if only key_phrased field is not empty
            if phrases[0] != '':
                for phrase in phrases:
                    # If occurence in text was found the propagate this TD record
                    if html_str.find(phrase) != -1:
                        tds_to_use.append(td)

        context.update({'tds': list(set(tds_to_use))[:website_conf.max_displayed_termins]})

    # QA model's record must have at leas 3 similar tags with post tags and be published
    qas =  U.getAllWithTags(Post_M.QA.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_questions)
    if len(qas) > 0:
        context.update({'qas': qas[:website_conf.max_displayed_questions]})

    return TemplateResponse(request, post.template.path, context=context)

def qa(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.QA, slug=post_slug)
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    sim_post_doc = None
    related_articles = U.getAllWithTags(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_questions)
    if len(related_articles) > 0:
        context.update({'posts': related_articles[:website_conf.max_displayed_questions]})
        loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
        sim_post_doc = loaded_template.render(context, request)
    context.update({'related_articles': sim_post_doc})

    if post.template:
        return TemplateResponse(request, post.template.path, context=context)
    else:
        return TemplateResponse(request, post.default_template, context=context)

def td(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.TD, slug=post_slug)
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    sim_post_doc = None
    related_articles = U.getAllWithTags(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_termins)
    if len(related_articles) > 0:
        context.update({'posts': related_articles[:website_conf.max_displayed_termins]})
        loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
        sim_post_doc = loaded_template.render(context, request) 
    context.update({'related_articles': sim_post_doc})

    if post.template:
        return TemplateResponse(request, post.template.path, context=context)
    else:
        return TemplateResponse(request, post.default_template, context=context)

def tool(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.Tool, slug=post_slug)
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    sim_post_doc = None
    related_tools = U.getAllWithTags(Post_M.Tool.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())).exclude(slug=post_slug), post.tags.all(), 3)
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