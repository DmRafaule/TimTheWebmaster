from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.cache import cache
import re
from django.utils.translation import gettext as _
from .models import User
from Main.utils import initDefaults


def profile(request, user_slug):
    user = User.objects.filter(name=user_slug).first()
    context = initDefaults(request)
    context.update({'user': user})
    if (request.session["username"] == user_slug):
        return render(request, 'User/profile.html', context=context)
    else:
        return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/login")


def login(request):
    context = initDefaults(request)
    return render(request, 'User/login.html', context=context)


def logout(request):
    request.session.flush()
    cache.clear()
    return HttpResponseRedirect(f"/{request.LANGUAGE_CODE}/login")


def signup(request):
    context = initDefaults(request)
    return render(request, 'User/signup.html', context=context)


def login_verify(request):
    message = {
        'common': '',
        'username': '',
        'password': '',
    }
    status = 200
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        message['common']=_('✖ не могу войти')
        # username,email,password fields does not filled up
        if len(username) == 0:
            message['username']=_('⚠ пользователь пуст')
            status = 406
        if len(password) == 0:
            message['password']=_('⚠ пароль пуст')
            status = 406
        # Check if user already exist
        required_user = User.objects.filter(name=username)
        if required_user.exists():
            # Password does match
            if required_user.first().password == password:
                status = 200
                request.session["is_auth"] = True
                request.session["username"] = username
                message['common'] = _('✔ Вы успешно вошли, перенаправление ... ')
                message['username'] = _('✔ Хорошо')
                message['password'] = _('✔ Хорошо')
            else:
                message['password'] = _('⚠ Неправильный пароль')
                status = 406
        else:
            message['username'] = _('⚠ Такого пользователя не существует')
            status = 406

        return JsonResponse(message, status=status)


def signup_verify(request):
    message = {
        'common': '',
        'username': '',
        'email': '',
        'password': '',
        'repassword': '',
    }
    status = 200
    if request.method == 'POST':
        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeated_password = request.POST['repeated_password']
        about = request.POST['about']
        avatar = None
        try:
            avatar = request.FILES['file']
        except:
            avatar = None

        message['common']=_('✖ не могу зарегестрировать нового пользователя')
        # username,email,password fields does not filled up
        if len(username) == 0:
            message['username']=_('⚠ поле пользователя не заполнено')
            status = 406
        if len(email) == 0:
            message['email']=_('⚠ поле почты не заполнено')
            status = 406
        if len(password) == 0:
            message['password']=_('⚠ поле пароля не заполнено')
            status = 406
        # Check if user already exist
        if User.objects.filter(name=username).exists() or User.objects.filter(slug=slugify(username)).exists():
            message['username']=_('⚠ пользователь с таким именем уже существует')
            status = 406
        # Check if email already used
        if User.objects.filter(email=email).exists():
            message['email']=_('⚠ такая почта уже используется')
            status = 406
        # Check if username's length is big enough
        if len(username) < 3:
            message['username']=_('⚠ введённое имя слишком короткое')
            status = 406
        # Check if username's length not to big
        if len(username) > 25:
            message['username']=_('⚠ введённое имя слишком длинное')
            status = 406
        # Check if password length is big enough
        if len(password) < 6:
            message['password']=_('⚠ введённый пароль слишком короткий')
            status = 406
        # Password does not match
        if password != repeated_password:
            message['password']=_('⚠ пароль не совпадает')
            message['repassword']=_('⚠ пароль не совпадает')
            status = 406
        # Email addres does not right
        if not re.fullmatch(regex, email):
            message['email']=_('⚠ неправильный формат адреса почты')
            status = 406
        if status == 200:
            message['common'] = _('✔ вы успешно зарегестрировались, перенаправление')
            message['username'] = _('✔ Хорошо')
            message['email'] = _('✔ Хорошо')
            message['password'] = _('✔ Хорошо')
            message['repassword'] = _('✔ Хорошо')
            user = User(name=username, about=about, avatar=avatar, email=email, password=password)
            user.save()

        return JsonResponse(message, status=status)
    else:
        status = 403
        message['common'] = _("Ты, скользкий тип")
        message['username'] = _("Даже не пытайся")
        message['email'] = _("Или попытайся, всёравно")
        message['password'] = '¯\_(ツ)_/¯'
        message['repassword'] = ''
        return JsonResponse(message, status=status)
