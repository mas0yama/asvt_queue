# https://stackoverflow.com/a/48408333/15287569
# https://stackoverflow.com/a/49037059/15287569

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        open_urls = getattr(settings, 'OPEN_URLS', [])
        self.open_urls = [self.login_url] + [reverse_lazy(url) for url in open_urls]

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated or request.path_info in self.open_urls:
            return
        return login_required(view_func)(request, *view_args, **view_kwargs)
