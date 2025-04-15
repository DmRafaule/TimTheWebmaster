from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from .utils import GetCustomFilterPage

class PagiScrollEditorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_templates = ('PagiScroll/article_list.html', 'PagiScroll/tool_list.html', 'PagiScroll/note_list.html')

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if response.template_name in self.allowed_templates:
            # Here you will be check if URL match with slug of custom filter page
            filter_page = GetCustomFilterPage(request.get_full_path())
            if filter_page is not None:
                response.context_data.update({'cfp_title': filter_page.title})
                response.context_data.update({'cfp_description': filter_page.description})
                response.context_data.update({'cfp_h1': filter_page.h1})
                response.context_data.update({'cfp_lead': filter_page.lead})

        return response