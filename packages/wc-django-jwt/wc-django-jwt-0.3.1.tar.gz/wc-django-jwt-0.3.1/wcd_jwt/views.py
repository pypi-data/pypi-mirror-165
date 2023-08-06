from typing import Optional
from django.urls import path
from django.dispatch import Signal
from django.contrib.auth import login
from rest_framework_simplejwt.views import (
    TokenViewBase as _TokenViewBase, TokenVerifyView,
    token_verify as token_verify_view,
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status

from .conf import settings
from .signals import token_obtained, token_refreshed


__all__ = (
    'TokenRefreshView', 'TokenObtainView', 'TokenVerifyView',
    'token_refresh_view', 'token_obtain_view', 'token_verify_view',
    'make_urlpatterns',
)


class TokenViewBase(_TokenViewBase):
    notify_signal: Optional[Signal] = None

    def commit(self, serializer) -> dict:
        return (
            serializer.commit()
            if hasattr(serializer, 'commit')
            else serializer.validated_data
        )

    def notify(self, result: dict, serializer, request):
        if self.notify_signal is not None:
            self.notify_signal.send(
                self.__class__, result=result, serializer=serializer,
                request=request,
            )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)

        try:
            self.serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        result = self.commit(self.serializer)
        self.notify(result=result, serializer=self.serializer, request=request)

        return Response(result, status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    notify_signal = token_refreshed
    _serializer_class = settings.TOKEN_REFRESH_SERIALIZER


class TokenObtainView(TokenViewBase):
    """
    Takes a set of user credentials and returns a JSON web token to prove the
    authentication of those credentials.
    """
    notify_signal = token_obtained
    _serializer_class = settings.TOKEN_OBTAIN_SERIALIZER


class WithSessionTokenObtainView(TokenObtainView):
    """
    Takes a set of user credentials and returns a JSON web token to prove the
    authentication of those credentials.
    """
    def commit(self, serializer) -> dict:
        if self.serializer.is_valid():
            login(self.request, serializer.user)

        return super().commit(serializer)


token_refresh_view = TokenRefreshView.as_view()
token_obtain_view = TokenObtainView.as_view()
with_session_token_obtain_view = WithSessionTokenObtainView.as_view()


def make_urlpatterns(
    obtain_view=with_session_token_obtain_view,
    refresh_view=token_refresh_view,
    verify_view=token_verify_view,
):
    return [
        path('obtain/', csrf_exempt(obtain_view), name='obtain'),
        path('refresh/', csrf_exempt(refresh_view), name='refresh'),
        path('verify/', csrf_exempt(verify_view), name='verify'),
    ]
