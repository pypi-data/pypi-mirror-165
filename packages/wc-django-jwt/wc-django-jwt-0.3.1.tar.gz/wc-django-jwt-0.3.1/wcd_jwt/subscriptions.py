from django.dispatch import receiver
from django.contrib.auth.models import update_last_login

from .signals import token_obtained, token_refreshed
from .conf import settings


@receiver(token_obtained)
def update_last_login_on_token_obtain(sender, serializer, **kwargs):
    if settings.UPDATE_LAST_LOGIN:
        update_last_login(None, serializer.validated_data['user'])
