from django.shortcuts import render
import Main.utils as U
import Gallery.utils as GU
import json
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .forms import FeedbackForm
from MyBlog.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from django.core.mail import send_mail
from Post.models import Tool, Article
from django.template import loader


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

def home(request):
    context = U.initDefaults(request)
    internal_tools = Tool.objects.filter(type=Tool.INTERNAL)
    most_popular_article = [U.get_most_popular_post()]
    news = U.get_posts_by_tag('news', Article)
    latest_news = U.get_latest_post(3, news)
    post_series = U.get_posts_by_tag('search-result-parser-series', Article)
    latest_post_series = U.get_latest_post(2, post_series)
    latest_images = GU.getLatesImagesAll()[:3]
    my_resources = [
        {
            'tag': 'CLI',
            'title': _('Командная строка'),
            'objs': []
        },
        {
            'tag': 'GUI',
            'title': _('С графическим интерфейсом'),
            'objs': []
        },
        {
            'tag': 'bot',
            'title': _('Боты'),
            'objs': []
        },
        {
            'tag': 'scraper',
            'title': _('Парсеры'),
            'objs': []
        },
        {
            'tag': 'script',
            'title': _('Скрипты'),
            'objs': []
        }
    ]
    for resource in my_resources:
        objs = U.get_posts_by_tag(resource['tag'], Tool)
        print(objs)
        resource['objs'] = U.get_latest_post(3, objs)

    other_articles = [
        {
            'tag': 'django',
            'title': _('Джанго'),
            'objs': []
        },
        {
            'tag': 'bot',
            'title': _('Боты'),
            'objs': []
        },
        {
            'tag': 'history',
            'title': _('История'),
            'objs': []
        },
        {
            'tag': 'backend',
            'title': _('Бэкенд'),
            'objs': []
        },
        {
            'tag': 'react',
            'title': _('Реакт'),
            'objs': []
        }
    ]
    for resource in other_articles:
        objs = U.get_posts_by_tag(resource['tag'], Article)
        resource['objs'] = U.get_latest_post(2, objs)
    
    context.update({'posts': internal_tools})
    context.update({'current_tag': ''})
    loaded_template = loader.get_template(f'Post/list--post_preview-tool.html')
    context.update({'internal_tools': loaded_template.render(context, request)})
    
    context.update({'posts': most_popular_article})
    loaded_template = loader.get_template(f'Post/basic--post_preview-article.html')
    context.update({'most_popular_article': loaded_template.render(context, request)})

    context.update({'posts': latest_news})
    loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
    context.update({'latest_news': loaded_template.render(context, request)})

    context.update({'posts': latest_post_series})
    context.update({'series_tag': 'search-result-parser-series'})
    loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
    context.update({'latest_post_series': loaded_template.render(context, request)})

    my_res = []
    for res in my_resources:
        if len(res['objs']) > 0:
            context.update({'posts': res['objs']})
            loaded_template = loader.get_template(f'Post/list--post_preview-tool.html')
            res['objs'] = loaded_template.render(context, request)
            my_res.append(res)
    context.update({'my_resources': my_res})

    oth_art = []
    for res in other_articles:
        if len(res['objs']) > 0:
            context.update({'posts': res['objs']})
            loaded_template = loader.get_template(f'Post/basic--post_preview-article.html')
            res['objs'] = loaded_template.render(context, request)
            oth_art.append(res)
    context.update({'other_articles': oth_art})

    context.update({'latest_images': latest_images})

    return render(request, 'Main/home.html', context=context)

def page_not_found(request, exception):
    context = U.initDefaults(request)
    return render(request, 'Main/404.html', context=context, status=404)

def load_table_of_content(request):
    titles = json.loads(request.POST.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Main/table_of_content.html", context=context)
