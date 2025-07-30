from datetime import datetime
from django.template.response import TemplateResponse
from django.template import loader
from django.utils.translation import gettext as _
from Post.models import Platform

class PostFilterMiddleware:
    ''' Мидлвари для обработки шаблонов страниц пагинации,
     для последующего добавления фильтров '''
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
        # Обрабатывает только шаблоны по указаным за ранее путям
        if response.template_name in self.allowed_templates:
            # В зависимости от того, что за категория, будут представленны разные фильтры
            match response.context_data['category'].slug:
                case 'articles':
                    self.filter_list = [{'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'}]
                case 'notes':
                    self.filter_list = [{'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'}]
                case 'services':
                    self.filter_list = [{'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'}]
                case 'tools':
                    self.filter_list = [
                        {'template': 'PagiScroll/post_filter_tooltypes.html', 'verified': 'isTooltypesFilter'},
                        {'template': 'PagiScroll/post_filter_times.html', 'verified': 'isTimeFilter'} 
                    ]
                    
            if len(self.filter_list) > 0:
                # Определяем какие года доступны для фильтрации
                last_year = datetime.today().year 
                years = []
                for y in range(2021,last_year + 1):
                    years.append(y)
                self.years = years
                # Обновляем контекстные данные и разрешаем данному мидлвари менять шаблоны
                response.context_data.update({'isPostFilterMiddlewareConnected': True})
                response.context_data.update({'filters_doc': self._proceed_filters(request, response, self.filter_list)})

        return response

    def _proceed_filters(self, request, response, filter_list: list):
        ''' Рендерит шаблон фильтров '''
        filters_doc = []
        for filter_item in filter_list:
            response.context_data.update({filter_item['verified']: True})
            loaded_template = loader.get_template(filter_item['template'])
            # Обновляем контекстные данные дополнительными значениями в зависимости от фильтра
            filters_doc.append(loaded_template.render({
                'years': self.years,
                'letters': _('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЬ'),
                'platforms': Platform.objects.all()
            }, request))
        # Лучше обнулить получившийся список, чтобы при переходе на следующую стр. пагинации
        # сохранились предыдущие фильтры 
        self.filter_list = []
        return filters_doc