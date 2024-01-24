from pydantic import BaseModel


class ProductResponse(BaseModel):
    title: str
    description: str
    price: int


class ProductResult(ProductResponse):
    id: int
    name: str
