from django.shortcuts import render
from django.http import JsonResponse
from Post.models import Post
from User.models import User
from .models import Comment
from MyBlog import settings
from django.utils.translation import gettext as _
import time

TRESHOLD = 60
COMMENT_DIFF_TIMER = 60


def send_comment_guesting(request):
    global COMMENT_DIFF_TIMER
    last_comment_time = request.session['time_since_last_comment'] = request.session.get('time_since_last_comment', time.time())
    if COMMENT_DIFF_TIMER >= TRESHOLD:
        last_comment_time = request.session['time_since_last_comment'] = time.time()
        COMMENT_DIFF_TIMER = int(time.time() - last_comment_time)
        media_root = settings.MEDIA_URL
        if request.method == 'POST':
            type = Post.objects.filter(slug=request.POST['post']).get()
            content = request.POST['about']
            username = request.POST['username']
            user_id = request.session.session_key
            comment = Comment(
                    anonymous_user_id=user_id,
                    anonymous_user_name=username,
                    type=type,
                    content=content
            )
            comment.save()
        context = {
            'com': comment,
            'media_root': media_root,
        }
        return render(request, "Comment/comment.html", context=context)
    else:
        COMMENT_DIFF_TIMER = int(time.time() - last_comment_time)
        return JsonResponse({"message": _("Нельзя спамить сообщениями!")}, status=403)


def send_comment_authorized(request):
    global COMMENT_DIFF_TIMER
    last_comment_time = request.session['time_since_last_comment'] = request.session.get('time_since_last_comment', time.time())
    if COMMENT_DIFF_TIMER >= TRESHOLD:
        last_comment_time = request.session['time_since_last_comment'] = time.time()
        COMMENT_DIFF_TIMER = int(time.time() - last_comment_time)
        media_root = settings.MEDIA_URL
        if request.method == 'POST':
            user = User.objects.filter(name=request.session.get('username')).get()
            type = Post.objects.filter(slug=request.POST['post']).get()
            content = request.POST['about']
            comment = Comment(user=user, type=type, content=content)
            comment.save()
        context = {
            'com': comment,
            'user': user,
            'media_root': media_root,
        }
        return render(request, "Comment/comment.html", context=context)
    else:
        COMMENT_DIFF_TIMER = int(time.time() - last_comment_time)
        return JsonResponse({"message": _("Нельзя спамить сообщениями!")}, status=403)


def prepare_user(request):
    data = {
            'isValid': False,
            'username': None,
            }
    if request.method == "GET":
        username = request.GET['username']
        data['isValid'] = True
        data['username'] = username

    return JsonResponse(data)


def remove_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        comment = Comment.objects.filter(id=comment_id).get()
        comment.delete()
        status = 200

    return JsonResponse({}, status=status)


def load_comments(request):
    try:
        user = User.objects.filter(name=request.session.get('username')).get()
    except:
        user = None

    media_root = settings.MEDIA_URL
    if request.method == 'POST':
        number = request.POST.get('number', 5)
        offset = request.POST.get('offset', 0)
        type = Post.objects.filter(slug=request.POST['post']).get()
        comments = Comment.objects.filter(type=type).order_by('-timeCreated')[(int(offset)):(int(number)) + (int(offset))]

    context = {
        'comments': comments,
        'user': user,
        'media_root': media_root,
    }
    return render(request, "Comment/comments.html", context=context)


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

    return render(request, "Comment/comments.html", context=context)
