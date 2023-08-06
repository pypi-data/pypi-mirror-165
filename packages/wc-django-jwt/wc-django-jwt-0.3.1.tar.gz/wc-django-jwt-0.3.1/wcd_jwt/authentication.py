from rest_framework_simplejwt.authentication import JWTAuthentication as Base
# TODO: Remove dependency over `api_settings`.
from rest_framework_simplejwt.settings import api_settings

from .services import token_resolver
from .signals import user_token_authenticated


class JWTAuthentication(Base):
    def get_validated_token(self, raw_token):
        print('shitt')
        return token_resolver.resolve_valid(
            raw_token, from_classes=api_settings.AUTH_TOKEN_CLASSES,
        )

    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, token = result
        user_token_authenticated.send(
            self.__class__, user=user, token=token, request=request
        )

        return user, token
