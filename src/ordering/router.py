from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.ordering.schemas import NewOrder
from src.auth.models import User
from src.auth.auth_config import current_user
from src.ordering.orm import OrderORM

router = APIRouter(
    prefix='/orders',
    tags=['Order']
)


@router.get('/')
async def get_orders(limit: int, offset: int, user: User = Depends(current_user)):
    response = await OrderORM.get_orders(limit, offset, user)

    return JSONResponse(jsonable_encoder(response), status_code=200)


@router.post('/')
async def new_order(order: NewOrder, user: User = Depends(current_user)):
    response = await OrderORM.new_order(user, order)

    return JSONResponse(response, status_code=201)

