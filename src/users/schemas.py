from datetime import datetime
from typing import Optional, Union
from string import ascii_letters, digits

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


class UserUpdate(BaseModel):
    email: Optional[Union[EmailStr, None]] = None
    first_name: Optional[Union[str, None]] = None
    last_name: Optional[Union[str, None]] = None

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, first_name: str) -> str:
        if first_name:
            if not 2 <= len(first_name) <= 20:
                raise PydanticCustomError(
                    'first_name_len_error',
                    'Incorrect first-name, should be [2:20] chars'
                )
            for char in first_name:
                if char not in ascii_letters:
                    raise PydanticCustomError(
                        'first_name_chars_error',
                        'Incorrect first-name, should be chars only'
                    )
        return first_name

    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, last_name: str) -> str:
        if last_name:
            if not 2 <= len(last_name) <= 20:
                raise PydanticCustomError(
                    'last_name_len_error',
                    'Incorrect last-name, should be [2:20] chars'
                )
            for char in last_name:
                if char not in ascii_letters:
                    raise PydanticCustomError(
                        'last_name_chars_error',
                        'Incorrect last-name, should be chars only'
                    )
        return last_name


class AdmUserUpdate(BaseModel):
    username: str
    email: EmailStr
    first_name: Union[str, None]
    last_name: Union[str, None]
    is_superuser: bool
    is_staff: bool
    is_active: bool

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


class AdmUserResponse(AdmUserUpdate):
    id: int
    last_login: Union[datetime, None]
    date_joined: datetime
