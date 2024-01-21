from typing import List
from fastapi import APIRouter, Depends

from src.auth.secure import admin
from src.admin.schemas import AdmUserResponse
from src.config import VERSION
from src.admin.orm import adm

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


@router.get('/users/{user_id}', dependencies=[Depends(admin)], status_code=200)
async def get_user(user_id: int):
    return {'user': user_id}


@router.patch('/users/{user_id}', dependencies=[Depends(admin)], status_code=200)
async def update_user(user_id: int):
    return {'user': user_id}


@router.delete('/users/{user_id}', dependencies=[Depends(admin)], status_code=200)
async def delete_user(user_id: int):
    return {'user': user_id}
