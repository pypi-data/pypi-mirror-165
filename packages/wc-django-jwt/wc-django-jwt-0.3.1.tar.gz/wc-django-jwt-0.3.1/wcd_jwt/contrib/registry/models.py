from datetime import datetime
from typing import List, Optional, Sequence, Union
from uuid import uuid4, UUID
from django.db import models
from django.utils.translation import pgettext_lazy
from rest_framework_simplejwt.utils import aware_utcnow
from django.conf import settings


__all__ = 'Token', 'TokenUserConnection',


TokenID = Union[str, UUID]


class UUIDable(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        verbose_name=pgettext_lazy('wcd_jwt', 'ID'),
        primary_key=True, default=uuid4,
    )

    created_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_jwt', 'Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_jwt', 'Updated at'),
        auto_now=True
    )


class TokenQuerySet(models.QuerySet):
    def relatives(self, ids: Sequence[TokenID]):
        return self.filter(
            models.Q(parent_id__in=ids) | models.Q(id__in=ids)
        )

    def expired(self, now: Optional[datetime] = None):
        now = now if now else aware_utcnow()

        return self.filter(
            models.Q(expired_at__lt=now)
            |
            models.Q(internal_expired_at__lt=now)
        )

    def active(self, now: Optional[datetime] = None):
        now = now if now else aware_utcnow()

        return self.filter(
            models.Q(expired_at__gte=now)
            &
            models.Q(internal_expired_at__gte=now)
        )

    def set_expired(self, now: Optional[datetime] = None):
        return self.update(expired_at=now if now else aware_utcnow())

    def collect_tree(self, ids: Sequence[TokenID]) -> List[TokenID]:
        count_first = 0
        ids = set(ids) - {None}
        count_second = len(ids)

        while count_first != count_second:
            count_first = count_second
            relatives = (
                x
                for items in self.relatives(ids).values_list('id', 'parent_id')
                for x in items
            )
            ids = set(relatives) - {None}
            count_second = len(ids)

        return list(ids)


class Token(UUIDable):
    # type: models.Manager[TokenQuerySet]
    objects = TokenQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_jwt', 'Token')
        verbose_name_plural = pgettext_lazy('wcd_jwt', 'Tokens')

    jti = models.CharField(
        verbose_name=pgettext_lazy('wcd_jwt', 'JTI'), max_length=512,
        db_index=True,
    )
    token = models.TextField(
        verbose_name=pgettext_lazy('wcd_jwt', 'Token'), db_index=True,
    )

    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('wcd_jwt', 'Parent token'),
        null=True, blank=True,
    )

    expired_at = models.DateTimeField(pgettext_lazy('wcd_jwt', 'Expired at'))
    internal_expired_at = models.DateTimeField(
        pgettext_lazy('wcd_jwt', 'Expired at(internal)'), editable=False,
    )

    def __str__(self):
        return f'{self.jti}'


class TokenUserConnection(UUIDable):
    class Meta:
        verbose_name = pgettext_lazy('wcd_jwt', 'User token connection')
        verbose_name_plural = pgettext_lazy('wcd_jwt', 'User token connections')
        unique_together = (
            ('user', 'token',),
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='token_connections', on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_jwt', 'Connected user'),
    )
    token = models.ForeignKey(
        Token,
        related_name='user_connections', on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_jwt', 'Connected token'),
    )

    def __str__(self):
        return f'User #{self.user_id} token #{self.token_id}'
