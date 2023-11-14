from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.auth.models import User
from src.auth.auth_config import admin
from src.users.orm import UsersORM
from src.config import VERSION

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Admin']
)


@router.get('/')
async def get_users(limit: int, offset: int, user: User = Depends(admin)):
    result = await UsersORM.get_users(limit, offset)
    return JSONResponse(result, status_code=200)


@router.get('/{user_id}')
async def get_user(user_id: int, user: User = Depends(admin)):
    result = await UsersORM.get_user(user_id)
    return JSONResponse(result, status_code=200)


@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: int, user: User = Depends(admin)):
    await UsersORM.delete_user(user_id)
    return
