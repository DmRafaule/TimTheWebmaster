from django.shortcuts import render, get_object_or_404
from django.utils.translation import activate, get_language
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Post.models import Post
from User.models import User
from Comment.models import Comment
from MyBlog import settings
from Main.models import Downloadable, Image
import json


def getLatest(number, type):
    new_cases = list()
    cases = Post.objects.filter(type=type, isPublished=True)
    if (len(cases) > number):
        case = cases.latest('timeUpdated')
        for i in range(0, number):
            new_cases.append(case)
            cases = cases.exclude(id=case.id)
            case = cases.latest('timeUpdated')

    return new_cases


def load_post_preview(request):
    media_root = settings.MEDIA_URL
    number = request.GET.get('number', 1)
    offset = request.GET.get('offset', 1)
    forWho = request.GET.get('forWho', '')
    if forWho != '':
        forWho = '-' + forWho
    category = request.GET.get('category', 'Articles')
    # Take published, in one category, newest first and just slice of available posts
    loadedArticles = Post.objects.filter(type=category, isPublished=True).order_by('-timeCreated')[(int(offset)):(int(number)) + (int(offset))]
    offset = int(offset) + int(number)
    length = Post.objects.filter(type=category, isPublished=True).count()
    category = category.lower()
    is_end = False
    if (length <= int(offset) or length == 0):
        is_end = True
    context = {
        'posts': loadedArticles,
        'user': User.objects.filter(name=request.session.get('username', 'Guest')).first(),
        'media_root': media_root,
        'is_end': is_end
    }
    return render(request, f'Post/{category}_preview{forWho}.html', context=context)


def article_list(request):
    media_root = settings.MEDIA_URL
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'popular_posts': popular_posts,
        'articles': Post.objects.filter(type="Articles"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username', 'Guest')).first(),
    }
    return render(request, 'Post/article_list.html', context=context)


def news_list(request):
    media_root = settings.MEDIA_URL
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'popular_posts': popular_posts,
        'news': Post.objects.filter(type="News"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/news_list.html', context=context)


def proj_list(request):
    media_root = settings.MEDIA_URL
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'popular_posts': popular_posts,
        'projects': Post.objects.filter(type="Projects"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/proj_list.html', context=context)


def case_list(request):
    media_root = settings.MEDIA_URL
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'popular_posts': popular_posts,
        'cases': Post.objects.filter(type="Cases"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/case_list.html', context=context)


def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    downloadables = Downloadable.objects.filter(type=post)
    images = Image.objects.filter(type=post)
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'popular_posts': popular_posts,
        'post': post,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
        'comments': Comment.objects.filter(type=post).order_by('-timeCreated'),
        'comments_number': Comment.objects.filter(type=post).count(),
        'media_root': media_root,
        'domain_name': domain_name,
        'downloadables': downloadables,
        'images': images,
    }
    try:
        template = post.template.path
    except:
        template = 'Main/InProccess.html'

    return render(request, template, context=context)


def CheckIdInRangeAndReturnValidOnError(id, size):
    min = 1
    max = size
    rang = (1 + max - min)
    id = ((((id - min) % rang) + rang) % rang) + min
    return id


def load_case(request):
    cases = Post.objects.filter(type="Cases", isPublished=True)
    cases_number = cases.last().id
    mod = int(request.GET.get('id'))
    requested_id = request.session.get("case_id", 1)
    request.session["case_id"] = requested_id

    # find requested query in database
    while True:
        try:
            requested_id = requested_id + mod
            requested_id = CheckIdInRangeAndReturnValidOnError(requested_id, cases_number)
            case_curr = cases.get(id=requested_id)
            break
        except:
            request.session["case_id"] = request.session.get("case_id") + mod

    # find prev query in database
    requested_id = case_curr.id
    while True:
        try:
            requested_id = requested_id - 1
            requested_id = CheckIdInRangeAndReturnValidOnError(requested_id, cases_number)
            case_prev = cases.get(id=requested_id)
            break
        except:
            pass

    # find next query in database
    requested_id = case_curr.id
    while True:
        try:
            requested_id = requested_id + 1
            requested_id = CheckIdInRangeAndReturnValidOnError(requested_id, cases_number)
            case_next = cases.get(id=requested_id)
            break
        except:
            pass

    request.session["case_id"] = request.session.get("case_id") + mod

    media_root = settings.MEDIA_URL
    context = {
        'media_root': media_root,
        "case_curr": case_curr,
        "case_next": case_next,
        "case_prev": case_prev,
    }
    return render(request, 'Post/case_preview.html', context=context)


# Basicaly one browser one like for one article
def like_post(request):
    post_slug = request.POST['slug']
    isLiked = request.session.get("is_liked_" + post_slug, False)
    if not isLiked:
        post = get_object_or_404(Post, slug=post_slug)
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
    post = get_object_or_404(Post, slug=post_slug)
    post.shares = post.shares + 1
    post.save()
    data = {
        'shares': post.shares,
    }
    return JsonResponse(data)
