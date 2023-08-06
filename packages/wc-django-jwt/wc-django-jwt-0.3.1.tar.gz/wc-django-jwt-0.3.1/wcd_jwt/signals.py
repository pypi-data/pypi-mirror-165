from django.dispatch import Signal


token_obtained = Signal()
token_refreshed = Signal()

user_token_authenticated = Signal()
