from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .conf import settings

from wcd_jwt.views import TokenViewBase


__all__ = (
    'TokenExpireView',
    'token_expire_view',
    'make_urlpatterns',
)


class TokenExpireView(TokenViewBase):
    """
    Expires any provided token.
    """
    _serializer_class = settings.TOKEN_EXPIRE_SERIALIZER


token_expire_view = TokenExpireView.as_view()


def make_urlpatterns(
    expire_view=token_expire_view,
):
    return [
        path('expire/', csrf_exempt(expire_view), name='refresh'),
    ]
