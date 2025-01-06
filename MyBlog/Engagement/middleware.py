from django.template.response import TemplateResponse
from Main.forms import FeedbackForm
from django.template import loader
from .models import Comment, Interaction
from .forms import CommentForm, ReviewForm
from .utils import getSlugFromURL

class EngagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.slug = None
        # If you do not need a engagement options, but need to proceed templates with other data 
        self.allowed_func_no_engagement = ('home',)
        # If comments needed include view funcions here
        self.allowed_func_posts_with_comments = ('article',)
        # If no comments needed include view funcions here
        self.allowed_func_posts_with_no_comments = ('td','qa')
        # All tools main view functions must be called tool_main
        self.allowed_func_tools = ('tool_main',)
        self.allowed_func_lists = ('article_list', 'td_list', 'qa_list', 'tools_list', 'notes_list')
        self.form = FeedbackForm()
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ in self.allowed_func_posts_with_comments:
            self.handler = self.post_handler
            self.slug = view_kwargs['post_slug']
        elif view_func.__name__ in self.allowed_func_posts_with_no_comments:
            self.handler = self.post_no_comment_handler
            self.slug = view_kwargs['post_slug']
        elif view_func.__name__ in self.allowed_func_tools:
            self.handler = self.tool_handler
        elif view_func.__name__ in self.allowed_func_no_engagement:
            self.handler = self.no_engagement_handler
        elif view_func.__name__ in self.allowed_func_lists:
            self.handler = self.list_handler

        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if self.handler is not None:
            response.context_data.update({'isEngagementMiddlewareConnected': True})
            self.handler(request, response)
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
            comments = Comment.objects.filter(url=request.path).order_by('-time_published')
            loaded_template = loader.get_template(template)
            comments_doc = loaded_template.render({
                'comment_form': comment_form,
                'all_comments_length': len(comments),
                'comments': comments[:Comment.COMMENTS_PER_PAGE],
                'per_page_comments': Comment.COMMENTS_PER_PAGE
            }, request)
            response.context_data.update({'comments_doc': comments_doc})
        
        return isComments
    

    # Updates articles + adding comments 
    def no_engagement_handler(self, request, response):
        response.context_data.update({'isDisplayingActualAvailableInteractions': False})

    # Updates articles + adding comments 
    def post_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        response.context_data.update({'url_to_share': url})
        response.context_data.update({'is_likes': True})
        response.context_data.update({'is_comments': self._set_comments(request, response, True, 'Engagement/engagement_post_comments.html')})
        response.context_data.update({'is_shares': True})
        response.context_data.update({'is_bookmarks': True})
        response.context_data.update({'is_feedbacks': True})
        response.context_data.update({'form': self.form})
        response.context_data.update({'isBottomEngagementBody': True})
        response.context_data.update({'isDisplayingActualAvailableInteractions': True})
        self._update_views_counter(request.path)

    # Updates td and qa types of posts withour commentst
    def post_no_comment_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        response.context_data.update({'url_to_share': url})
        response.context_data.update({'is_likes': True})
        response.context_data.update({'is_comments': self._set_comments(request, response, False)})
        response.context_data.update({'is_shares': True})
        response.context_data.update({'is_bookmarks': True})
        response.context_data.update({'is_feedbacks': True})
        response.context_data.update({'form': self.form})
        response.context_data.update({'isBottomEngagementBody': True})
        response.context_data.update({'isDisplayingActualAvailableInteractions': True})
        self._update_views_counter(request.path)

    # Updates internal tools + comments
    def tool_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        response.context_data.update({'url_to_share': url})
        response.context_data.update({'is_likes': True})
        response.context_data.update({'is_comments': self._set_comments(request, response, True, 'Engagement/engagement_tool_comments.html', ReviewForm())})
        response.context_data.update({'is_shares': True})
        response.context_data.update({'is_bookmarks': True})
        response.context_data.update({'is_feedbacks': True})
        response.context_data.update({'form': self.form})
        response.context_data.update({'isBottomEngagementBody': True})
        response.context_data.update({'isDisplayingActualAvailableInteractions': True})
        self._update_views_counter(request.path)

   # Updates pages of paginator 
    def list_handler(self, request, response):
        response.context_data.update({'is_likes': True})
        response.context_data.update({'is_comments': self._set_comments(request, response, False)})
        response.context_data.update({'is_shares': False})
        response.context_data.update({'is_bookmarks': True})
        response.context_data.update({'is_feedbacks': True})
        response.context_data.update({'form': self.form})
        response.context_data.update({'isBottomEngagementBody': False})
        response.context_data.update({'isDisplayingActualAvailableInteractions': False})
        self._update_views_counter(request.path)