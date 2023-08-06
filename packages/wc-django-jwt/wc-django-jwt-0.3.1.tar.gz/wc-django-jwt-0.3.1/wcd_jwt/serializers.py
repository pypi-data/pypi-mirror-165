from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer as _TokenObtainSerializer

)

from .conf import settings


class TokenObtainSerializer(_TokenObtainSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {'user': self.user}

    def commit(self):
        return {}


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        data['refresh'] = self.get_token(data['user'])
        data['access'] = data['refresh'].access_token

        return data

    def commit(self):
        v = self.validated_data

        return {'refresh': str(v['refresh']), 'access': str(v['access'])}


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        data['refresh'] = self.token_class(attrs['refresh'])
        data['access'] = data['refresh'].access_token

        return data

    def commit(self):
        refresh = self.validated_data['refresh']
        data = {'access': str(self.validated_data['access'])}

        if settings.ROTATE_REFRESH_TOKENS:
            # TODO: Rework it to make some sort of token `.clone()`.
            updated = self.token_class(str(refresh))
            updated.set_jti()
            updated.set_exp()
            updated.set_iat()

            data["refresh"] = str(updated)

        return data


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        # Will raise if something wrong with token.
        UntypedToken(attrs["token"])

        return attrs

    def commit(self):
        return {}
