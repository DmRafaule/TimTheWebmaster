from django.urls import path
from .views import PostListView
from Post.models import Article, Tool, Note, Category


urlpatterns = [
    path('articles/', PostListView.as_view(model=Article, template_name='PagiScroll/article_list.html', category=Category.objects.get(slug='articles')), name='articles-list'),
    path('tools/', PostListView.as_view(model=Tool, template_name='PagiScroll/tool_list.html', category=Category.objects.get(slug='tools')), name='tools-list'),
    path('notes/', PostListView.as_view(model=Note, template_name='PagiScroll/note_list.html', category=Category.objects.get(slug='notes')), name='notes-list'),
]