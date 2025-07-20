from django.urls import path
from . import views as V


urlpatterns = [
    path('editor/', V.tool_main, name='editor_home'),
    path('editor/list/', V.templates_list),
    path('editor/delete/', V.delete_template),
    path('editor/upload/', V.upload_template),
    path('editor/save/', V.save_template),
    path('editor/load_table_of_content/', V.load_table_of_content),
]
