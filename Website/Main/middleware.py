

class FrameAncestorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = (
            "frame-ancestors timthewebmaster.com metrika.yandex.ru metrika.yandex.com metrika.yandex.by metrika.yandex.com.tr webvisor.com;"
        )
        return response
