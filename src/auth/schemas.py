from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    date_joined: datetime


class UserChangePass(BaseModel):
    current_password: str
    new_password: str

