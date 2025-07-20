from django.urls import path, include

from rest_framework.renderers import TemplateHTMLRenderer

from .views import FeedListView, FeedDetailedView, FeedPostListView, FeedIdDetailedView
from .serializers import FeedSerializer, FeedGroupSerializer, FeedIdSerializer
from .models import Feed, FeedGroup, FeedId
from .views import tool_main 


urlpatterns = [
    path('rss-reader/', tool_main, name='rss-reader'),
    path('rss-reader/posts/', FeedPostListView.as_view(serializer_class=FeedSerializer, queryset=Feed.objects.all()), name="rss-reader-posts"),
    path('rss-reader/feeds/', FeedListView.as_view(serializer_class=FeedSerializer, queryset=Feed.objects.all())),
    path('rss-reader/feeds/<int:pk>/', FeedDetailedView.as_view(serializer_class=FeedSerializer, queryset=Feed.objects.all())),
    path('rss-reader/user-id/<str:user_id>/', FeedIdDetailedView.as_view(serializer_class=FeedIdSerializer, queryset=FeedId.objects.all())),
]
