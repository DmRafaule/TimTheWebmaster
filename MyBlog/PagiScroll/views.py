import json
import Post.models as Post_M
import Main.models as Main_M
import Main.utils as U
from django.http import Http404, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse
from django.views.generic.list import ListView


class PostListView(ListView):
    allow_empty=True
    context_object_name = "posts"
    website_conf = None
    is_recent = "true"
    is_alphabetic = "ignored"
    category = None
    pages = 0
    page = 1
    tags = None
    tags_names = None
    image = None
    context = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Update context data
        context['category'] = Post_M.Category.objects.get(slug=self.category)
        context['displayTags'] = True
        context['num_pages'] = self.pages
        context['current_page'] = self.page
        context['page'] = self.page + 1
        context['is_recent'] = self.is_recent
        context['current_tag'] = self.tags
        context['current_tag_names'] = self.tags_names
        context['tags_json'] = json.dumps(self.tags)
        context['post_list_preview'] = self.image

        return context

    def get(self, request):
        error_response = self.fetch(request)
        if error_response is None:
            return TemplateResponse(request, self.template_name, self.context)
        else:
            return error_response

    def post(self, request):
        error_response = self.fetch(request)
        if  error_response is None:
            cat = "-" + Post_M.Category.objects.get(slug=self.category).categry_name.lower()
            return TemplateResponse(request, f'Post/basic--post_preview{cat}.html', self.context)
        else:
            return error_response
    
    def fetch(self, request):
        self.website_conf = Main_M.Website.objects.get(is_current=True)
        if request.method == "GET":
            self.page = int(request.GET.get('page', 1))
        elif request.method == "POST":
            self.page = int(request.POST.get('page', 1))
            self.is_recent = request.POST.get('is_recent', 'true')
            self.is_alphabetic = request.POST.get('is_alphabetic', 'ignored')
        else:
            return HttpResponseBadRequest()

        self.object_list =  self.model.objects.filter(isPublished=True)
        self.object_list = in_order(self.object_list, self.is_recent)
        self.object_list = in_alphabetic(self.object_list, self.is_alphabetic)

        if request.method == "POST":
            # Filter posts by date filters specified
            relative_this = request.POST.get('relative_this')
            match (relative_this):
                case 'this_day':
                    self.object_list = U.get_this_day_posts(self.object_list)
                case 'this_week':
                    self.object_list = U.get_this_week_posts(self.object_list)
                case 'this_month':
                    self.object_list = U.get_this_month_posts(self.object_list)
                case 'this_year':
                    self.object_list = U.get_this_year_posts(self.object_list)

            week_days = json.loads(request.POST['week_day'])
            self.object_list = U.get_posts_by_week_days(week_days, self.object_list)
            month_days = json.loads(request.POST['month_day'])
            self.object_list = U.get_posts_by_month_days(month_days, self.object_list)
            months = json.loads(request.POST['month'])
            self.object_list = U.get_posts_by_months(months, self.object_list)
            years = json.loads(request.POST['year'])
            self.object_list = U.get_posts_by_years(years, self.object_list)
            letters = json.loads(request.POST['letter'])
            self.object_list = U.get_posts_by_letters(letters, self.object_list)
            platforms_id = json.loads(request.POST['platform'])
            platforms = Post_M.Platform.objects.filter(id__in=platforms_id)
            self.object_list = U.get_posts_by_platforms(platforms, self.object_list)

            if len(self.object_list) == 0:
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Ничего не нашёл.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)

        self.tags_names = []
        if request.method == "GET":
            self.tags = request.GET.getlist('tag', [])
        elif request.method == "POST":
            self.tags = json.loads(request.POST['tag'])
        else: 
            return HttpResponseBadRequest()
        
        if len(self.tags) > 0:
            # Search everywhere !!!
            tag_obj = Post_M.Tag.objects.filter(Q(name_ru__in=self.tags) | Q(name_en__in=self.tags) | Q(slug_ru__in=self.tags)  | Q(slug_en__in=self.tags))
            if (len(self.tags) != len(tag_obj)) or tag_obj is None:
                if request.method == "GET":
                    raise Http404(_("Такого тега не существует, или он введён с ошибкой"))
                elif request.method == "POST":
                    return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Такого тега не существует, или он введён с ошибкой'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
                else:
                    return HttpResponseBadRequest()

            for key, tag in enumerate(tag_obj):
                self.tags[key] = tag.slug
            for key, tag in enumerate(tag_obj):
                self.tags_names.append(tag.name)

            self.object_list = U.getAllWithTags(self.object_list, tag_obj)

        if len(self.object_list) == 0:
            if request.method == "POST":
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Ничего не нашёл.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
            elif request.method == "GET":
                raise Http404()
            else:
                return HttpResponseBadRequest()

        # Create a paginator
        self.pages = calculate_pages(len(self.object_list), self.website_conf.paginator_per_page_posts)
        if self.page > self.pages :
            if request.method == "GET":
                raise Http404(_("Так много страниц у меня нет."))
            elif request.method == "POST":
                return render(request, 'PagiScroll/not_found_posts.html', context={'message': _('Так много страниц у меня нет.'), 'kaomodji': '(っ °Д °;)っ'}, status=404)
            else:
                return HttpResponseBadRequest()


        self.object_list = self.object_list[(self.page-1) * self.website_conf.paginator_per_page_posts : self.page * self.website_conf.paginator_per_page_posts]
        self.context = self.get_context_data()
        self.context.update(U.initDefaults(request))

        return None

def calculate_pages(total_items, items_per_page):
    if total_items <= 0 or items_per_page <= 0:
        return 1
    
    return -(-total_items // items_per_page)  # Using ceiling division

def in_order(queryset, is_recent):
    if is_recent == 'true':
        order = '-timeCreated'
    else:
        order = 'timeCreated'
    # Resort posts by time of creation
    return queryset.order_by(order)

def in_alphabetic(queryset, is_alphabetic):
    if is_alphabetic != 'ignored':
        if is_alphabetic == 'true':
            order = '-termin'
        else:
            order = 'termin'
        # Resort posts by alphabet
        return queryset.order_by(order)
    else:
        return queryset