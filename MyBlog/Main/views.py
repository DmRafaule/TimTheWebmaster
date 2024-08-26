from django.shortcuts import render
import Main.utils as U
import json
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .forms import FeedbackForm
from MyBlog.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from django.core.mail import send_mail


class MainView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        context.update({'me_years': U.get_how_old_human_in_years('16/07/2000', "%d/%m/%Y")})
        
        form = FeedbackForm()
        context.update({'form': form})
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(self.request.POST)
        context = super(MainView, self).get_context_data(**kwargs)
        context = U.initDefaults(self.request)

        if form.is_valid():
            subject = f'{form.cleaned_data.get("username")} | {form.cleaned_data.get("email")}'
            message = f'{form.cleaned_data.get("message")}'
            send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[DEFAULT_TO_EMAIL])
            context.update({'feedback_message': _('✔ Вы успешно отправили сообщение')})
        else:
            context.update({'feedback_message': _('✗ Возникла ошибка при отправке формы')})

        
        context.update({'me_years': U.get_how_old_human_in_years('16/07/2000', "%d/%m/%Y")})
        context.update({'form': form})
    
        return render(request, self.template_name, context=context)


def page_not_found(request, exception):
    context = U.initDefaults(request)
    return render(request, 'Main/404.html', context=context, status=404)

def load_table_of_content(request):
    titles = json.loads(request.POST.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Main/table_of_content.html", context=context)
