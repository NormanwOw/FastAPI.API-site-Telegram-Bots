from pydantic import BaseModel


class ProductResponse(BaseModel):
    name: str
    price: int
    title: str
    description: str


class ProductResult(ProductResponse):
    id: int
