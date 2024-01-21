from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class NewOrder(BaseModel):
    phone_number: str = Field(pattern='^[+]7\(9[0-9]{2}\)[0-9]{7}')
    admin_panel: bool
    database: bool


class ResponseOrder(BaseModel):
    order_id: int
    phone_number: str
    email: EmailStr
    bot_shop: int
    admin_panel: int
    database: int
    total_price: int
    status: str
    date: datetime
