from django.template.response import TemplateResponse
from django.template import loader

from Main.models import Media
from Main.utils import get_tool, getAllWithTags
from Post.models import Tag, Note

class ToolMiddleware:
    ''' Промежуточный обработчик шаблонов для инструментов '''


    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.slug = None
        # Определяем какие представления следует обрабатывать
        self.allowed_func_tools = ('tool_main', 'tool')

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # Задаём обработчику соответствующую функцию, для последующего вызова, для тех представлений, которые
            # были обозначен при создании этого мидлвари
            if view_func.__name__ in self.allowed_func_tools:
                self.handler = self.tool_handler
        except:
            pass
        return None

    def process_template_response(self, request, response: TemplateResponse):
        if self.handler is not None:
            if response.context_data:
                # Если представление правильное и присутствует контекстное хранилище переменных
                # Задаём ещё одну контекстную переменную, которая будет необходима,
                # чтобы знать когда менять шаблон а когда нет
                response.context_data.update({'isToolMiddlewareConnected': True})
            # Запускаем обработчик
            self.handler(request, response)

        return response
    
    def tool_handler(self, request, response):
        ''' Обрабатывает представления инструментов для задания соответствующих, общих контекстных переменных '''
        url = f'{request.get_host()}{request.path}'
        if response.context_data:
            # Сохраняем и возвращаем текущий УРЛ представления
            response.context_data.update({'url_to_share': url})
            # Получаем используемый инструмент в представлении
            tool = get_tool(request.path)
            if tool:
                # Сохраняем медиа файлы связанные с данным инструментом
                downloadables = tool.media.filter_by_lang().filter(type=Media.RAW_FILE).order_by('timeCreated')
                images = tool.media.filter_by_lang().filter(type=Media.IMAGE).order_by('timeCreated')
                videos = tool.media.filter_by_lang().filter(type=Media.VIDEO).order_by('timeCreated')
                pdfs = tool.media.filter_by_lang().filter(type=Media.PDF).order_by('timeCreated')
                audios = tool.media.filter_by_lang().filter(type=Media.AUDIO).order_by('timeCreated')
                response.context_data.update({'post': tool})
                response.context_data.update({'downloadables': downloadables})
                response.context_data.update({'images': images})
                response.context_data.update({'videos': videos})
                response.context_data.update({'pdfs': pdfs})
                response.context_data.update({'audios': audios})
                # Пытаемся получить последние заметки по данному инструменту
                tool_tags = Tag.objects.filter(slug_en=tool.slug)
                if len(tool_tags) > 0:
                    # Чтобы это сработало, должен будет существовать особый тег для инструмента, у которого tag.slug=tool.slug
                    posts = getAllWithTags(Note.objects.filter(isPublished=True), [tool_tags[0]])[:3]
                    if len(posts) > 0:
                        is_notes = True
                    else:
                        is_notes = False
                    # Сохраняем полученый тег, для того чтобы можно было перейти на стр. пагинации
                    # и посмотреть уже все заметки
                    response.context_data.update({'tool_tag': tool_tags[0].slug})
                    # Отрисовываем и возвращаем кусочек отрисованного шаблона
                    response.context_data.update({'posts': posts})
                    loaded_template = loader.get_template(f'Post/basic--post_preview-note.html')
                    response.context_data.update({'latest_notes': loaded_template.render(response.context_data, request), 'is_notes': is_notes})
                # Получаем платформы, на которых данный инструмент может работать
                response.context_data.update({'platforms': tool.platforms.all()})