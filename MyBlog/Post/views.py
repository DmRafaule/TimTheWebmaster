import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import Post.models as Post_M
from django.utils.translation import gettext as _
import Comment.models as Comment_M
import Main.models as Main_M
import User.models as User_M
import Main.utils as U
from django.views.generic import DetailView, ListView, TemplateView

max_el_in_related_post = 5


class PostPreviewView(TemplateView):

    model = None
    context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        # Defines order of loading posts. Recent of latest
        is_recent = self.request.GET.get('is_recent')
        if is_recent == 'true':
            order = '-timeCreated'
        else:
            order = 'timeCreated'
        # Define how much to load
        number = self.request.GET.get('number', 1)
        # Define from which post to start count
        offset = self.request.GET.get('offset', 1)
        context.update({'posts': self.model.objects.filter(isPublished=True).order_by(order)[(int(offset)):(int(number)) + (int(offset))] })
        offset = int(offset) + int(number)
        length = self.model.objects.filter(isPublished=True).count()
        is_end = False
        if (length <= int(offset) or length == 0):
            is_end = True

        context.update({'is_end': is_end})

        return context

    def get(self, request):
        context = self.get_context_data()
        # Define how much data should be loaded on user screen
        # There are 3 modes
        # basic - display everything that possible from preview to views
        # simple - display only needes information, title, description, date published
        # minimal - display only title and date published
        # raw - display row links to pages
        mode = self.request.GET.get('mode', 'basic') + '--'
        # Define specific (unique) preview templates
        for_who = self.request.GET.get('for_who', '')
        cat = "-" + self.request.GET.get('category', '')
        if for_who != '':
            for_who = '-' + for_who
        return render(
                request,
                f'Post/{mode}post_preview{for_who}{cat}.html',
                context=context)


class PostListView(ListView):

    model = Post_M.Category
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = U.initDefaults(self.request)
        context['category'] = self.category
        return context


def article(request, post_slug):
    post = get_object_or_404(Post_M.Article, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'comments': Comment_M.Comment.objects.filter(type=post).order_by('-timeCreated')})
    context.update({'comments_number': Comment_M.Comment.objects.filter(type=post).count()})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template.path, context=context)


def news(request, post_slug):
    post = get_object_or_404(Post_M.News, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template, context=context)


def case(request, post_slug):
    post = get_object_or_404(Post_M.Case, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})

    return render(request, post.template, context=context)


def qa(request, post_slug):
    post = get_object_or_404(Post_M.QA, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    tags = post.tags.values_list('pk', flat=True)
    related_articles = Post_M.Article.objects.filter(tags__in=tags)
    context.update({'related_articles': set(related_articles[:max_el_in_related_post])})

    related_cases = Post_M.Case.objects.filter(tags__in=tags)
    context.update({'related_cases': set(related_cases[:max_el_in_related_post])})

    related_news = Post_M.News.objects.filter(tags__in=tags)
    context.update({'related_news': set(related_news[:max_el_in_related_post])})

    related_tools = Post_M.Tool.objects.filter(tags__in=tags)
    context.update({'related_tools': set(related_tools[:max_el_in_related_post])})

    related_services = Post_M.Service.objects.filter(tags__in=tags)
    context.update({'related_services': set(related_services[:max_el_in_related_post])})

    return render(request, post.template, context=context)


def td(request, post_slug):
    post = get_object_or_404(Post_M.TD, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    tags = post.tags.values_list('pk', flat=True)
    related_articles = Post_M.Article.objects.filter(tags__in=tags)
    context.update({'related_articles': set(related_articles[:max_el_in_related_post])})

    related_cases = Post_M.Case.objects.filter(tags__in=tags)
    context.update({'related_cases': set(related_cases[:max_el_in_related_post])})

    related_news = Post_M.News.objects.filter(tags__in=tags)
    context.update({'related_news': set(related_news[:max_el_in_related_post])})

    related_tools = Post_M.Tool.objects.filter(tags__in=tags)
    context.update({'related_tools': set(related_tools[:max_el_in_related_post])})

    related_services = Post_M.Service.objects.filter(tags__in=tags)
    context.update({'related_services': set(related_services[:max_el_in_related_post])})

    return render(request, post.template, context=context)


def service(request, post_slug):
    post = get_object_or_404(Post_M.Service, slug=post_slug)
    post.viewed = post.viewed + 1
    post.save()
    downloadables = Main_M.Downloadable.objects.filter(type=post)
    images = Main_M.Image.objects.filter(type=post)
    context = U.initDefaults(request)
    context.update({'post': post})
    context.update({'downloadables': downloadables})
    context.update({'images': images})
    tags = post.tags.values_list('pk', flat=True)
    cases = Post_M.Case.objects.filter(tags__in=tags)
    qas = Post_M.QA.objects.filter(tags__in=tags)
    context.update({'cases': cases})
    context.update({'qas': qas})

    return render(request, post.template, context=context)


# Basicaly one browser one like for one article
def like_post(request):
    post_slug = request.POST['slug']
    isLiked = request.session.get("is_liked_" + post_slug, False)
    if not isLiked:
        post = get_object_or_404(Post_M.Post, slug=post_slug)
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
    post = get_object_or_404(Post_M.Post, slug=post_slug)
    post.shares = post.shares + 1
    post.save()
    data = {
        'shares': post.shares,
    }
    return JsonResponse(data)


def load_message(request, post_slug):
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
            source = Post_M.Service.objects.get(slug=post_slug).get_absolute_url()
            new_message = User_M.Message(source=source, name=username, email=email, content=about)
            new_message.save()

        return JsonResponse(message, status=status)
    else:
        status = 403
        message['common'] = _("Ты, скользкий тип")
        message['username'] = _("Даже не пытайся")
        message['email'] = _("Или попытайся, всёравно")
        return JsonResponse(message, status=status)
