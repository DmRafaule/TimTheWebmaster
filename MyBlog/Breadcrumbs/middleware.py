from django.template.response import TemplateResponse
from django.template import loader
from Post.models import Tool, Article, TD, QA


class BreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.slug = None
        self.allowed_func_posts = ('article','td','qa')
        self.allowed_func_tools = ('tool_main',)
        self.allowed_func_lists = ('article_list', 'td_list', 'qa_list', 'tools_list', 'notes_list')
        self.allowed_templates_pagination = ('PagiScroll/article_list.html', 'PagiScroll/termin_list.html', 'PagiScroll/question_list.html', 'PagiScroll/tool_list.html', 'PagiScroll/note_list.html')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ in self.allowed_func_posts:
            self.handler = self.post_handler
            self.slug = view_kwargs['post_slug']
        elif view_func.__name__ in self.allowed_func_tools:
            self.handler = self.tool_handler
            self.slug = self._remove_items(request.path.split('/'),'')[-1]
        
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        response.context_data.update({'isBreadcrumbsMiddlewareConnected': True})
        if self.handler is not None:
            self.handler(request, response)
        elif response.template_name in self.allowed_templates_pagination:
            self.list_handler(request, response)

        return response

    def _remove_items(self, list, item): 
        # remove the item for all its occurrences 
        c = list.count(item) 
        for i in range(c): 
            list.remove(item) 
        return list 
    
    def post_handler(self, request, response):
        if len(Article.objects.filter(slug=self.slug)) == 1:
            name = Article.objects.filter(slug=self.slug)[0].title
        elif len(QA.objects.filter(slug=self.slug)) == 1:
            name = QA.objects.filter(slug=self.slug)[0].question
        elif len(TD.objects.filter(slug=self.slug)) == 1:
            name = TD.objects.filter(slug=self.slug)[0].termin
        response.context_data.update({'post_title': name})
    
    def tool_handler(self, request, response):
        title_qs = Tool.objects.filter(slug=self.slug)
        if len(title_qs) > 0:
            title = title_qs[0]
        else:
            title = self.slug
        response.context_data.update({'post_title': title.name})
    
    def list_handler(self, request, response):
        pass