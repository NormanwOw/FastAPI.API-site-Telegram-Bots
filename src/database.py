from sqlalchemy import select

from src.session import async_session
from src.ordering.models import Order


orders = set()


class Database:

    @classmethod
    async def get_all_order_id(cls) -> list:
        async with async_session() as session:
            stmt = select(Order.order_id)
            resp = await session.execute(stmt)
            result = resp.scalars().all()

            return result
