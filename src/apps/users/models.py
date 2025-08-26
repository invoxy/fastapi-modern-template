from tortoise import fields, models

from core.database import TimestampMixin


class User(TimestampMixin, models.Model):
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
