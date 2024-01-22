from pydantic import BaseModel


class ProductResponse(BaseModel):
    name: str
    price: int
    title: str
    description: str


class Product(ProductResponse):
    id: int

