from typing import Optional

from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None