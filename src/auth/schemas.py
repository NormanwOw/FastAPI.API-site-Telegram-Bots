from datetime import datetime
from typing import Union
from string import ascii_letters, digits

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


class UserRead(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, username: str) -> str:
        if not 3 <= len(username) <= 16:
            raise PydanticCustomError(
                'username_len_error',
                'Incorrect username, should be [3:16] chars'
            )
        for char in username:
            if char not in ascii_letters + digits:
                raise PydanticCustomError(
                    'username_chars_error',
                    'Incorrect username, should be chars and digits only'
                )
        return username

    @field_validator('confirm_password')
    @classmethod
    def validate_password(cls, confirm_password: str, meta) -> str:
        password = meta.data['password']
        if not 8 <= len(password) <= 32:
            raise PydanticCustomError(
                'password_len_error',
                'Incorrect password, should be [8:32] chars'
            )
        if confirm_password != password:
            raise PydanticCustomError(
                'confirm_password_error',
                'Passwords do not match'
            )
        return confirm_password


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

    @field_validator('new_password')
    @classmethod
    def passwords_match(cls, new_password: str, meta) -> str:
        current_password = meta.data['current_password']
        if 'current_password' in meta.data:
            if not 8 <= len(new_password) <= 32:
                raise PydanticCustomError(
                    'password_error',
                    'Incorrect new password, should be [8:32] chars'
                )
            if new_password == current_password:
                raise PydanticCustomError(
                    'new_password_error',
                    'New password match the Current password'
                )
        return new_password

