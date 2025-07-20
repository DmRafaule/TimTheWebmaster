from django.urls import path

from . import views as V


# УРЛ паттерны для отображения постов типа Статей и Инструментов
# Причём, паттерн для инструментов будет отображать только те инструменты
# которые без шаблона, или же с шаблоно но всё ещё не отдельные Django-приложения
urlpatterns = [
    path('articles/<slug:post_slug>/', V.article, name="article"),
    path('tools/<slug:post_slug>/', V.tool, name="tool"),
]