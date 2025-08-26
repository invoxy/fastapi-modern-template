class JWTError(Exception):
    class PayloadTypeError(Exception):
        pass

    class TokenExpiredError(Exception):
        pass

    class InvalidTokenError(Exception):
        pass


invalid_token = JWTError.InvalidTokenError("Неверный токен.")
token_expired = JWTError.TokenExpiredError("Токен истёк.")
payload_type = JWTError.PayloadTypeError("Неверный тип. Payload должен быть словарём.")
