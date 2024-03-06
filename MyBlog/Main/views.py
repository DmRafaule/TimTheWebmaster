from django.http import JsonResponse
from django.shortcuts import render
import Main.utils as U
import User.models as User_M
import re
import json
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


class MainView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        context['me_years'] = U.get_how_old_human_in_years('16/07/2000', "%d/%m/%Y")
        return context


def load_message(request):
    message = {
        'common': '',
        'username': '',
        'email': '',
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
            source = 'about'
            new_message = User_M.Message(source=source, name=username, email=email, content=about)
            new_message.save()

        return JsonResponse(message, status=status)
    else:
        status = 403
        message['common'] = _("Ты, скользкий тип")
        message['username'] = _("Даже не пытайся")
        message['email'] = _("Или попытайся, всёравно")
        return JsonResponse(message, status=status)


def page_not_found(request, exception):
    context = U.initDefaults(request)
    return render(request, 'Main/404.html', context=context, status=404)


def load_table_of_content(request):
    titles = json.loads(request.POST.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Main/table_of_content.html", context=context)
