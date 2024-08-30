from decimal import Decimal

from fastapi import APIRouter, Depends

from src.core.auth import current_user
from src.core.pagination import Page, Params, paginate
from src.sales.models.orders import Order, Order_Pydantic, OrderProducts
from src.sales.models.products import Product
from src.sales.schemas import OrderCreate

router = APIRouter(prefix="/orders", tags=["sales", "orders"], dependencies=[Depends(current_user)])

@router.get("/", response_model=Page[Order_Pydantic])
async def order_list(params: Params = Depends()):
    return await paginate(Order.all(), params)

@router.post("/", response_model=Order_Pydantic)
async def order_create(body: OrderCreate, user = Depends(current_user)):
    products = body.products
    data = body.model_dump(exclude={"products"})
    order = await Order.create(**data, user=user)
    total = Decimal(0)
    for product in products:
        product_obj = await Product.get(id=product.product_id)
        total += product_obj.price * product.quantity
        await OrderProducts.create(
            order=order,
            product=product_obj,
            quantity=product.quantity
        )
    order.subtotal = total
    order.total = total
    order.status = "CREATED"
    await order.save()

    return order
