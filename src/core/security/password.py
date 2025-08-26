import bcrypt
from settings import environment


class Password:
    """Password hashing and verification with application pepper.

    Pepper is taken from settings.secret_key and concatenated to the password
    before hashing/verifying. Verification keeps backward compatibility by
    attempting both peppered and legacy (non-peppered) checks.
    """

    @staticmethod
    def hash_password(password: str, secret_key: str) -> str:
        password_bytes = f"{password}{secret_key}".encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def is_valid(password: str, hashed_password: str, secret_key: str) -> bool:
        # First try peppered verification
        password_bytes = f"{password}{secret_key}".encode()
        hashed_password_bytes = hashed_password.encode("utf-8")
        if bcrypt.checkpw(password_bytes, hashed_password_bytes):
            return True

        # Backward compatibility: try legacy non-peppered check
        legacy_password_bytes = password.encode()
        return bcrypt.checkpw(legacy_password_bytes, hashed_password_bytes)
