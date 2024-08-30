from decimal import Decimal

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from src.db.models import TimeStampedModel
from src.users.models import User


class Product(TimeStampedModel):
    """
    The Product model
        - name
        - description
        - is_billable
        - price
        - image
        - code
        - barcode
    """

    id = fields.IntField(primary_key=True)
    #: This is a username
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_billable = fields.BooleanField(default=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    image = fields.TextField(null=True)
    code = fields.CharField(max_length=50, null=True)
    barcode = fields.CharField(max_length=50, null=True)

    orders: fields.ManyToManyRelation

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="products")

    class PydanticMeta:
        computed = []
        exclude = ['created_at', 'updated_at']

    class Meta:
        table = "products"

Product_Pydantic = pydantic_model_creator(Product, name="Product")
ProductIn_Pydantic = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)
