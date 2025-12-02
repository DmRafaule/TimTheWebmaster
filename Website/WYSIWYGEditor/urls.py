from django.urls import path
from . import views as V


urlpatterns = [
    path('wysiwyg-editor/', V.tool_main, name='editor_home'),
    path('wysiwyg-editor/delete/', V.delete_template),
    path('wysiwyg-editor/upload/', V.upload_template),
    path('wysiwyg-editor/list/', V.list_templates),
    path('wysiwyg-editor/save/', V.save_template),
    path('wysiwyg-editor/get-save-form/', V.save_form),
]
