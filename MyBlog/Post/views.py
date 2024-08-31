from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
import Post.models as Post_M
from django.utils.translation import gettext as _
import Main.models as Main_M
import Main.utils as U
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator
from django.apps import apps
from django.template import loader
import json

max_el_in_related_post = 5
UPLOAD_SIZE = 4

class PostPreviewView(TemplateView):

    model = None
    context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        # Defines order of loading posts. Recent of latest
        is_recent = self.request.GET.get('is_recent')
        if is_recent == 'true':
            order = '-timeCreated'
        else:
            order = 'timeCreated'
        # Define how much to load
        number = self.request.GET.get('number', 1)
        # Define from which post to start count
        offset = self.request.GET.get('offset', 1)
        context.update({'posts': self.model.objects.filter(isPublished=True).order_by(order)[(int(offset)):(int(number)) + (int(offset))] })
        offset = int(offset) + int(number)
        length = self.model.objects.filter(isPublished=True).count()
        context.update({'length': length})

        return context

    def get(self, request):
        context = self.get_context_data()
        # Define how much data should be loaded on user screen
        # There are 2 modes
        # basic - display everything that possible from preview to views
        # simple - display only needes information, title, description, date published
        mode = self.request.GET.get('mode', 'basic') + '--'
        # Define specific (unique) preview templates
        for_who = self.request.GET.get('for_who', '')
        cat = "-" + self.request.GET.get('category', '')
        if for_who != '':
            for_who = '-' + for_who
        return render(
                request,
                f'Post/{mode}post_preview{for_who}{cat}.html',
                context=context)


def filterByTag(list, tags):
    new_list = []
    for item in set(list.filter(tags__in=tags)):
        counter = 0
        for tag in tags:
            if item.tags.filter(name=tag):
                counter += 1
        if counter == len(tags):
            new_list.append(item)

    if len(new_list) == 0:
        return None
    else:
        return new_list

class PostListView(TemplateView):

    model = Post_M.Category
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        context['category'] = self.category
        return context
    
    def get(self, request):
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
        if len(tags) > 0:
            tag_obj = Post_M.Tag.objects.filter(name__in=tags)
            if not tag_obj:
                raise Http404(tag_obj)
            posts = filterByTag(posts, tag_obj)
        # Create a paginator
        paginator = Paginator(posts, UPLOAD_SIZE)
        page = int(request.GET.get('page', 1))
        if page > paginator.num_pages :
            raise Http404(page)
        page_obj = paginator.get_page(page)
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
        context.update({'posts': page_obj})
        context.update({'num_pages': paginator.num_pages})
        context.update({'current_page': page})
        context.update({'page': page + 1})
        context.update({'type': type})
        context.update({'mode': mode[:-2]})
        context.update({'is_recent': is_recent})
        context.update({'current_tag': tags})
        context.update({'tags_json': json.dumps(tags)})
        if type == 'full':
            loaded_template = loader.get_template(f'Post/{mode}post_preview{for_who}{cat}.html')
            context.update({'doc': loaded_template.render(context, request)})
            return render(request, self.template_name, context)
        elif type == 'part':
            return render(request,f'Post/{mode}post_preview{for_who}{cat}.html',context=context)


def article(request, post_slug):
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template.path, context=context)


def news(request, post_slug):
    post = get_object_or_404(Post_M.News, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template, context=context)


def case(request, post_slug):
    post = get_object_or_404(Post_M.Case, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template, context=context)


def qa(request, post_slug):
    post = get_object_or_404(Post_M.QA, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    tags = post.tags.values_list('pk', flat=True)
    related_articles = Post_M.Article.objects.filter(tags__in=tags)
    context.update({'related_articles': set(related_articles[:max_el_in_related_post])})

    related_cases = Post_M.Case.objects.filter(tags__in=tags)
    context.update({'related_cases': set(related_cases[:max_el_in_related_post])})

    related_news = Post_M.News.objects.filter(tags__in=tags)
    context.update({'related_news': set(related_news[:max_el_in_related_post])})

    related_tools = Post_M.Tool.objects.filter(tags__in=tags)
    context.update({'related_tools': set(related_tools[:max_el_in_related_post])})

    return render(request, post.template, context=context)


def td(request, post_slug):
    post = get_object_or_404(Post_M.TD, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    tags = post.tags.values_list('pk', flat=True)
    related_articles = Post_M.Article.objects.filter(tags__in=tags)
    context.update({'related_articles': set(related_articles[:max_el_in_related_post])})

    related_cases = Post_M.Case.objects.filter(tags__in=tags)
    context.update({'related_cases': set(related_cases[:max_el_in_related_post])})

    related_news = Post_M.News.objects.filter(tags__in=tags)
    context.update({'related_news': set(related_news[:max_el_in_related_post])})

    related_tools = Post_M.Tool.objects.filter(tags__in=tags)
    context.update({'related_tools': set(related_tools[:max_el_in_related_post])})

    return render(request, post.template, context=context)


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