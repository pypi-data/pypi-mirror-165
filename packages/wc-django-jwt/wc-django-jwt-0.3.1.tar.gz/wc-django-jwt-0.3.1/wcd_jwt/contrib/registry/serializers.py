from django.utils.translation import pgettext_lazy

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import Token as TokenStruct

from wcd_jwt.serializers import TokenRefreshSerializer as _TokenRefreshSerializer
from wcd_jwt.services import token_resolver

from .services import token_manager


__all__ = 'TokenExpirationCheckMixin', 'TokenRefreshSerializer',


class TokenExpirationCheckMixin:
    default_error_messages = {
        'token_expired': pgettext_lazy(
            'wcd_jwt', 'Token is not longer valid.',
        )
    }

    def is_expired(self, token: TokenStruct):
        return token_manager.check_expired(token)

    def validate(self, attrs):
        data = super().validate(attrs)

        # TODO: Rework this as there could be no field with that name:
        token = data.get('refresh')

        if token is not None:
            if self.is_expired(token):
                raise ValidationError(
                    self.error_messages['token_expired'], 'token_expired',
                )

        return data


class TokenRefreshSerializer(TokenExpirationCheckMixin, _TokenRefreshSerializer):
    pass


class TokenExpireSerializer(serializers.Serializer):
    default_error_messages = {
        'token_expired': pgettext_lazy(
            'wcd_jwt', 'Token is not longer valid.',
        )
    }

    token = serializers.CharField(required=True)
    affect_tree = serializers.BooleanField(required=False, default=False)

    def validate_token(self, value):
        token = token_resolver.resolve_valid(value, silent=True)

        if token is None or token_manager.check_expired(token, silent=True):
            raise ValidationError(
                self.error_messages['token_expired'], 'token_expired',
            )

        return token

    def commit(self):
        token_manager.expire(
            (self.validated_data['token'],),
            affect_tree=self.validated_data['affect_tree'],
        )

        return {}
