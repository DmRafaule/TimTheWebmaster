from django.shortcuts import render, get_object_or_404
from django.utils.translation import activate, get_language
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Post.models import Post
from User.models import User, Comment
from django.urls import reverse
from MyBlog import settings
from Main.models import Downloadable, Image
import re, json


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
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
        'media_root': media_root,
        'comments': Comment.objects.all(),
        'is_end': is_end
    }
    return render(request, f'Post/{category}_preview{forWho}.html', context=context)


def article_list(request):
    media_root = settings.MEDIA_URL
    context = {
        'articles': Post.objects.filter(type="Articles"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username', 'Guest')).first(),
    }
    return render(request, 'Post/article_list.html', context=context)


def news_list(request):
    media_root = settings.MEDIA_URL
    context = {
        'news': Post.objects.filter(type="News"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/news_list.html', context=context)


def proj_list(request):
    media_root = settings.MEDIA_URL
    context = {
        'projects': Post.objects.filter(type="Projects"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/proj_list.html', context=context)


def case_list(request):
    media_root = settings.MEDIA_URL
    context = {
        'cases': Post.objects.filter(type="Cases"),
        'media_root': media_root,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
    }
    return render(request, 'Post/case_list.html', context=context)


def case(request, post_slug):
    case = get_object_or_404(Post, slug=post_slug)
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    downloadables = Downloadable.objects.filter(type=case)
    images = Image.objects.filter(type=case)
    context = {
        'post': case,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
        'media_root': media_root,
        'domain_name': domain_name,
        'downloadables': downloadables,
        'images': images,
    }

    try:
        template = case.template.path
    except:
        template = 'Main/InProccess.html'

    return render(request, template, context=context)


def article(request, post_slug):
    article = get_object_or_404(Post, slug=post_slug)
    article.viewed = article.viewed + 1
    article.save()
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    downloadables = Downloadable.objects.filter(type=article)
    images = Image.objects.filter(type=article)
    context = {
        'post': article,
        'user': User.objects.filter(name=request.session.get('username','Guest')).first(),
        'comments': Comment.objects.filter(type=article).order_by('-timeCreated'),
        'comments_number': Comment.objects.filter(type=article).count(),
        'media_root': media_root,
        'domain_name': domain_name,
        'downloadables': downloadables,
        'images': images,
    }
    try:
        template = article.template.path
    except:
        template = 'Main/InProccess.html'

    return render(request, template, context=context)


def news(request, post_slug):
    news = get_object_or_404(Post, slug=post_slug)
    news.viewed = news.viewed + 1
    news.save()
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    downloadables = Downloadable.objects.filter(type=news)
    images = Image.objects.filter(type=news)
    context = {
        'post': news,
        'user': User.objects.filter(name=request.session.get('username', 'Guest')).first(),
        'comments': Comment.objects.filter(type=news).order_by('-timeCreated'),
        'comments_number': Comment.objects.filter(type=news).count(),
        'media_root': media_root,
        'domain_name': domain_name,
        'downloadables': downloadables,
        'images': images,
    }
    try:
        template = news.template.path
    except:
        template = 'Main/InProccess.html'

    return render(request, template, context=context)


def proj(request, post_slug):
    proj = get_object_or_404(Post, slug=post_slug)
    proj.viewed = proj.viewed + 1
    proj.save()
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    downloadables = Downloadable.objects.filter(type=proj)
    images = Image.objects.filter(type=proj)
    context = {
        'post': proj,
        'user': User.objects.filter(name=request.session.get('username', 'Guest')).first(),
        'comments': Comment.objects.filter(type=proj).order_by('-timeCreated'),
        'comments_number': Comment.objects.filter(type=proj).count(),
        'media_root': media_root,
        'domain_name': domain_name,
        'downloadables': downloadables,
        'images': images,
    }
    try:
        template = proj.template.path
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


def load_comment(request):
    media_root = settings.MEDIA_URL
    if request.method == 'POST':
        user = User.objects.filter(name=request.session.get('username', 'guest')).get()
        type = Post.objects.filter(slug=request.POST['post']).get()
        content = request.POST['about']
        comment = Comment(user=user, type=type, content=content)
        comment.save()
    context = {
        'com': comment,
        'user': user,
        'media_root': media_root,
    }
    return render(request, "Post/comment.html", context=context)


def remove_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        comment = Comment.objects.filter(id=comment_id).get()
        comment.delete()

    return render(request, "Post/comment.html")


def load_comments(request):
    media_root = settings.MEDIA_URL
    if request.method == 'POST':
        try:
            user = User.objects.filter(name=request.session.get('username', 'guest')).get()
        except:
            user = None
        number = request.POST.get('number', 5)
        offset = request.POST.get('offset', 0)
        type = Post.objects.filter(slug=request.POST['post']).get()
        comments = Comment.objects.filter(type=type).order_by('-timeCreated')[(int(offset)):(int(number)) + (int(offset))]

    context = {
        'comments': comments,
        'user': user,
        'media_root': media_root,
    }
    return render(request, "Post/comments.html", context=context)


def load_comments_by_user(request):
    media_root = settings.MEDIA_URL
    if request.method == 'POST':
        user = User.objects.filter(name=request.session.get('username')).get()
        number = request.POST.get('number', 5)
        offset = request.POST.get('offset', 0)
        comments = Comment.objects.filter(user=user).order_by('-timeCreated')[(int(offset)):(int(number)) + (int(offset))]

    context = {
        'comments': comments,
        'user': user,
        'media_root': media_root,
    }

    return render(request, "Post/comments.html", context=context)


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


def load_table_of_content(request):
    titles = json.loads(request.GET.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Post/table_of_content.html", context=context)
