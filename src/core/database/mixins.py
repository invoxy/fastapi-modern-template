from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    """
    A mixin class that automatically adds timestamp fields to Tortoise ORM models.

    This mixin provides automatic tracking of when a record was created and last modified.
    It's designed to be inherited by other model classes to add timestamp functionality.

    Attributes:
        created_at (DatetimeField): Automatically set to the current datetime when the record is created.
                                   Uses auto_now_add=True to set the value only on creation.
        edited_at (DatetimeField): Automatically updated to the current datetime whenever the record is modified.
                                  Uses auto_now=True to update the value on every save operation.

    Example:
        class User(TimestampMixin, Model):
            name = fields.CharField(max_length=255)
            email = fields.CharField(max_length=255)

            class Meta:
                table = "users"

    Note:
        This is an abstract model, so it won't create its own database table.
        It's intended to be used as a mixin for other models.
    """

    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
