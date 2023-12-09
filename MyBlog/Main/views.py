from django.http import JsonResponse
from django.shortcuts import render
from User.models import User, Message
from Post.models import Post
import re
import json
from MyBlog import settings
from django.utils.translation import gettext as _


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


def home(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    # latest article
    article = Post.objects.filter(type='Articles', isPublished=True).latest('timeCreated')
    # latest case
    case = Post.objects.filter(type='Cases', isPublished=True).latest('timeCreated')
    # 3 newest news
    news = getLatest(1, "News")
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += news

    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
        'case': case,
        'article': article,
        'news': news,
        'popular_posts': popular_posts,
    }
    return render(request, 'Main/home.html', context=context)


def about(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    news = getLatest(1, "News")
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += news
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    return render(request, 'Main/about.html', context=context)


def contacts(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    news = getLatest(1, "News")
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += news
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    return render(request, 'Main/contacts.html', context=context)


def services(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    news = getLatest(1, "News")
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += news
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    return render(request, 'Main/services.html', context=context)


def load_message(request):
    message = {
        'common': '',
        'username': _(''),
        'email': _(''),
    }
    status = 200
    if request.method == 'POST':
        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        username = request.POST['username']
        email = request.POST['email']
        about = request.POST['about']

        message['common']=_('✖ не могу отправить сообщение')
        # username,email,password fields does not filled up
        if len(username) == 0:
            message['username']=_('⚠ поле пользователя не заполнено')
            status = 406
        if len(email) == 0:
            message['email']=_('⚠ поле почты не заполнено')
            status = 406
        # Check if username's length is big enough
        if len(username) < 3:
            message['username']=_('⚠ введённое имя слишком короткое')
            status = 406
        # Check if username's length not to big
        if len(username) > 25:
            message['username']=_('⚠ введённое имя слишком длинное')
            status = 406
        # Email addres does not right
        if not re.fullmatch(regex, email):
            message['email']=_('⚠ введённый адрес почты некорректен')
            status = 406
        if status == 200:
            message['common'] = _('✔ вы успешно отправили сообщение')
            message['username'] = _('✔ Хорошо')
            message['email'] = _('✔ Хорошо')
            new_message = Message(name=username, email=email, content=about)
            new_message.save()

        return JsonResponse(message, status=status)
    else:
        status = 403
        message['common'] = _("Ты, скользкий тип")
        message['username'] = _("Даже не пытайся")
        message['email'] = _("Или попытайся, всёравно")
        return JsonResponse(message, status=status)


def page_not_found(request, exception):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    popular_posts = getLatest(1, "Articles")
    popular_posts += getLatest(1, "Cases")
    popular_posts += getLatest(1, "News")
    context = {
        'user': user,
        'media_root': media_root,
        'popular_posts': popular_posts,
    }

    return render(request, 'Main/404.html', context=context, status=404)


def load_table_of_content(request):
    titles = json.loads(request.GET.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Main/table_of_content.html", context=context)


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
        'is_end': is_end
    }
    return render(request, f'Main/{category}_preview{forWho}.html', context=context)
