from django.urls import path
from .views import tool_main, init, start, stop, update_status, update_logs


urlpatterns = [
    path('image_thief/', tool_main, name='image_thief'),
    path('image_thief-start/', start),
    path('image_thief-init/', init),
    path('image_thief-stop/', stop),
    path('image_thief-tabclosed/', stop),
    path('image_thief-update_status/', update_status),
    path('image_thief-update_logs/', update_logs),
]
