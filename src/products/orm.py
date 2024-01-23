from sqlalchemy import select, update, delete

from src.session import async_session
from src.products.models import Product
from src.products.schemas import ProductResponse, ProductResult


class ProductORM:
    @staticmethod
    async def get_products() -> list:
        async with async_session() as session:
            resp = await session.execute(
                select(Product)
            )
            product_list = resp.scalars().all()

            return product_list

    @staticmethod
    async def new_product(product: ProductResponse) -> ProductResult:
        async with async_session() as session:
            product_model = Product(**product.model_dump())
            session.add(product_model)
            await session.flush()
            result_product = ProductResult(**product_model.as_dict())
            await session.commit()

            return result_product

    @staticmethod
    async def update_product(product: ProductResponse, product_name: str):
        async with async_session() as session:
            await session.execute(
                update(Product).values(**product.model_dump()).where(
                    Product.name == product_name
                )
            )
            await session.commit()

    @staticmethod
    async def delete_product(product_name: str):
        async with async_session() as session:
            await session.execute(
                delete(Product).where(Product.name == product_name)
            )
            await session.commit()


products = ProductORM()
