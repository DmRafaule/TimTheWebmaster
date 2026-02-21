from django.template.response import TemplateResponse
from Main.forms import FeedbackForm
from Main.models import Media
from Main.utils import get_tool
from django.template import loader
from .models import Comment, Interaction
from .forms import CommentForm, ReviewForm, EmailForm
from .utils import get_root_comments

class EngagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.slug = None
        # If you do not need a engagement options, but need to proceed templates with other data 
        self.allowed_func_no_engagement = ('home',)
        # If comments needed include view funcions here
        self.allowed_func_posts_with_comments = ('article',)
        # All tools main view functions must be called tool_main
        self.allowed_func_tools = ('tool_main', 'tool')
        # Beacause of Class base view we use templates name instead of functions
        self.allowed_templates_pagination = ('PagiScroll/base_post_list.html',)
        self.form = FeedbackForm()
        self.email_form = EmailForm()
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.__name__ in self.allowed_func_posts_with_comments:
                self.handler = self.post_handler
                self.slug = view_kwargs['post_slug']
            elif view_func.__name__ in self.allowed_func_tools:
                self.handler = self.tool_handler
            elif view_func.__name__ in self.allowed_func_no_engagement:
                self.handler = self.no_engagement_handler
        except:
            pass
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if self.handler is not None:
            if response.context_data:
                response.context_data.update({'isEngagementMiddlewareConnected': True})
            self.handler(request, response)

        if response.template_name in self.allowed_templates_pagination:
            if response.context_data:
                response.context_data.update({'isEngagementMiddlewareConnected': True})
            self.list_handler(request, response)

        return response
    
    def _update_views_counter(self, url):
        interaction_qs = Interaction.objects.filter(url=url)
        if len(interaction_qs) > 0:
            interaction = interaction_qs[0]
            interaction.views += 1
            interaction.save()
    
    def _set_comments(self, request, response, isComments, template=None, form=CommentForm()):
        if isComments:
            comment_form = form
            comments = Comment.objects.filter(url=request.path).filter(is_root=True).order_by('-time_published')
            loaded_template = loader.get_template(template)
            comments_doc = loaded_template.render({
                'comment_form': comment_form,
                'all_comments_length': len(comments),
                'comments': comments[:Comment.COMMENTS_PER_PAGE],
                'per_page_comments': Comment.COMMENTS_PER_PAGE
            }, request)
            if response.context_data:
                response.context_data.update({'comments_doc': comments_doc})
        
        return isComments
    

    # Updates articles + adding comments 
    def no_engagement_handler(self, request, response):
        if response.context_data:
            response.context_data.update({'isDisplayingActualAvailableInteractions': False})

    # Updates articles + adding comments 
    def post_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        if response.context_data:
            response.context_data.update({'url_to_share': url})
            response.context_data.update({'is_likes': True})
            response.context_data.update({'is_comments': self._set_comments(request, response, True, 'Engagement/Commenting/engagement_post_comments.html')})
            response.context_data.update({'is_shares': True})
            response.context_data.update({'is_bookmarks': True})
            response.context_data.update({'is_email': True})
            response.context_data.update({'email_subscription_form': self.email_form})
            response.context_data.update({'isBottomEngagementBody': True})
            response.context_data.update({'isDisplayingActualAvailableInteractions': True})
            self._update_views_counter(request.path)

    # Updates internal tools + comments
    def tool_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        if response.context_data:
            response.context_data.update({'url_to_share': url})
            response.context_data.update({'is_likes': True})
            response.context_data.update({'is_comments': self._set_comments(request, response, True, 'Engagement/Commenting/engagement_tool_comments.html', ReviewForm())})
            response.context_data.update({'is_shares': True})
            response.context_data.update({'is_bookmarks': True})
            response.context_data.update({'is_email': True})
            response.context_data.update({'email_subscription_form': self.email_form})
            response.context_data.update({'isBottomEngagementBody': True})
            response.context_data.update({'isDisplayingActualAvailableInteractions': True})
            # THis is all for Google Rich Results, SoftwareApplication
            comments = Comment.objects.filter(url=request.path).order_by('-time_published')
            response.context_data.update({'comments_number': len(comments)})
            if len(comments) > 0:
                response.context_data.update({'comments_score': Comment.get_score(request.path)})
            tool = get_tool(request.path)
            if tool:
                response.context_data.update({'page_tool': tool})

            self._update_views_counter(request.path)

   # Updates pages of paginator 
    def list_handler(self, request, response):
        if response.context_data:
            response.context_data.update({'is_likes': True})
            response.context_data.update({'is_comments': self._set_comments(request, response, False)})
            response.context_data.update({'is_shares': False})
            response.context_data.update({'is_bookmarks': True})
            response.context_data.update({'is_email': True})
            response.context_data.update({'email_subscription_form': self.email_form})
            response.context_data.update({'isBottomEngagementBody': False})
            response.context_data.update({'isDisplayingActualAvailableInteractions': False})
            self._update_views_counter(request.path)