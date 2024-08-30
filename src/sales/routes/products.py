from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.core.auth import current_user
from src.core.pagination import Page, ProductParams, paginate
from src.sales.models.products import Product, Product_Pydantic, ProductIn_Pydantic

router = APIRouter(prefix="/products", tags=["sales", "products"], dependencies=[Depends(current_user)])

class Status(BaseModel):
    message: str
#  dependencies=[Depends(current_user)]
@router.get("/", response_model=Page[Product_Pydantic])
async def product_list(params: ProductParams = Depends()):
    is_billable = params.all
    if is_billable is None:
        queryset = Product.all()
    else:
        queryset = Product.filter(is_billable=is_billable)
    return await paginate(queryset, params)

@router.post("/", response_model=Product_Pydantic)
async def product_create(product: ProductIn_Pydantic, user=Depends(current_user)): # type: ignore
    product_obj = await Product.create(**product.model_dump(exclude_unset=True), user=user)
    return await Product_Pydantic.from_tortoise_orm(product_obj)

@router.put("/{product_id}", response_model=Product_Pydantic)
async def update_user(product_id: int, product: ProductIn_Pydantic): # type: ignore
    await Product.filter(id=product_id).update(**product.model_dump(exclude_unset=True))
    return await Product_Pydantic.from_queryset_single(Product.get(id=product_id))

@router.delete("/{product_id}", response_model=Status)
async def delete_user(product_id: int):
    deleted_count = await Product.filter(id=product_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {product_id} not found")
    return Status(message=f"Deleted user {product_id}")
