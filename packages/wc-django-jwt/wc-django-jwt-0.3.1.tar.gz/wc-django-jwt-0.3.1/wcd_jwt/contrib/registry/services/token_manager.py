from datetime import datetime
from typing import List, Optional, Sequence, Tuple
from itertools import groupby
from django.utils.translation import pgettext_lazy

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import Token as TokenStruct
from rest_framework_simplejwt.utils import datetime_from_epoch

# FIXME: This should not be here!
from wcd_device_recognizer.utils import model_bulk_get_or_create
from wcd_jwt.utils import get_token_jti

from ..models import Token
from ..signals import token_pairs_registered, tokens_expired


__all__ = 'check_expired', 'expire', 'register',

TokenPair = Tuple[TokenStruct, Optional[TokenStruct]]


def check_expired(token: TokenStruct, silent: bool = True) -> bool:
    exists = Token.objects.filter(jti=get_token_jti(token)).expired().exists()

    if not silent and exists:
        raise InvalidToken(
            pgettext_lazy('wcd_jwt', 'Token is not longer valid.'),
            code='token_expired',
        )

    return exists


def expire(
    tokens: Sequence[TokenStruct],
    affect_tree: bool = False,
    exclude: Optional[Sequence[TokenStruct]] = None,
):
    tree = (
        Token.objects
        .filter(jti__in=map(get_token_jti, tokens))
        .values_list('id', flat=True)
    )

    if affect_tree:
        tree = Token.objects.collect_tree(ids=tree)

    if len(tree) == 0:
        return []

    q = Token.objects.filter(id__in=tree).active()

    if exclude is not None and len(exclude) > 0:
        q = q.exclude(jti__in=map(get_token_jti, exclude))

    q.set_expired()

    tokens_expired.send(None, tokens=q, tree_affected=affect_tree)

    return tree


def simplify_token(token: TokenStruct) -> Tuple[str, str, datetime]:
    return (
        get_token_jti(token), str(token),
        datetime_from_epoch(token.payload['exp']),
    )


def _count_nested_list(nested: List[list], depth: int) -> int:
    # Recursion fix.
    if depth == 0:
        return 0

    depth -= 1

    return len(nested) + sum((
        _count_nested_list(inside, depth)
        for inside in nested
    ), 0)


def register(pairs: Sequence[TokenPair]) -> List[TokenPair]:
    resolved = [
        (
            simplify_token(child),
            simplify_token(parent) if parent is not None else None,
        )
        for child, parent in pairs
    ]
    parents = {}
    ids = {}

    # Collecting strange parents tree to find out how many parents to
    # resolve each of children has.
    for child, parent in resolved:
        parents[child] = parents.get(child, [])

        if parent is not None:
            parents[parent] = parents.get(parent, [])
            parents[child].append(parents[parent])

    total = len(parents)
    weight_sorted = sorted([
        (_count_nested_list(nested, total), i)
        for i, nested in parents.items()
    ])
    chunks = groupby(weight_sorted, key=lambda x: x[0])
    parents_map = dict(resolved)
    result = {}

    for _, items in chunks:
        items = [v for _, v in items]

        tokens = model_bulk_get_or_create(Token, [
            (
                {
                    'jti': value[0], 'token': value[1],
                },
                {
                    'parent_id': ids.get(parents_map.get(value)),
                    'expired_at': value[2], 'internal_expired_at': value[2],
                },
            )
            for value in items
        ])
        result.update(zip(items, tokens))
        ids.update(zip(items, (x.id for x in tokens)))

    result_pairs = [
        (result[child], result[parent] if parent is not None else None)
        for child, parent in resolved
    ]

    token_pairs_registered.send(None, source=pairs, result=result_pairs)

    return result_pairs
