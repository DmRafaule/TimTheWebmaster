from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET , require_POST

from Main.forms import FeedbackForm
from Website.settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from .models import Comment, Interaction, Email
from .forms import CommentForm, ReviewForm, EmailForm
from .utils import get_root_comments



@require_POST
def bookmark_post(request):
    url = request.POST['url']
    isBookmarked = request.session.get("is_bookmarked_" + url, False)
    if not isBookmarked:
        interaction_tulpe = Interaction.objects.get_or_create(url=url)
        interaction = interaction_tulpe[0]
        interaction.bookmarks += 1
        interaction.save()
        request.session["is_bookmarked_" + url] = True
    status = 200 

    return JsonResponse({}, status=status)

@require_POST
def like_post(request):
    url = request.POST['url']
    isLiked = request.session.get("is_liked_" + url, False)
    if not isLiked:
        interaction_tulpe = Interaction.objects.get_or_create(url=url)
        interaction = interaction_tulpe[0]
        interaction.likes += 1
        interaction.save()
        request.session["is_liked_" + url] = True
        status = 200
    else:
        status = 201

    return JsonResponse({}, status=status)

@require_POST
def share_post(request):
    url = request.POST['url']
    interaction_tulpe = Interaction.objects.get_or_create(url=url)
    interaction = interaction_tulpe[0]
    interaction.shares += 1
    interaction.save()
    status = 200

    return JsonResponse({}, status=status)

@require_POST
def email_post(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        record, isCreated = Email.objects.get_or_create(email=email)
        if isCreated:
            record.save()
            status = 200
        else:
            status = 503
        context = {'email_subscription_form': EmailForm()}
        loaded_template = loader.get_template(f'Engagement/Other/engagement_email_subscription_form.html')
        email_form_doc = loaded_template.render(context, request)
    else:
        context = {'email_subscription_form': form}
        loaded_template = loader.get_template(f'Engagement/Other/engagement_email_subscription_form.html')
        email_form_doc = loaded_template.render(context, request)
        status = 400

    return HttpResponse(email_form_doc, status=status)

@require_GET
def email_form_get(request):
    context = {'email_subscription_form': EmailForm()}
    loaded_template = loader.get_template(f'Engagement/Other/engagement_email_subscription_form_container.html')
    email_form_doc = loaded_template.render(context, request)
    return HttpResponse(email_form_doc)

def load_comments(request):
        
    if request.method == 'POST':
        url = request.POST['url']
        page_number = int(request.POST['page_number'])
        comments_already_posted = int(request.POST['posted_comments'])

        comments = Comment.objects.filter(url=url).filter(is_root=True).order_by('-time_published')[comments_already_posted:]

        paginator = Paginator(comments, Comment.COMMENTS_PER_PAGE)
        if paginator.num_pages >= page_number:
            next_page = paginator.page(page_number)
            loaded_template = loader.get_template(f'Engagement/Commenting/comments.html')
            comments_doc = loaded_template.render({'comments': next_page.object_list, 'from': "post"}, request)
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

def load_replies(request):
    if request.method == 'POST':
        comment_root_id = int(request.POST['comment_root_id'])
        page_number = int(request.POST['page_number'])
        comments = Comment.objects.get(id=comment_root_id).replies.all()
        paginator = Paginator(comments, Comment.COMMENTS_PER_PAGE)
        if paginator.num_pages >= page_number:
            next_page = paginator.page(page_number)
            loaded_template = loader.get_template(f'Engagement/Commenting/comments.html')
            comments_doc = loaded_template.render({'comments': next_page.object_list, 'from': "post"}, request)
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
        if form.is_valid() and (form.cleaned_data['name'] != 'timthewebmaster' or request.user.is_superuser ):
            # Update comment counter
            url = request.POST['url']
            interaction_tulpe = Interaction.objects.get_or_create(url=url)
            interaction = interaction_tulpe[0]
            
            comment = form.save(commit=False)
            comment.interaction = interaction
            comment.save()
            # Check if it is response
            comment_reply_to_id = request.POST['comment_reply_to']
            if comment_reply_to_id == 'false' or comment_reply_to_id == 'False'  :
                comment_reply_to_id = False
            else:
                comment_reply_to_id = int(comment_reply_to_id)
                # Save replies to comment
                comment_reply_to = Comment.objects.get(id=comment_reply_to_id)
                comment_reply_to.replies.add(comment)
                comment_reply_to.save()
                comment.is_root = False
                comment.save()
            # Render empty form
            context = {'comment_form': Form()}
            loaded_template = loader.get_template(f'Engagement/Commenting/comment_form.html')
            comment_form = loaded_template.render(context, request)
            # Render a comment
            context = {'comments': [comment]}
            loaded_template = loader.get_template(f'Engagement/Commenting/comments.html')
            comment_doc = loaded_template.render(context, request)
            data = {
                'msg': _('✔ Вы успешно отправили сообщение (＠＾０＾)'),
                'reply_id': comment_reply_to_id,
                'comment_id': comment.id,
                'form': comment_form,
                'new_comment': comment_doc,
                'new_comments_length': len(Comment.objects.filter(url=comment.url))
            }
            status = 200
            
        else:
            context = {'comment_form': form}
            loaded_template = loader.get_template(f'Engagement/Commenting/comment_form.html')
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