from functools import lru_cache
from django.utils.module_loading import import_string
from rest_framework_simplejwt.tokens import Token as TokenStruct
from rest_framework_simplejwt.settings import api_settings


@lru_cache
def cached_import_string(path: str):
    return import_string(path)


def get_token_jti(token: TokenStruct) -> str:
    return token.payload[api_settings.JTI_CLAIM]
