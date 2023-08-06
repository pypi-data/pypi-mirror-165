from django.dispatch import receiver
from wcd_jwt.signals import token_refreshed, token_obtained

from .services import pipeline, token_manager
from .utils import may_parallel
from .conf import settings


@receiver(token_obtained)
@may_parallel
def register_token_on_obtain(sender, serializer, result, request, **kwargs):
    if not settings.TOKEN_REGISTRATION_ON_SIGNAL:
        return

    v = serializer.validated_data

    pipeline.run({
        'pairs': [(v['access'], v['refresh'])],
        'user': v.get('user') or None,
        'request': request,
    })


@receiver(token_refreshed)
@may_parallel
def register_token_on_refresh(sender, serializer, result, request, **kwargs):
    if not settings.TOKEN_REGISTRATION_ON_SIGNAL:
        return

    v = serializer.validated_data
    base = v['refresh']
    pairs = [(v['access'], base)]
    expiration = ((base,), (base,))

    if 'refresh' in result:
        refresh = serializer.token_class(result['refresh'])
        pairs = (
            # Wer'e replacing access token parent with newly generated refresh.
            # It's because we want to form a straight relation between
            # responded refresh->access tokens.
            (v['access'], refresh),
            (refresh, base),
        )
        expiration = ((base,), ())

    if settings.TOKEN_EXPIRE_ON_REFRESH:
        expire, exclude = expiration
        token_manager.expire(expire, affect_tree=True, exclude=exclude)

    pipeline.run({'pairs': pairs, 'request': request})
