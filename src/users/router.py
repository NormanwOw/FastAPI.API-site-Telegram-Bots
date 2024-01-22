from fastapi import APIRouter, Depends, Response
from typing import List

from src.auth.secure import get_current_user, Secure, admin, auth
from src.config import VERSION, SITE_NAME
from src.auth.schemas import UserResponse
from src.users.schemas import UserUpdate, AdmUserResponse, AdmUserUpdate
from src.users.orm import users
from src import utils

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Users']
)


@router.get('/me', response_model=UserResponse)
async def me(user: Secure = Depends(get_current_user)):
    return user


@router.patch('/')
async def update_me(data: UserUpdate, user: Secure = Depends(get_current_user)):
    await users.update_user(user, schema=data)
    return utils.SUCCESS


@router.delete('/', status_code=204)
async def delete_me(response: Response, user: Secure = Depends(get_current_user)):
    await users.delete_user(user)
    response.delete_cookie(SITE_NAME)
    return utils.SUCCESS


@router.get(
    path='/',
    dependencies=[Depends(admin)],
    response_model=List[AdmUserResponse],
    status_code=200
)
async def get_users(limit: int, offset: int):
    user_list = await users.get_users(limit, offset)
    return user_list


@router.get(
    path='/{user_id}',
    dependencies=[Depends(admin)],
    response_model=AdmUserResponse,
    status_code=200
)
async def get_user(user_id: int):
    user = await auth.get_user(user_id)
    return user


@router.patch('/{user_id}', status_code=200)
async def update_user(user_id: int, data: AdmUserUpdate, user: Secure = Depends(admin)):
    await users.update_user(user, user_id, schema=data)
    return utils.SUCCESS


@router.delete('/users/{user_id}', status_code=204)
async def delete_user(user_id: int, user: Secure = Depends(admin)):
    await users.delete_user(user, user_id)
    return utils.SUCCESS
