from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .resolver import resolve_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        # Default django's authentication middleware could already
        # authenticate user. So there is no sense to do it by our own.
        if hasattr(request, 'user'):
            if request.user.is_authenticated:
                return

        request.user = SimpleLazyObject(lambda: resolve_user(request)[0])
