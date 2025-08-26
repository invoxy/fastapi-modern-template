from datetime import UTC, datetime, timedelta

import jwt

from .exceptions import invalid_token, payload_type, token_expired


class JWTManager:
    def __init__(self, algorithm: str, secret_key: str, expiration_minutes: int = 60):
        self.algorithm: str = algorithm
        self.secret_key: str = secret_key
        self.expiration_minutes: int = expiration_minutes

    def encode(self, payload: dict) -> str:
        """
        Creates a JWT token with the specified payload and expiration time.

        :param payload: Data to be encoded in the token.
        :return: JWT token string.
        """
        if not isinstance(payload, dict):
            raise payload_type

        payload["exp"] = datetime.now(UTC) + timedelta(minutes=self.expiration_minutes)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        """
        Decodes a JWT token and verifies its authenticity.

        :param token: JWT token to decode.
        :return: Decoded payload (dictionary).
        :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
        """
        try:
            if isinstance(token, str):
                token = token.encode("utf-8")
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise token_expired
        except jwt.InvalidTokenError:
            raise invalid_token
