from typing import List

from fastapi import APIRouter, Depends

from src.auth.secure import get_current_user, admin
from src.products.schemas import ProductResponse, Product
from src.config import VERSION
from src import utils


router = APIRouter(
    prefix=f'/api/{VERSION}/products',
    tags=['Products']
)


@router.get('/', dependencies=[Depends(get_current_user)], status_code=200,
            response_model=List[ProductResponse])
async def get_products():
    pass


@router.post('/', dependencies=[Depends(admin)], response_model=Product, status_code=201)
async def new_product():
    pass


@router.patch('/{product_name}', dependencies=[Depends(admin)], status_code=200)
async def update_product():
    return utils.SUCCESS


@router.delete('/{product_name}', dependencies=[Depends(admin)], status_code=204)
async def delete_product():
    return utils.SUCCESS
