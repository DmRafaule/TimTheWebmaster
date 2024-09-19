from django.shortcuts import render
import Main.utils as U
from .models import Website
import Gallery.utils as GU
import json
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .forms import FeedbackForm
from MyBlog.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from django.core.mail import send_mail
from Post.models import Tool, Article, Tag
from django.db.models import Q
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
    website_conf = Website.objects.get(is_current=True)

    context = U.initDefaults(request)
    internal_tool_tag = Tag.objects.get(slug_en='internal-tool')
    internal_tools = Tool.objects.filter(type=Tool.INTERNAL)
    most_popular_article = [U.get_most_popular_post()]
    latest_news_tag = Tag.objects.get(slug_en='news')
    news = U.get_posts_by_tag('News', Article)
    latest_news = U.get_latest_post(website_conf.max_displayed_news_on_home, news)
    series_tag = Tag.objects.get(slug_en='search-result-parser-series')
    post_series = U.get_posts_by_tag('search-result-parser-series', Article)
    latest_post_series = U.get_latest_post(website_conf.max_displayed_postSeries_on_home, post_series)
    latest_images = GU.getLatesImagesAll()[:website_conf.max_displayed_images_on_home]

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
    context.update({'posts': internal_tools})
    context.update({'current_tag': ''})
    loaded_template = loader.get_template(f'Post/list--post_preview-tool.html')
    context.update({'internal_tools': loaded_template.render(context, request)})
    
    context.update({'posts': most_popular_article})
    loaded_template = loader.get_template(f'Post/basic--post_preview-article.html')
    context.update({'most_popular_article': loaded_template.render(context, request)})

    context.update({'posts': latest_news})
    context.update({'latest_news_tag': latest_news_tag.slug})
    loaded_template = loader.get_template(f'Post/simple--post_preview-article.html')
    context.update({'latest_news': loaded_template.render(context, request)})

    context.update({'posts': latest_post_series})
    context.update({'series_tag': series_tag.slug})
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
