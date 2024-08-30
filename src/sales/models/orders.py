from enum import Enum
from uuid import uuid4

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from src.db.models import TimeStampedModel
from src.users.models import User

from .products import Product


class StatusEnum(str, Enum):
    CANCELED = "CANCELED"
    PENDING = "PENDING"
    STARTED = "STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FINISHED = "FINISHED"
    ALL_DISCOUNT = "ALL_DISCOUNT"

class PaymentTypeEnum(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    CASH = "CASH"
    OTHER = "OTHER"
    NONE = "NONE"

class Order(TimeStampedModel):
    """
    The Order model
    - uuid
    - status
    - payment_type
    - voucher
    - subtotal
    - discount
    - total
    - extra_data
    - profile
    - products
    """

    id = fields.IntField(primary_key=True)
    #: This is a username
    uuid = fields.UUIDField(default=uuid4)
    status = fields.CharEnumField(enum_type=StatusEnum, max_length=20)
    payment_type = fields.CharEnumField(enum_type=PaymentTypeEnum, max_length=10)
    voucher = fields.CharField(max_length=50)
    subtotal = fields.DecimalField(max_digits=10, decimal_places=2)
    discount = fields.DecimalField(max_digits=10, decimal_places=2)
    total = fields.DecimalField(max_digits=10, decimal_places=2)
    extra_data = fields.JSONField(null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="orders")
    products: fields.ManyToManyRelation[Product] = fields.ManyToManyField(
        "models.Product",
        through="orderproducts",
        forward_key="order_id",
        backward_key="product_id",
        related_name="orders",
    )

    class PydanticMeta:
        computed = []
        exclude = ['uuid','extra_data', 'created_at', 'updated_at']

    class Meta:
        ordering = ["-created_at"]
        table = "orders"


Order_Pydantic = pydantic_model_creator(Order, name="Order")
OrderIn_Pydantic = pydantic_model_creator(Order, name="OrderIn", exclude_readonly=True)

class OrderProducts(models.Model):
    quantity = fields.SmallIntField(default=0)

    # Relationships
    order = fields.ForeignKeyField(
        "models.Order",
        on_delete=fields.RESTRICT,
        related_name="order_products"
    )
    product = fields.ForeignKeyField(
        "models.Product",
        on_delete=fields.RESTRICT,
        related_name="order_products"
    )

OrderProducts_Pydantic = pydantic_model_creator(OrderProducts, name="OrderProducts")
OrderProductsIn_Pydantic = pydantic_model_creator(OrderProducts, name="OrderProductsIn", exclude_readonly=True)
