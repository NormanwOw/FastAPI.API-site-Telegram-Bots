from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.ordering.schemas import NewOrder
from src.auth.models import User
from src.auth.auth_config import current_user
from src.ordering.orm import OrdersORM
from src.config import VERSION

router = APIRouter(
    prefix=f'/api/{VERSION}/orders',
    tags=['Orders']
)


@router.get('/')
async def get_orders(limit: int, offset: int, user: User = Depends(current_user)):
    if limit < 1 or offset < 0:
        return JSONResponse(
            {'error': 'incorrect values [limit > 0 and offset >= 0]'}, status_code=422
        )
    response = await OrdersORM.get_orders(limit, offset, user)

    return JSONResponse(jsonable_encoder(response), status_code=200)


@router.get('/{order_id}', status_code=404)
async def get_order_by_id(order_id: int, user: User = Depends(current_user)):
    response = await OrdersORM.get_order_by_id(order_id, user)
    if response:
        return JSONResponse(response, status_code=200)


@router.post('/')
async def new_order(order: NewOrder, user: User = Depends(current_user)):
    response = await OrdersORM.new_order(user, order)

    return JSONResponse(response, status_code=201)

