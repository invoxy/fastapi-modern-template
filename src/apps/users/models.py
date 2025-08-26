from tortoise import fields

from core.database import TimestampMixin


class User(TimestampMixin):
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
