from django.db.models import Q
from django.template import loader
from django.template.response import TemplateResponse

from Main.utils import getAllWithTags
from Post.models import Tag, Post

from .models import AffiliateLink, AffiliateLinkConnectionTag, AffiliateLinkConnectionSlug, AffiliateLinkConnectionSpecial


class AffiliateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = None
        self.home_view = ('home',)
        self.post_view = ('article', 'tool', 'tool_main')
        self.pagiscroll_view = ('PagiScroll/base_post_list.html',)

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
            response.context_data.update({'isAffiliateLinkMiddlewareConnected': True})

        if self.handler is not None:
            self.handler(request, response)
        elif response.template_name in self.pagiscroll_view:
            self.pagiscroll_handler(request, response)

        self.handler = None

        return response
    
    def home_handler(self, request, response):
        if response.context_data:
            affiliates = []
            affiliates_context = AffiliateLinkConnectionSpecial.objects.filter(special=AffiliateLinkConnectionSpecial.SpecialPages.HOME)
            if len(affiliates_context) > 0:
                aff_ids = []
                for aff_id in affiliates_context.values_list('affiliate'):
                    aff_ids.append(aff_id[0])
                affiliates = AffiliateLink.objects.filter_by_lang().filter(id__in=aff_ids)
            response.context_data.update({'affiliates_partners': affiliates[:3]})
    
    def post_handler(self, request, response):
        if response.context_data:
            affiliates = []
            # Делим строку
            urlList = request.path.split('/')
            # Чистим не нужный мусор
            c = urlList.count('') 
            for i in range(c): 
                urlList.remove('') 
            # Проверяем есть ли такой инструмент
            slug = urlList[-1]
            post = Post.objects.get(slug=slug)
            affiliates_context = AffiliateLinkConnectionSlug.objects.filter(slugs=post)
            if len(affiliates_context) > 0:
                aff_ids = []
                for aff_id in affiliates_context.values_list('affiliate'):
                    aff_ids.append(aff_id[0])
                affiliates = AffiliateLink.objects.filter_by_lang().filter(id__in=aff_ids)
            response.context_data.update({'affiliates_partners': affiliates[:2]})


    # Updates  posts lists
    def pagiscroll_handler(self, request, response):
        if response.context_data:
            affiliates = []
            tags_names = request.GET.getlist('tag', [])
            tags = Tag.objects.filter(Q(name_ru__in=tags_names) | Q(name_en__in=tags_names) | Q(slug_ru__in=tags_names)  | Q(slug_en__in=tags_names))
            if len(tags) > 0:
                affiliates = getAllWithTags(AffiliateLinkConnectionTag.objects.all(), tags) 
            if len(affiliates) > 0:
                aff_ids = []
                for aff_id in affiliates.values_list('affiliate'):
                    aff_ids.append(aff_id[0])
                affiliates = AffiliateLink.objects.filter_by_lang().filter(id__in=aff_ids)
            response.context_data.update({'affiliates_partners': affiliates[:3]})
