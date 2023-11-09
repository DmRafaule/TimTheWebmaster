from django.http import JsonResponse
from django.shortcuts import render
from User.models import User, Message
from Post.models import Post
import re
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
    news = getLatest(3, "News")

    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
        'case': case,
        'article': article,
        'news': news,
    }
    return render(request, 'Main/home.html', context=context)


def about(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
    }
    return render(request, 'Main/about.html', context=context)


def contacts(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
    }
    return render(request, 'Main/contacts.html', context=context)


def services(request):
    user = User.objects.filter(name=request.session.get('username','Guest')).first() 
    media_root = settings.MEDIA_URL
    domain_name = settings.ALLOWED_HOSTS[0]
    context = {
        'user': user,
        'media_root': media_root,
        'domain_name': domain_name,
    }
    return render(request, 'Main/services.html', context=context)


def load_message(request):
    message = {
        'common': '',
        'username': _('обязательно'),
        'email': _('обязательно'),
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
    return render(request, 'Main/404.html', status=404)
