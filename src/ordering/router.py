from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response

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


@router.get('/{order_id}', response_model=ResponseOrder, status_code=200)
async def get_order(order_id: int, user: Secure = Depends(get_current_user)):
    result_order = await orders.get_order_by_id(order_id, user)

    return result_order


@router.post('/', response_model=ResponseOrder, status_code=201)
async def new_order(order: NewOrder, user: Secure = Depends(get_current_user)):
    result_order = await orders.new_order(user, order)

    return result_order


@router.delete('/{order_id}')
async def delete_order(order_id: int, user: Secure = Depends(get_current_user)):
    await orders.delete_order(order_id, user)

    return Response(status_code=204)
