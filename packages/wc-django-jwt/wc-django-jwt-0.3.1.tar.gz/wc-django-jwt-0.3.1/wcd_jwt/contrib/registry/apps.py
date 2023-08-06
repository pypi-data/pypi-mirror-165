from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('JWTRegistryConfig',)


class JWTRegistryConfig(AppConfig):
    name = 'wcd_jwt.contrib.registry'
    label = 'wcd_jwt_registry'
    verbose_name = pgettext_lazy('wcd_jwt', 'JWT Token registry')

    def ready(self):
        from . import subscriptions
