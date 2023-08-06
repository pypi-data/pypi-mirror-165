from typing import List, Sequence, Optional
from wcd_device_recognizer.models import Interlocutor, InterlocutorNetwork
from wcd_device_recognizer.utils import model_bulk_get_or_create
from wcd_jwt.contrib.registry.models import Token

from ..models import TokenInterlocutorConnection
from ..signals import interlocutor_connected


def connect(
    interlocutor: Interlocutor,
    tokens: Sequence[Token],
    network: Optional[InterlocutorNetwork] = None,
) -> List[TokenInterlocutorConnection]:
    connections = model_bulk_get_or_create(TokenInterlocutorConnection, [
        ({'interlocutor': interlocutor, 'network': network, 'token': token}, {})
        for token in tokens
    ])

    interlocutor_connected.send(
        None, connections=connections, interlocutor=interlocutor,
        network=network, tokens=tokens,
    )

    return connections
