from rest_framework_simplejwt.authentication import JWTAuthentication as Base

from .services import token_manager


class JWTAuthentication(Base):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        token_manager.check_expired(token, silent=False)

        return token
