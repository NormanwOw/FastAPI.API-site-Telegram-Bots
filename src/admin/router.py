from fastapi import APIRouter, Depends

from src.auth.secure import Secure, admin
from src.config import VERSION


router = APIRouter(
    prefix=f'/api/{VERSION}',
    tags=['Admin']
)


@router.get('/users')
async def get_users(user_id: int, user: Secure = Depends(admin)):
    return {'user': user_id}


@router.get('/users/{user_id}')
async def get_user(user_id: int, user: Secure = Depends(admin)):
    return {'user': user_id}


@router.patch('/users/{user_id}')
async def update_user(user_id: int, user: Secure = Depends(admin)):
    return {'user': user_id}


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, user: Secure = Depends(admin)):
    return {'user': user_id}
