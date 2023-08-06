from wcd_device_recognizer.services import registry, request_resolver
from wcd_jwt.contrib.registry.services.pipeline import flat_pairs

from . import connector


def connect_interlocutor(context):
    request, pairs = context.get('request'), context.get('registered_pairs')

    if request is None:
        return

    tokens = flat_pairs(pairs)
    interlocutor_dto = request_resolver.resolve(request)
    (interlocutor, network), = registry.register_interlocutors((
        interlocutor_dto,
    ))
    connections = connector.connect(
        interlocutor, tokens=tokens, network=network
    )

    return {
        'interlocutor': interlocutor,
        'interlocutor_dto': interlocutor_dto,
        'interlocutor_network': network,
        'interlocutor_connections': connections,
    }
