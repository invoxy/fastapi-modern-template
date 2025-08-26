class JWTError(Exception):
    class PayloadTypeError(Exception):
        pass

    class TokenExpiredError(Exception):
        pass

    class InvalidTokenError(Exception):
        pass


invalid_token = JWTError.InvalidTokenError("Invalid token.")
token_expired = JWTError.TokenExpiredError("Token has expired.")
payload_type = JWTError.PayloadTypeError("Invalid type. Payload must be a dict.")
