import re
from .models import CommonNotification
from django.template.response import TemplateResponse

class FrameAncestorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = (
            "frame-ancestors timthewebmaster.com metrika.yandex.ru metrika.yandex.com metrika.yandex.by metrika.yandex.com.tr webvisor.com;"
        )
        return response

class CommonNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response: TemplateResponse):
        notification_objects = []
        # Here you will be check if URL match with slug of custom filter page
        notifications = CommonNotification.objects.all()
        values = notifications.values('regex_slug','id')
        for value in values:
            slug = value['regex_slug']
            id = value['id']
            if re.match(f'{slug}', request.get_full_path()) is not None:
                notification_objects.append(CommonNotification.objects.get(id=id))

        if len(notification_objects) > 0:
            response.context_data.update({'common_notifications': notification_objects})
            response.context_data.update({'isCommonNotification': True})

        return response