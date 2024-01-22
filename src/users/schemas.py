from typing import Optional
from string import ascii_letters

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, first_name: str) -> str:
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
