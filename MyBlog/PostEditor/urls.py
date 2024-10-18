from django.urls import path
from . import views as V


urlpatterns = [
    path('editor/', V.home, name='editor_home'),
    path('editor/list/', V.templates_list),
    path('editor/delete/', V.delete_template),
    path('editor/upload/', V.upload_template),
    path('editor/save/', V.save_template),
]
