from dataclasses import dataclass, field
from typing import Sequence
from px_pipeline.pipelines import Executable
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


@s('WCD_JWT_REGISTRY')
@dataclass
class Settings:
    TOKEN_EXPIRE_SERIALIZER: str = 'wcd_jwt.contrib.registry.serializers.TokenExpireSerializer'
    TOKEN_EXPIRE_ON_REFRESH: bool = False

    TOKEN_REGISTRATION_PIPELINE: Sequence[Executable] = field(default_factory=lambda: [
        'wcd_jwt.contrib.registry.services.pipeline.register_pairs',
        'wcd_jwt.contrib.registry.services.pipeline.connecting_user',
    ])
    TOKEN_REGISTRATION_ON_SIGNAL: bool = True
    TOKEN_REGISTRATION_ON_SIGNAL_PARALLEL: bool = False


settings = Settings()
