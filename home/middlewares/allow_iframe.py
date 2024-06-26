   
from django.http import HttpResponse

class AllowIframeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Frame-Options'] = 'http://127.0.0.1:8000/'  # Allow embedding from the same origin
        return response