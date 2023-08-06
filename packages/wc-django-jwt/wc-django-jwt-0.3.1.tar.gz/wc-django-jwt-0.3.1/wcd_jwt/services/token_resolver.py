from typing import Sequence, Type, Optional
from django.utils.translation import pgettext_lazy

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from ..conf import settings
from ..utils import cached_import_string


def get_all_token_types():
    return [cached_import_string(x) for x in settings.TOKEN_TYPES]


def resolve_valid(
    raw_token: str,
    from_classes: Optional[Sequence[Type]] = None,
    silent: bool = False,
):
    """
    Validates an encoded JSON web token and returns a validated token
    wrapper object.
    """
    messages = []
    if from_classes is None:
        from_classes = get_all_token_types()

    for AuthToken in from_classes:
        try:
            return AuthToken(raw_token)
        except TokenError as e:
            messages.append({
                'token_class': AuthToken.__name__,
                'token_type': AuthToken.token_type,
                'message': e.args[0],
            })

    if silent:
        return None

    raise InvalidToken({
        'detail': pgettext_lazy(
            'wcd_jwt', 'Given token not valid for any token type'
        ),
        'messages': messages,
    })
