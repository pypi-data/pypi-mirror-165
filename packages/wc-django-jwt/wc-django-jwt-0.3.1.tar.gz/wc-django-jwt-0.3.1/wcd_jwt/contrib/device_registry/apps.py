from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('JWTDeviceRegistryConfig',)


class JWTDeviceRegistryConfig(AppConfig):
    name = 'wcd_jwt.contrib.device_registry'
    label = 'wcd_jwt_device_registry'
    verbose_name = pgettext_lazy('wcd_jwt', 'JWT Token device registry')
