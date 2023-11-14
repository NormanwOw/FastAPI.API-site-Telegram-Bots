from datetime import datetime
from random import randint

from sqlalchemy import insert, select

from src.database import async_session
from src.ordering.models import Order
from src.auth.models import User


class OrdersORM:

    @classmethod
    async def new_order(cls, user, order) -> dict:
        async with async_session() as session:

            order_id = randint(10 ** 6, 10 ** 7 - 1)
            data = {
                    'order_id': order_id,
                    'email': user.email,
                    'phone_number': order.phone_number,
                    'bot_shop': True,
                    'admin_panel': order.admin_panel,
                    'database': order.database,
                    'total_price': 1000
            }
            stmt = insert(Order).values(data)

            await session.execute(stmt)
            await session.commit()

            data['date'] = datetime.utcnow().strftime('%d.%m.%Y %H:%m')

            return data

    @classmethod
    async def get_orders(cls, limit: int, offset: int, user: User) -> list:
        async with async_session() as session:
            if user.is_superuser:
                query = select(Order).limit(limit).offset(offset)
            else:
                query = select(Order).where(Order.email == user.email).limit(limit).offset(offset)

            result = await session.execute(query)

            return result.scalars().all()

