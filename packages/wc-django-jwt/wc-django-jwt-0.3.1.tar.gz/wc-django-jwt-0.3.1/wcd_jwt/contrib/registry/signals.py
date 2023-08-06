from django.dispatch import Signal


token_pairs_registered = Signal()
tokens_connected = Signal()
tokens_expired = Signal()

registration_pipeline_run = Signal()
