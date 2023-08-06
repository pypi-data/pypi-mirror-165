from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf import settings

from jet.filters import RelatedFieldAjaxListFilter


User = get_user_model()

if 'wcd_jwt.contrib.registry' in settings.INSTALLED_APPS:
    from wcd_jwt.contrib.registry.models import Token, TokenUserConnection
    from wcd_jwt.contrib.registry.admin import TokenAdmin, TokenUserConnectionAdmin


    admin.site.unregister(Token)
    admin.site.unregister(TokenUserConnection)


    @admin.register(Token)
    class TokenWithFiltersAdmin(TokenAdmin):
        list_filter = (
            ('user_connections__user', RelatedFieldAjaxListFilter),
        )


    @admin.register(TokenUserConnection)
    class TokenUserConnectionWithFiltersAdmin(TokenUserConnectionAdmin):
        list_filter = (
            ('user', RelatedFieldAjaxListFilter),
            ('token', RelatedFieldAjaxListFilter),
        )


    if not hasattr(User, 'autocomplete_search_fields'):
        User.autocomplete_search_fields = staticmethod(lambda *a: ('username',))

    if not hasattr(Token, 'autocomplete_search_fields'):
        Token.autocomplete_search_fields = staticmethod(lambda *a: ('pk', 'token', 'jti',))


if 'wcd_jwt.contrib.device_registry' in settings.INSTALLED_APPS:
    from wcd_device_recognizer.models import Interlocutor, InterlocutorNetwork

    if not hasattr(Interlocutor, 'autocomplete_search_fields'):
        Interlocutor.autocomplete_search_fields = staticmethod(lambda *a: ('outer_id', 'user_agent',))
    if not hasattr(InterlocutorNetwork, 'autocomplete_search_fields'):
        InterlocutorNetwork.autocomplete_search_fields = staticmethod(lambda *a: ('interlocutor__user_agent', 'ip',))
