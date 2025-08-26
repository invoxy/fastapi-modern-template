class JWTException(Exception):
    class PayloadTypeError(Exception):
        pass

    class TokenExpiredError(Exception):
        pass

    class InvalidTokenError(Exception):
        pass


invalid_token = JWTException.InvalidTokenError("Неверный токен.")
token_expired = JWTException.TokenExpiredError("Токен истёк.")
payload_type = JWTException.PayloadTypeError(
    "Неверный тип. Payload должен быть словарём."
)
