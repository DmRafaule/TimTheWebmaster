from django.template.response import TemplateResponse
from django.template import loader

from Main.models import Media
from Main.utils import get_tool, getAllWithTags
from Post.models import Tag, Note

class ToolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.slug = None
        self.allowed_func_tools = ('tool_main', 'tool')

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.__name__ in self.allowed_func_tools:
                self.handler = self.tool_handler
        except:
            pass
        return None

    def process_template_response(self, request, response: TemplateResponse):
        if self.handler is not None:
            if response.context_data:
                response.context_data.update({'isToolMiddlewareConnected': True})
            self.handler(request, response)

        return response
    
    def tool_handler(self, request, response):
        url = f'{request.get_host()}{request.path}'
        if response.context_data:
            response.context_data.update({'url_to_share': url})
            tool = get_tool(request.path)
            if tool:
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

                # Get latest notes about this tool
                tool_tags = Tag.objects.filter(slug_en=tool.slug)
                if len(tool_tags) > 0:
                    posts = getAllWithTags(Note.objects.filter(isPublished=True), [tool_tags[0]])[:3]
                    if len(posts) > 0:
                        is_notes = True
                    else:
                        is_notes = False
                    response.context_data.update({'tool_tag': tool_tags[0].slug})
                    response.context_data.update({'posts': posts})
                    loaded_template = loader.get_template(f'Post/basic--post_preview-note.html')
                    response.context_data.update({'latest_notes': loaded_template.render(response.context_data, request), 'is_notes': is_notes})
                
                # Get used platforms
                response.context_data.update({'platforms': tool.platforms.all()})