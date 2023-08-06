from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('JWTJetConfig',)


class JWTJetConfig(AppConfig):
    name = 'wcd_jwt.contrib.jet'
    label = 'wcd_jwt_jet'
    verbose_name = pgettext_lazy('wcd_jwt', 'JWT Token jet integration')
