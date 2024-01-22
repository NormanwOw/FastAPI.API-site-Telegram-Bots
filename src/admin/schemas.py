from datetime import datetime
from typing import Union
from string import ascii_letters, digits

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


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
