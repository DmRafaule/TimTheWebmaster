import feedparser
import ssl

from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseBadRequest 
from django.template.response import TemplateResponse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination

from Main.utils import initDefaults
from .models import Feed, FeedId, FeedGroup
from .forms import FeedAddFormEmpty, FeedAddFormWithName, FeedIdForm


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
    
class CustomNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = 10

class FeedListView(
    generics.mixins.ListModelMixin, 
    generics.mixins.CreateModelMixin, 
    generics.mixins.DestroyModelMixin, 
    generics.mixins.UpdateModelMixin, 
    generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'RSSAggregator/feed_edit_dynamic_added_root.html'

    def get_queryset(self):
        queryset = self.queryset 
        id = self.request.query_params.get('user_id')
        if id is not None:
            queryset = queryset.filter(user_id__in=id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        modified_request_data = request.data.copy()
        user_id, is_created = FeedId.objects.get_or_create(user_id=request.session.session_key)
        modified_request_data['user_id'] = user_id.pk
        serializer = self.get_serializer(data=modified_request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        form =  FeedAddFormWithName(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'feed_form': form, 'id': serializer.data['id'], 'messages': [_("Успешно добавил фид")] }, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class FeedPostListView(
    generics.mixins.ListModelMixin, 
    generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'RSSAggregator/rss-pagination.html'
    pagination_class = CustomNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'queryset': list(self.filter_queryset(self.get_queryset()))})
        return context

    def get_queryset(self):
        user_str_id = self.request.session.session_key
        user_id, is_created = FeedId.objects.get_or_create(user_id=user_str_id)
        queryset = get_queryset_feed_by_user_id(user_id) 
        feed = self.request.query_params.getlist('feed')
        if feed is not None:
            queryset = queryset.filter(feed__in=feed)
        return queryset

    def get(self, request, *args, **kwargs):
        user_str_id = self.request.session.session_key
        user_id, is_created = FeedId.objects.get_or_create(user_id=user_str_id)
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) > 0:
            posts = get_all_posts(queryset.values_list('feed', flat=True), user_id.get_sort_direction())
        else:
            feeds_list = request.query_params.getlist('feed')
            posts = get_all_posts(feeds_list, user_id.get_sort_direction())
        self.paginator.max_page_size = user_id.posts_per_page
        page = self.paginate_queryset(posts)
        if page is not None:
            return Response({"posts": page, "next_link": self.paginator.get_next_link(), 'isPreview': user_id.with_previews})

        return Response({"posts": page})
    
class FeedDetailedView(
    MultipleFieldLookupMixin, 
    generics.RetrieveAPIView, 
    generics.CreateAPIView, 
    generics.DestroyAPIView, 
    generics.UpdateAPIView, 
    generics.GenericAPIView):
    lookup_fields = ['pk']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'RSSAggregator/feed_edit_dynamic_added_root.html'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'is_delete': True})

    def put(self, request, *args, **kwargs):
        messages = []
        messages.append(_("Что-то пошло не так. Не смог обновить фид. ＼（〇_ｏ）／"))
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        form =  FeedAddFormWithName(serializer.data)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        messages[0] = _("Успешно обновил фид. （￣︶￣）↗　")
        return Response({'data': serializer.data, 'feed_form': form, 'id': serializer.data['id'], 'messages': messages})

class FeedIdDetailedView(
    generics.RetrieveAPIView, 
    generics.UpdateAPIView, 
    generics.GenericAPIView):
    lookup_field = ['user_id']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'RSSAggregator/feedId_settings_form.html'


    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        user_str_id = self.kwargs['user_id']
        user_id, is_created = FeedId.objects.get_or_create(user_id=user_str_id)
        obj = get_object_or_404(queryset, user_id=user_id)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        messages = []
        messages.append(_("Что-то пошло не так. Не смог обновить настройки. ＼（〇_ｏ）／"))
        user_str_id = self.kwargs['user_id']
        instance = self.get_object()
        form = FeedIdForm(request.data)
        if form.is_valid():
            try:
                user = get_object_or_404(FeedId, user_id=form.cleaned_data['previos_user_id'])
                instance.similar_user_id.add(user)
                instance.sort = form.cleaned_data['sort']
                instance.posts_per_page = form.cleaned_data['posts_per_page']
                instance.with_previews = form.cleaned_data['with_previews']
                instance.save()
                messages[0] = _("Успешно обновил настройки пользователя. （￣︶￣）↗　")
                form = FeedIdForm(instance=instance)
            except:
                instance.sort = form.cleaned_data['sort']
                instance.posts_per_page = form.cleaned_data['posts_per_page']
                instance.with_previews = form.cleaned_data['with_previews']
                instance.save()
                messages[0] = _("Такого пользователя не существует ＞︿＜")
                form = FeedIdForm(instance=instance)

        return Response({'feed_form': form, 'user_id': user_str_id, 'messages': messages})


def sort_by_date(element):
    return element.published_parsed

def get_all_posts(feed_urls, sort):
    feed_items = []
    for source in feed_urls:
        feed_items += feedparser.parse(source)['entries']

    if sort:
        feed_items.sort(key=sort_by_date, reverse=True)
    else:
        feed_items.sort(key=sort_by_date)


    posts = []
    for item in feed_items:
        image_link = ""
        for link in item.links:
            if link['type'] == 'image/jpeg':
                image_link = link['href']
        posts.append({
            'title' : item.title,
            'date_published': item.published,
            'description': item.description,
            'link': item.link,
            'image_link': image_link

        })
    return posts

def get_posts(feed_urls: list, sort: bool=True, offset: int=0, posts_per_page: int=CustomNumberPagination.max_page_size):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    feed_items = []
    for source in feed_urls:
        feed_items += feedparser.parse(source)['entries']
    
    if sort:
        feed_items.sort(key=sort_by_date, reverse=True)
    else:
        feed_items.sort(key=sort_by_date)


    # Add model field to hold parsed data
    posts = []
    for item in feed_items[offset:offset + posts_per_page]:
        image_link = ""
        for link in item.links:
            if link['type'] == 'image/jpeg':
                image_link = link['href']
        posts.append({
            'title' : item.title,
            'date_published': item.published,
            'description': item.description,
            'link': item.link,
            'image_link': image_link

        })
    
    return posts

def get_queryset_feed_by_user_id(user_id: FeedId):
    user_feeds_queryset = Feed.objects.filter(user_id=user_id)
    for sim_id in user_id.similar_user_id.all():
        user_feeds_queryset |= Feed.objects.filter(user_id=sim_id)
    
    return user_feeds_queryset

def tool_main(request):
    context = initDefaults(request)

    user_str_id = request.session.session_key
    user_id, is_created = FeedId.objects.get_or_create(user_id=user_str_id)


    if request.method == "GET":
        # Get feeds in use right now
        feed_urls = request.GET.getlist('feed', [])
        # Build empty form to submit new feed
        if len(feed_urls) > 0:
            add_feed_empty = FeedAddFormEmpty(request.GET)
            if add_feed_empty.is_valid():
                add_feed_empty = FeedAddFormEmpty(user_id=user_id)
        else:
            add_feed_empty = FeedAddFormEmpty(user_id=user_id)
        context.update({'feed_add_empty': add_feed_empty})
    else: 
        return HttpResponseBadRequest()

    # Get the user's saved feeds
    user_feeds = []
    user_feeds_queryset = get_queryset_feed_by_user_id(user_id)
    for user_feed_rec in user_feeds_queryset:
        form = FeedAddFormWithName(id=user_feed_rec.pk, name=user_feed_rec.name, feed=user_feed_rec.feed)
        to_add = True
        if user_feed_rec.feed in feed_urls:
            to_add = False
        user_feeds.append({'form': form, 'id': user_feed_rec.pk, 'to_add': to_add})

    # Get the user's saved feed groups
    user_feed_groups = []
    feed_groups = FeedGroup.objects.filter(user_id=user_id)
    for feed_group in feed_groups:
        flat_values_by_pk_of_feeds_in_group = feed_group.feeds.all().values_list('pk', flat=True)
        for user_feed in user_feeds_queryset:
            if user_feed.pk in flat_values_by_pk_of_feeds_in_group:
                # Build the forms for them and append into feed groups
                form = FeedAddFormWithName(id=user_feed.pk, name=user_feed.name, feed=user_feed.feed)
                user_feed_groups.append({'form': form, 'id': user_feed.pk})
                # Remove user feeds that duplicates
                #for prev_user_feed in user_feeds:
                #    if prev_user_feed.get('id') in flat_values_by_pk_of_feeds_in_group:
                #        user_feeds.remove(prev_user_feed)

    context.update({'user_feed_groups': user_feed_groups})
    context.update({'user_feeds': user_feeds})
    
    # Build forms for feeds in use right now
    add_feed_not_empty_list = []
    for url in feed_urls:
        # Build a request to validate form
        form_data = request.GET.copy()
        form_data['feed'] = url
        form = FeedAddFormEmpty(form_data)
        if form.is_valid():
            to_add = True
            if url in user_feeds_queryset.values_list('feed', flat=True):
                to_add = False
            add_feed_not_empty_list.append({'form': form, 'id': form.feed_id, 'to_add': to_add})
    
    # Build settings form
    feedId_form = FeedIdForm(instance=user_id)
    context.update({'feedId_form': feedId_form})    
    context.update({'feed_add_not_empty_list': add_feed_not_empty_list})
    context.update({'feed_urls': feed_urls})
    context.update({'posts': get_posts(feed_urls, posts_per_page=user_id.posts_per_page, sort=user_id.get_sort_direction())})
    context.update({'isPreview': user_id.with_previews})
    context.update({'user_id': user_id.user_id})
    context.update({'page_query_param': CustomNumberPagination.page_query_param})
    context.update({'page_size_query_param': CustomNumberPagination.page_size_query_param})

    return TemplateResponse(request, 'RSSAggregator/rss-aggregator.html', context=context)