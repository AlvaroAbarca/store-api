from fastapi import APIRouter

from src.sales.routes.orders import router as order_router
from src.sales.routes.products import router as product_router

router = APIRouter(prefix="/sales", tags=["sales"])
router.include_router(order_router)
router.include_router(product_router)
