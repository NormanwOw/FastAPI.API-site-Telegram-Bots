from typing import Optional
from pydantic import EmailStr, Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    phone_number: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    phone_number: str = Field(pattern='^[+]7\(9[0-9]{2}\)[0-9]{7}')
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
