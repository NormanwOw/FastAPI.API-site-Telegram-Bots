from typing import List

from fastapi import APIRouter, Depends

from src.auth.secure import get_current_user, admin
from src.products.schemas import ProductResponse, ProductResult
from src.products.orm import products
from src.config import VERSION
from src import utils


router = APIRouter(
    prefix=f'/api/{VERSION}/products',
    tags=['Products']
)


@router.get('/', dependencies=[Depends(get_current_user)], status_code=200,
            response_model=List[ProductResponse])
async def get_products():
    product_list = await products.get_products()
    return product_list


@router.post('/', dependencies=[Depends(admin)], status_code=201,
             response_model=ProductResult)
async def new_product(product: ProductResponse):
    product_result = await products.new_product(product)
    return product_result


@router.patch('/{product_name}', dependencies=[Depends(admin)], status_code=200)
async def update_product(product_name: str, product: ProductResponse):
    await products.update_product(product, product_name)
    return utils.SUCCESS


@router.delete('/{product_name}', dependencies=[Depends(admin)], status_code=204)
async def delete_product(product_name: str):
    await products.delete_product(product_name)
    return
