from django.urls import path
from .views import tool_main, loadFeeds, submitFeed, deleteFeed, getFeedPosts

urlpatterns = [
    path('rss-reader/', tool_main, name='rss_aggregator'),
    path('rss-reader/load-feeds/', loadFeeds),
    path('rss-reader/submit-feed/', submitFeed),
    path('rss-reader/delete-feed/', deleteFeed),
    path('rss-reader/get-feed-posts/', getFeedPosts),
]
