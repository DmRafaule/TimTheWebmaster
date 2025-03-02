from django.http import JsonResponse
from django.template import loader
from django.utils.translation import gettext as _
from Main.forms import FeedbackForm
from django.core.mail import send_mail
from .models import Comment, Interaction, Email
from .forms import CommentForm, ReviewForm, EmailForm
from .utils import getSlugFromURL
from MyBlog.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from django.core.paginator import Paginator



def bookmark_post(request):
    if request.method == 'POST':
        url = request.POST['url']
        isBookmarked = request.session.get("is_bookmarked_" + url, False)
        if not isBookmarked:
            interaction_tulpe = Interaction.objects.get_or_create(url=url)
            interaction = interaction_tulpe[0]
            interaction.bookmarks += 1
            interaction.save()
            request.session["is_bookmarked_" + url] = True

        data = {
            'msg': _("≡[。。]≡ Извини, JS не позволяет создавать собственные кнопки создания закладок и по этому, чтобы создать закладку нажми ctrl+d"),
        }
        status = 200 
    else:
        data = {
            'msg': _('Только POST запросы (╬▔皿▔)╯')
        }
        status = 503

    return JsonResponse(data, status=status)

# Basicaly one browser one like for one article
def like_post(request):
    if request.method == "POST":
        url = request.POST['url']
        isLiked = request.session.get("is_liked_" + url, False)
        if not isLiked:
            interaction_tulpe = Interaction.objects.get_or_create(url=url)
            interaction = interaction_tulpe[0]
            interaction.likes += 1
            interaction.save()
            request.session["is_liked_" + url] = True
            data = {
                'msg': _("Спасибо \(￣︶￣*\))"),
            }
            status = 200
        else:
            data = {
                'msg': _('Большое спасибо, но ты уже лайкнул (*￣3￣)╭')
            }
            status = 200
    else:
        data = {
            'msg': _('Только POST запросы (╬▔皿▔)╯')
        }
        status = 503

    return JsonResponse(data, status=status)

# No checks for multiple shares, because I do not want it.
# I want as many as I could get
def share_post(request):
    if request.method == "POST":
        url = request.POST['url']
        interaction_tulpe = Interaction.objects.get_or_create(url=url)
        interaction = interaction_tulpe[0]
        interaction.shares += 1
        interaction.save()
        data = {
            'msg': _("Большое спасибо что поделился \(￣︶￣*\))"),
        }
        status = 200
    else:
        data = {
            'msg': _('Только POST запросы (╬▔皿▔)╯')
        }
        status = 503

    return JsonResponse(data, status=status)

def email_post(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        msg = _('✔ Вы успешно подписались на рассылку (＠＾０＾)')
        email = form.cleaned_data.get("email")
        record, isCreated = Email.objects.get_or_create(email=email)
        if isCreated:
            record.save()
            status = 200
        else:
            msg = _('! Такая почта уже зарегистрированна')
            status = 503
        context = {'email_subscription_form': EmailForm()}
        loaded_template = loader.get_template(f'Engagement/engagement_email_subscription_form.html')
        email_form_doc = loaded_template.render(context, request)
        data = {
            'msg': msg,
            'form': email_form_doc
        }
    else:
        context = {'email_subscription_form': form}
        loaded_template = loader.get_template(f'Engagement/engagement_email_subscription_form.html')
        email_form_doc = loaded_template.render(context, request)
        data = {
            'msg': _('✗ Возникла ошибка при отправке формы ＼（〇_ｏ）／'),
            'form': email_form_doc
        }
        status = 503

    return JsonResponse(data,status=status)

def feedback_post(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        subject = f'{form.cleaned_data.get("username")} | {form.cleaned_data.get("email")}'
        message = f'{form.cleaned_data.get("message")}'
        send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[DEFAULT_TO_EMAIL])
        context = {'feedback_form': FeedbackForm()}
        loaded_template = loader.get_template(f'Engagement/engagement_feedback_form.html')
        feedback_doc = loaded_template.render(context, request)
        data = {
            'msg': _('✔ Вы успешно отправили сообщение (＠＾０＾)'),
            'form': feedback_doc
        }
        status = 200
    else:
        context = {'feedback_form': form}
        loaded_template = loader.get_template(f'Engagement/engagement_feedback_form.html')
        feedback_doc = loaded_template.render(context, request)
        data = {
            'msg': _('✗ Возникла ошибка при отправке формы ＼（〇_ｏ）／'),
            'form': feedback_doc
        }
        status = 503

    return JsonResponse(data,status=status)

def load_comments(request):
    if request.method == 'POST':
        url = request.POST['url']
        page_number = int(request.POST['page_number'])
        comments_already_posted = int(request.POST['posted_comments'])

        comments = Comment.objects.filter(url=url).order_by('-time_published')[comments_already_posted:]

        paginator = Paginator(comments, Comment.COMMENTS_PER_PAGE)
        if paginator.num_pages >= page_number:
            next_page = paginator.page(page_number)
            loaded_template = loader.get_template(f'Engagement/comments.html')
            comments_doc = loaded_template.render({'comments': next_page.object_list}, request)
            data = {
                'next_page_number': page_number + 1,
                'comments_doc': comments_doc,
                'is_next_page': next_page.has_next()
            }
            status = 200
        else:
            data = {'msg': _('Чувак, используй UI ┗( T﹏T )┛'),}
            status = 503
    else:
        data = {'msg': _('Только POST запросы (╬▔皿▔)╯'),}
        status = 503
    return JsonResponse(data, status=status)

def send_comment(request):
    if request.method == 'POST':
        # Check which type of form to use
        if request.POST['is_rating'] == 'false':
            Form = CommentForm
        else: 
            Form = ReviewForm

        form = Form(request.POST)
        if form.is_valid():
            # Update comment counter
            url = request.POST['url']
            interaction_tulpe = Interaction.objects.get_or_create(url=url)
            interaction = interaction_tulpe[0]
            
            comment = form.save(commit=False)
            comment.interaction = interaction
            comment.save()
            # Render empty form
            context = {'comment_form': Form()}
            loaded_template = loader.get_template(f'Engagement/comment_form.html')
            comment_form = loaded_template.render(context, request)
            # Render a comment
            context = {'comments': [comment]}
            loaded_template = loader.get_template(f'Engagement/comments.html')
            comment_doc = loaded_template.render(context, request)
            data = {
                'msg': _('✔ Вы успешно отправили сообщение (＠＾０＾)'),
                'form': comment_form,
                'new_comment': comment_doc,
                'new_comments_length': len(Comment.objects.filter(url=comment.url))
            }
            status = 200
            
        else:
            context = {'comment_form': form}
            loaded_template = loader.get_template(f'Engagement/comment_form.html')
            comment_form = loaded_template.render(context, request)
            data = {
                'msg': _('✗ Возникла ошибка при отправке комментария ＼（〇_ｏ）／'),
                'form': comment_form
            }
            status = 503

    else:
        data = {'msg': _('Только POST запросы (╬▔皿▔)╯'),}
        status = 503

    return JsonResponse(data, status=status)