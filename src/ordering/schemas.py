from pydantic import BaseModel, Field


class NewOrder(BaseModel):
    phone_number: str = Field(pattern='^[+]7\(9[0-9]{2}\)[0-9]{7}')
    admin_panel: bool
    database: bool
