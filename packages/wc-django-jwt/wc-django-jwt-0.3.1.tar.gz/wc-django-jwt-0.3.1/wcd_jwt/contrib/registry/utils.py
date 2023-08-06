import threading
from functools import wraps

from .conf import settings


def maybe_parallel_execution(callback, args, kwargs):
    if settings.TOKEN_REGISTRATION_ON_SIGNAL_PARALLEL:
        thread = threading.Thread(target=callback, args=args, kwargs=kwargs, daemon=True)
        thread.start()
    else:
        callback(*args, **kwargs)


def may_parallel(callback):
    @wraps(callback)
    def wrapper(*a, **kw):
        return maybe_parallel_execution(callback, a, kw)

    return wrapper
