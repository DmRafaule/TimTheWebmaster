from datetime import datetime
from django.template.response import TemplateResponse
from django.template import loader
from django.utils.translation import gettext as _
from Post.models import Platform

class PostFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.filter_list = [] 
        self.allowed_templates = ('PagiScroll/base_post_list.html',)
        self.years = None

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        if response.template_name in self.allowed_templates:
            match response.context_data['category'].slug:
                case 'articles':
                    self.filter_list = [{'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'}]
                case 'notes':
                    self.filter_list = [{'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'}]
                case 'tools':
                    self.filter_list = [
                        {'template': 'PagiScroll/post_filter_tooltypes.html', 'verified': 'isTooltypesFilter'},
                        {'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'} 
                    ]
                    
            if len(self.filter_list) > 0:
                # Update how many years are
                last_year = datetime.today().year 
                years = []
                for y in range(2021,last_year + 1):
                    years.append(y)
                # Update context data
                self.years = years
                response.context_data.update({'isPostFilterMiddlewareConnected': True})
                response.context_data.update({'filters_doc': self._proceed_filters(request, response, self.filter_list)})

        return response

    def _proceed_filters(self, request, response, filter_list: list):
        filters_doc = []
        for filter_item in filter_list:
            response.context_data.update({filter_item['verified']: True})
            loaded_template = loader.get_template(filter_item['template'])
            filters_doc.append(loaded_template.render({
                'years': self.years,
                'letters': _('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЬ'),
                'platforms': Platform.objects.all()
            }, request))
        
        self.filter_list = []
        return filters_doc