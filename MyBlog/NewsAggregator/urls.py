from django.urls import path
from .views import tool_main

urlpatterns = [
    path('news-aggregator/', tool_main, name='news_aggregator'),
]
