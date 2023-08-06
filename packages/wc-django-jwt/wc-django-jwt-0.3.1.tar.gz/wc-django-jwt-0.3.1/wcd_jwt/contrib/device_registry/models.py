from django.db import models
from django.utils.translation import pgettext_lazy

from wcd_jwt.contrib.registry.models import UUIDable, Token
from wcd_device_recognizer.models import Interlocutor, InterlocutorNetwork


__all__ = 'TokenInterlocutorConnection',


class TokenInterlocutorConnection(UUIDable):
    class Meta:
        verbose_name = pgettext_lazy('wcd_jwt', 'Interlocutor token connection')
        verbose_name_plural = pgettext_lazy('wcd_jwt', 'Interlocutor token connections')

    interlocutor = models.ForeignKey(
        Interlocutor,
        related_name='token_connections', on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_jwt', 'Connected interlocutor'),
    )
    network = models.ForeignKey(
        InterlocutorNetwork,
        related_name='token_connections', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('wcd_jwt', 'Connected interlocutor network'),
        null=True, blank=True,
    )
    token = models.ForeignKey(
        Token,
        related_name='interlocutor_connections', on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_jwt', 'Connected token'),
    )

    def __str__(self):
        return f'Interlocutor #{self.interlocutor_id} token #{self.token_id}'
