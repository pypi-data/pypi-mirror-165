from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed, InvalidToken,
)

from .utils import cached_import_string
from .conf import settings


def resolve_user(request: HttpRequest):
    AuthenticationClass: BaseAuthentication = cached_import_string(
        settings.AUTHENTICATION_CLASS
    )
    result = None

    try:
        result = AuthenticationClass().authenticate(request)
    except (InvalidToken, AuthenticationFailed) as e:
        pass

    if result is None:
        return AnonymousUser(), None

    return result
