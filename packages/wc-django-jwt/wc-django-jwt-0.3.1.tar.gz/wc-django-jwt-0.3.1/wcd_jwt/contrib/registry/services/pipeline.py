from typing import Tuple
from px_pipeline import Filter, StraightPipeline
from functools import lru_cache
from django.contrib.auth import get_user_model

from ..conf import settings
from ..signals import registration_pipeline_run

from . import token_manager, user_connector


registration_filter = Filter()


def flat_pairs(pairs):
    return [y for x in pairs for y in x]


@lru_cache
def _cached_pipeline(pipeline: Tuple):
    return StraightPipeline(pipeline)


def register_pairs(context):
    pairs = context.get('pairs')

    if pairs is None:
        return

    return {'registered_pairs': token_manager.register(pairs)}


def connecting_user(context):
    user, pairs = context.get('user'), context.get('registered_pairs')

    if len(pairs) == 0:
        return

    if user is None:
        # Searching for user connections of the previous token(s).
        # To connect them. If there is more than one user - something
        # wrong happened and no connection will be established.
        users = list(
            get_user_model().objects
            .filter(token_connections__token__in=flat_pairs(pairs))
        )

        if len(users) != 1:
            return

        user = users[0]

    return {'connections': user_connector.connect(user, flat_pairs(pairs))}


def run(context: dict) -> dict:
    result = registration_filter(
        _cached_pipeline(tuple(settings.TOKEN_REGISTRATION_PIPELINE))(context)
    )

    registration_pipeline_run.send(None, result=result)

    return result
