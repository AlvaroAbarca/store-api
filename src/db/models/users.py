from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    """
    The User model
    first_name
    last_name
    mother_last_name
    email
    """

    id = fields.IntField(primary_key=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    mother_last_name = fields.CharField(max_length=50, null=True)

    email = fields.CharField(max_length=100, unique=True)

    password_hash = fields.CharField(max_length=128, null=True)

    class PydanticMeta:
        computed = []
        exclude = ["password_hash"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
