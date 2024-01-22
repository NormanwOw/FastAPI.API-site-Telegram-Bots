from typing import List
from fastapi import APIRouter, Depends

from src.auth.secure import admin, auth, Secure
from src.admin.schemas import AdmUserResponse, AdmUserUpdate
from src.admin.orm import adm
from src.config import VERSION
from src.users.orm import users
from src import utils


router = APIRouter(
    prefix=f'/api/{VERSION}',
    tags=['Admin']
)


@router.get(
    path='/users/',
    dependencies=[Depends(admin)],
    response_model=List[AdmUserResponse],
    status_code=200
)
async def get_users(limit: int, offset: int):
    user_list = await adm.get_users(limit, offset)
    return user_list


@router.get(
    path='/users/{user_id}',
    dependencies=[Depends(admin)],
    response_model=AdmUserResponse,
    status_code=200
)
async def get_user(user_id: int):
    user = await auth.get_user(user_id)
    return user


@router.patch('/users/{user_id}', status_code=200)
async def update_user(user_id: int, data: AdmUserUpdate, user: Secure = Depends(admin)):
    await users.update_user(user, user_id, schema=data)
    return utils.SUCCESS


@router.delete('/users/{user_id}', status_code=204)
async def delete_user(user_id: int, user: Secure = Depends(admin)):
    await users.delete_user(user, user_id)
    return utils.SUCCESS
