from pydantic import BaseModel


class ProductResponse(BaseModel):
    name: str
    title: str
    description: str
    price: int


class ProductResult(ProductResponse):
    id: int
