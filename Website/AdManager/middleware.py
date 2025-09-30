from django.db.models import Q
from django.template.response import TemplateResponse

from .models import CurrentAdNetwork


class AdManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.home_view = ('home',)
        self.post_view = ('article', 'tool', 'tool_main')
        self.pagiscroll_view = ('PagiScroll/base_post_list.html', 'Post/basic--post_preview-article.html', 'Post/basic--post_preview-note.html', 'Post/basic--post_preview-tool.html', 'TextThief/text-thief-form-result.html', 'LinkThief/link-thief-form-result.html' )

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.handler = None
        try:
            if view_func.__name__ in self.home_view:
                self.handler = self.home_handler
            elif view_func.__name__ in self.post_view:
                self.handler = self.post_handler
        except:
            pass
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if response.context_data:
            response.context_data.update({'isAdManagerMiddlewareConnected': True})

        if self.handler is not None:
            self.handler(request, response)
        elif response.template_name in self.pagiscroll_view:
            self.pagiscroll_handler(request, response)

        self.handler = None

        return response
    
    def home_handler(self, request, response):
        if response.context_data:
            current_ad_network = CurrentAdNetwork.get_current()
            if current_ad_network:
                for block_pk, block_type in current_ad_network.current.adnetwork_blocks.all().values_list('pk', 'adblock_type'):
                    response.context_data.update({f'adblock_id_{block_pk}': current_ad_network.current.adnetwork_blocks.get(pk=block_pk).adblock_id})
                response.context_data.update({'ad_loader': current_ad_network.current.adnetwork_loader_code})
                response.context_data.update({'ad_manager': current_ad_network.current})
    
    def post_handler(self, request, response):
        if response.context_data:
            current_ad_network = CurrentAdNetwork.get_current()
            if current_ad_network:
                for block_pk, block_type in current_ad_network.current.adnetwork_blocks.all().values_list('pk', 'adblock_type'):
                    response.context_data.update({f'adblock_id_{block_pk}': current_ad_network.current.adnetwork_blocks.get(pk=block_pk).adblock_id})
                response.context_data.update({'ad_loader': current_ad_network.current.adnetwork_loader_code})
                response.context_data.update({'ad_manager': current_ad_network.current})

    # Updates  posts lists
    def pagiscroll_handler(self, request, response):
        if response.context_data:
            current_ad_network = CurrentAdNetwork.get_current()
            if current_ad_network:
                for block_pk, block_type in current_ad_network.current.adnetwork_blocks.all().values_list('pk', 'adblock_type'):
                    response.context_data.update({f'adblock_id_{block_pk}': current_ad_network.current.adnetwork_blocks.get(pk=block_pk).adblock_id})
                response.context_data.update({'ad_loader': current_ad_network.current.adnetwork_loader_code})
                response.context_data.update({'ad_manager': current_ad_network.current})
                response.context_data.update({'ad_manager_show_on_page_each': current_ad_network.current.adnetwork_step_by})