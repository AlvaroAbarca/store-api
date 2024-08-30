from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, field_validator

from src.sales.models import Order_Pydantic, OrderIn_Pydantic, Product


class BaseOrder(BaseModel):
    short_name: str | None = None
    full_name: str | None = None


class OrderRead(BaseOrder):
    pass

class ProductOrder(BaseModel):
    product_id: int
    quantity: int

    @field_validator('product_id', mode='before')
    @classmethod
    def product_exists(cls, v: int) -> int:
        if Product.filter(id=v).exists():
            return v
        raise ValueError('Product does not exist')

class OrderCreate(OrderIn_Pydantic):
    """
    products = [
        { product_id: 1, quantity: 2 },
        { product_id: 2, quantity: 1 },
    ]
    """
    products: list[ProductOrder]


class OrderUpdate(BaseOrder):
    pass


class ProductRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
