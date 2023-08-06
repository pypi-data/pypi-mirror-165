from datetime import datetime
from typing import Optional

from rest_framework_simplejwt.utils import aware_utcnow

from ..models import Token


def archive(now: Optional[datetime] = None):
    now = aware_utcnow() if now is None else now

    return Token.objects.filter(internal_expired_at__lte=now).delete()
