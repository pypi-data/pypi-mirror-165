from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .discovery import autodiscover


__all__ = ('JWTConfig',)


class JWTConfig(AppConfig):
    name = 'wcd_jwt'
    verbose_name = pgettext_lazy('wcd_jwt', 'JWT authentication')

    def ready(self):
        autodiscover()
        from . import subscriptions
