from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.auth.secure import Secure, get_current_user
from src.ordering.schemas import NewOrder, ResponseOrder
from src.config import VERSION
from src.ordering.orm import orders

router = APIRouter(
    prefix=f'/api/{VERSION}/orders',
    tags=['Orders']
)


@router.get('/')
async def get_orders(limit: int, offset: int):
    if limit < 1 or offset < 0:
        raise HTTPException(
            detail='incorrect values [limit > 0 and offset >= 0]',
            status_code=422
        )

    return JSONResponse('orders', status_code=200)


# @router.get('/{order_id}', status_code=404)
# async def get_order_by_id(order_id: int):
#     return JSONResponse({f'order_id: {order_id}'}, status_code=200)


@router.post('/', response_model=ResponseOrder, status_code=201)
async def new_order(order: NewOrder, user: Secure = Depends(get_current_user)):
    result_order = await orders.new_order(user, order)

    return result_order

