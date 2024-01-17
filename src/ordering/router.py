from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.ordering.schemas import NewOrder
from src.config import VERSION

router = APIRouter(
    prefix=f'/api/{VERSION}/orders',
    tags=['Orders']
)


@router.get('/')
async def get_orders(limit: int, offset: int):
    if limit < 1 or offset < 0:
        return JSONResponse(
            {'error': 'incorrect values [limit > 0 and offset >= 0]'}, status_code=422
        )

    return JSONResponse('orders', status_code=200)


@router.get('/{order_id}', status_code=404)
async def get_order_by_id(order_id: int):
    return JSONResponse({f'order_id: {order_id}'}, status_code=200)


@router.post('/')
async def new_order(order: NewOrder):
    return JSONResponse(order, status_code=201)

