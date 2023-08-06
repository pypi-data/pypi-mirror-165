from dataclasses import dataclass, field
from functools import partial
from typing import Optional, Sequence
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


def get_simplejwt_setting(key: str, default: Optional[str] = None):
    result = default

    if hasattr(simple_jwt_settings, key):
        result = getattr(simple_jwt_settings, key)

    from rest_framework_simplejwt.settings import api_settings

    return (
        result
        if result is not None else
        default
        if default is not None else
        getattr(api_settings, key)
    )


pjwt = partial(partial, get_simplejwt_setting)


@s('SIMPLE_JWT')
@dataclass
class SimpleJWTSettings:
    TOKEN_OBTAIN_SERIALIZER: Optional[str] = None
    TOKEN_REFRESH_SERIALIZER: Optional[str] = None
    ROTATE_REFRESH_TOKENS: Optional[bool] = None
    UPDATE_LAST_LOGIN: Optional[bool] = None


@s('WCD_JWT')
@dataclass
class Settings:
    TOKEN_OBTAIN_SERIALIZER: str = field(default_factory=pjwt(
        'TOKEN_OBTAIN_SERIALIZER',
        'wcd_jwt.serializers.TokenObtainPairSerializer',
    ))
    TOKEN_REFRESH_SERIALIZER: str = field(default_factory=pjwt(
        'TOKEN_REFRESH_SERIALIZER',
        'wcd_jwt.serializers.TokenRefreshSerializer',
    ))
    ROTATE_REFRESH_TOKENS: bool = field(
        default_factory=pjwt('ROTATE_REFRESH_TOKENS')
    )
    UPDATE_LAST_LOGIN: bool = field(
        default_factory=pjwt('UPDATE_LAST_LOGIN')
    )
    TOKEN_TYPES: Sequence[str] = field(default_factory=lambda: [
        'rest_framework_simplejwt.tokens.AccessToken',
        'rest_framework_simplejwt.tokens.RefreshToken',
    ])

    AUTHENTICATION_CLASS: str = 'wcd_jwt.authentication.JWTAuthentication'


simple_jwt_settings = SimpleJWTSettings()
settings = Settings()
