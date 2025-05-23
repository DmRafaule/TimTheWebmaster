from django.shortcuts import render
import Main.utils as U
from .models import Website
import json
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from .forms import FeedbackForm
from MyBlog.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from django.core.mail import send_mail
from Post.models import Tool, Article, Tag, Note
from bs4 import BeautifulSoup
from Engagement.models import Comment


class MainView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        
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

        
        context.update({'form': form})
    
        return render(request, self.template_name, context=context)

def countWords_f(path):
    with open(path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, features='lxml')
        text_blocks = ''
        for el in soup.find_all('div', class_='text'):
            text_blocks += el.getText()
        for el in soup.find_all(class_='title'):
            text_blocks += el.getText()
        for el in soup.find_all(class_='paragraph'):
            text_blocks += el.getText()
        for el in soup.find_all(class_='list'):
            text_blocks += el.getText()
        html_str_words = text_blocks.lower().split()
    
        return html_str_words


def about(request):
    context = U.initDefaults(request)
    context.update({'me_years': U.get_how_old_human_in_years('16/07/2000', "%d/%m/%Y")})
    more_about_me_tags = Tag.objects.filter(slug_en='gamedev')
    if len(more_about_me_tags) > 0:
        more_about_me_tag = more_about_me_tags[0].slug
    else:
        more_about_me_tag = None
    
    context.update({'more_about_me_tag': more_about_me_tag})
    return render(request, 'Main/about.html', context=context)

def home(request):
    website_conf = Website.objects.get(is_current=True)

    context = U.initDefaults(request)
    context.update({'displayTags': False})
    internal_tool_tag = Tag.objects.get(slug_en='internal-tool')
    internal_tools = website_conf.choosen_tools.all()[:website_conf.max_displayed_inner_tools_on_home]
    most_popular_article = U.get_latest_post(3, Article.objects.all())

    news = U.get_posts_by_tag('News', Article)
    latest_news = U.get_latest_post(website_conf.max_displayed_news_on_home, news)
    latest_notes = U.get_latest_post(website_conf.max_displayed_notes_on_home, Note.objects.all())

    my_resources = []
    for tag in website_conf.my_resources_choosen_tags_on_home.all():
        objs = U.get_posts_by_tag(tag.name, Tool)
        my_resources.append({
            'tag': tag.slug,
            'title': tag.name,
            'objs': U.get_latest_post(website_conf.min_displayed_my_resources, objs)
        })

    other_articles = []
    for tag in website_conf.other_articles_choosen_tags_on_home.all():
        objs = U.get_posts_by_tag(tag.name, Article)
        other_articles.append({
            'tag': tag.slug,
            'title': tag.name,
            'objs': U.get_latest_post(website_conf.min_displayed_other_articles, objs)
        })
    
    context.update({'internal_tool_tag': internal_tool_tag.slug})
    context.update({'internal_tools_preview': website_conf.tools_post_preview})
    context.update({'internal_tools_posts': internal_tools})
    context.update({'internal_tools_length': len(internal_tools)})
    context.update({'current_tag': ''})
    
    context.update({'articles_preview': website_conf.articles_post_preview})
    context.update({'most_popular_article_posts': most_popular_article})

    context.update({'latest_news_posts': latest_news})

    context.update({'notes_preview': website_conf.notes_post_preview})
    context.update({'latest_notes_posts': latest_notes})


    my_res = []
    for res in my_resources:
        if len(res['objs']) > 0:
            my_res.append(res)
    context.update({'my_resources': my_res})

    oth_art = []
    for res in other_articles:
        if len(res['objs']) > 0:
            oth_art.append(res)
    context.update({'other_articles': oth_art})

    context.update({'comments': Comment.objects.filter(url__startswith=f"/{get_language()}/")[:10]})

    return TemplateResponse(request, 'Main/home.html', context=context)


def page_not_found(request, exception):
    context = U.initDefaults(request)
    return render(request, 'Main/404.html', context=context, status=404)

def load_table_of_content(request):
    titles = json.loads(request.POST.get("titles"))
    context = {
        'titles': titles,
    }
    return render(request, "Main/table_of_content.html", context=context)
