from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponse
import Post.models as Post_M
from django.utils.translation import gettext as _
import Main.models as Main_M
import Main.utils as U
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator
from django.apps import apps
from django.template import loader
from django.db.models import Q
import json


max_el_in_related_post = 3

# Return only those elements which has all tags in them
def filterByTag(list, tags, threshold = None):
    new_list = []
    max_len = threshold or len(tags)
    for item in set(list.filter(tags__in=tags)):
        counter = 0
        for tag in tags:
            if item.tags.filter(name=tag):
                counter += 1
        if counter == max_len:
            new_list.append(item)

    if len(new_list) == 0:
        return None
    else:
        return new_list

def calculate_pages(total_items, items_per_page):
    if total_items <= 0 or items_per_page <= 0:
        raise ValueError("Both total_items and items_per_page must be positive integers.")
    
    return -(-total_items // items_per_page)  # Using ceiling division

class PostListView(TemplateView):

    model = Post_M.Category
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        context['category'] = self.category
        return context
    
    def get(self, request):
        website_conf = Main_M.Website.objects.get(is_current=True)
        context = self.get_context_data()
        # Defines order of loading posts. Recent of latest
        is_recent = self.request.GET.get('is_recent', 'true')
        if is_recent == 'true':
            order = '-timeCreated'
        else:
            order = 'timeCreated'
        # Resort posts by time of creation
        # Get the category by some quirks, later add coresponding field
        model = apps.get_model(f'Post.{self.category.categry_name}')
        posts = model.objects.filter(isPublished=True).order_by(order)
        # Get posts with the same tags in
        tags = request.GET.getlist('tag', [])
        tags_names = []
        if len(tags) > 0:
            # Search everywhere !!!
            tag_obj = Post_M.Tag.objects.filter(Q(name_ru__in=tags) | Q(name_en__in=tags) | Q(slug_ru__in=tags)  | Q(slug_en__in=tags))
            for key, tag in enumerate(tag_obj):
                tags[key] = tag.slug
            for key, tag in enumerate(tag_obj):
                tags_names.append(tag.name)
            if not tag_obj:
                raise Http404(tag_obj)
            posts = filterByTag(posts, tag_obj)
        # Create a paginator
        page = int(request.GET.get('page', 1))
        pages = calculate_pages(len(posts), website_conf.paginator_per_page_posts)
        if page > pages :
            raise Http404(page)
        page_obj = posts[(page-1)*website_conf.paginator_per_page_posts:page*website_conf.paginator_per_page_posts]
        type = request.GET.get('type', 'full') 
        # Choose which template to render
        # There are 2 modes
        # basic - display everything that possible from preview to views
        # simple - display only needes information, title, description, date published
        if self.category.categry_name == 'Tool':
            mode = self.request.GET.get('mode', 'list') + '--'    
        else:
            mode = self.request.GET.get('mode', 'basic') + '--'
        # Define specific (unique) preview templates
        for_who = self.request.GET.get('for_who', '')
        cat = "-" + self.category.categry_name.lower()
        if for_who != '':
            for_who = '-' + for_who
        # Update context data
        context.update({'displayTags': True})
        context.update({'posts': page_obj})
        context.update({'num_pages': pages})
        context.update({'current_page': page})
        context.update({'page': page + 1})
        context.update({'type': type})
        context.update({'mode': mode[:-2]})
        context.update({'is_recent': is_recent})
        context.update({'current_tag': tags})
        context.update({'current_tag_names': tags_names})
        context.update({'tags_json': json.dumps(tags)})
        if type == 'full':
            loaded_template = loader.get_template(f'Post/{mode}post_preview{for_who}{cat}.html')
            context.update({'doc': loaded_template.render(context, request)})
            return render(request, self.template_name, context)
        elif type == 'part':
            return render(request,f'Post/{mode}post_preview{for_who}{cat}.html',context=context)


def article(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)

    context = U.initDefaults(request)

    sim_post_doc = None
    # Post model's records must have at least 3 similar tags with this post
    sim_post = filterByTag(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_similar_articles)
    if sim_post is not None:
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
    tds = filterByTag(Post_M.TD.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_termins)
    if tds is not None:
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
    qas =  filterByTag(Post_M.QA.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_questions)
    if qas is not None:
        context.update({'qas': qas[:website_conf.max_displayed_questions]})

    return render(request, post.template.path, context=context)

def qa(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.QA, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    sim_post_doc = None
    related_articles = filterByTag(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_questions)
    if related_articles is not None:
        context.update({'posts': related_articles[:website_conf.max_displayed_questions]})
        loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
        sim_post_doc = loaded_template.render(context, request)
    
    context.update({'related_articles': sim_post_doc})

    if post.template:
        return render(request, post.template.path, context=context)
    else:
        return render(request, post.default_template, context=context)


def td(request, post_slug):
    website_conf = Main_M.Website.objects.get(is_current=True)
    post = get_object_or_404(Post_M.TD, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    sim_post_doc = None
    related_articles = filterByTag(Post_M.Article.objects.filter(Q(isPublished=True) & Q(tags__in=post.tags.all())), post.tags.all(), website_conf.threshold_related_termins)
    if related_articles is not None:
        context.update({'posts': related_articles[:website_conf.max_displayed_termins]})
        loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
        sim_post_doc = loaded_template.render(context, request)
    
    context.update({'related_articles': sim_post_doc})

    if post.template:
        return render(request, post.template.path, context=context)
    else:
        return render(request, post.default_template, context=context)


# Basicaly one browser one like for one article
def like_post(request):
    post_slug = request.POST['slug']
    isLiked = request.session.get("is_liked_" + post_slug, False)
    if not isLiked:
        post = get_object_or_404(Post_M.Post, slug=post_slug)
        post.likes = post.likes + 1
        post.save()
        request.session["is_liked_" + post_slug] = True
        data = {
            'likes': post.likes,
        }
        return JsonResponse(data)
    else:
        data = {
            'likes': _('Большое спасибо, но ты уже лайкнул)')
        }
        return JsonResponse(data)


# No checks for multiple shares, because I do not want it.
# I want as many as I could get
def share_post(request):
    post_slug = request.POST['slug']
    post = get_object_or_404(Post_M.Post, slug=post_slug)
    post.shares = post.shares + 1
    post.save()
    data = {
        'shares': post.shares,
    }
    return JsonResponse(data)