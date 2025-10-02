from django.db.models import Q
from django.template.response import TemplateResponse

from .models import YandexCurrentAdBlockConfiguration


class AdManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.is_connected = False
        self.allowed_views = ('home', 'article', 'tool', 'tool_main')
        self.allowed_templates = ('PagiScroll/base_post_list.html', 'Post/basic--post_preview-article.html', 'Post/basic--post_preview-note.html', 'Post/basic--post_preview-tool.html' )

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.is_connected = False
        try:
            if view_func.__name__ in self.allowed_views:
                self.is_connected = True
        except:
            pass

        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if response.context_data:
            response.context_data.update({'isYandexAdManagerMiddlewareConnected': True})

        if self.is_connected or response.template_name in self.allowed_templates:
            self.ad_handler(request, response)

        self.is_connected = None

        return response
    
    def ad_handler(self, request, response):
        if response.context_data:
            current_ad_network = YandexCurrentAdBlockConfiguration.get_current()
            if current_ad_network:
                response.context_data.update({f'adlocations': current_ad_network.current.adnetwork_locations.all()})
                response.context_data.update({'ad_manager_show_on_page_each': current_ad_network.current.adnetwork_step_by})