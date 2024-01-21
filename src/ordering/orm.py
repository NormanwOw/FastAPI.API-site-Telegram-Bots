from datetime import datetime
from random import randint

from sqlalchemy import insert, select, delete
from fastapi.exceptions import HTTPException

from src.session import async_session
from src.ordering.models import Order, Product
from src.ordering.schemas import NewOrder, ResponseOrder
from src.auth.models import User
from src.database import Database
from src.tasks.tasks import send_email


class OrdersORM:

    def __init__(self):
        self.db = Database()

    async def new_order(self, user: User, new_order: NewOrder) -> dict:
        async with async_session() as session:
            min_id = 10 ** 6
            max_id = 10 ** 7 - 1
            total_price = 0

            order_id = randint(min_id, max_id)
            orders_list = await self.db.get_all_order_id()

            while order_id in orders_list:
                order_id += 1

                if order_id == max_id - 1:
                    order_id = min_id

            query = select(Product.name, Product.price)
            resp = await session.execute(query)

            products = resp.all()
            order_dict = new_order.model_dump()
            order_dict['bot_shop'] = True

            for product, price in products:
                if order_dict[product]:
                    total_price += price
                    order_dict[product] = price

            result_order = {
                    'order_id': order_id,
                    'user_id': user.id,
                    'phone_number': new_order.phone_number,
                    'bot_shop': order_dict['bot_shop'],
                    'admin_panel': order_dict['admin_panel'],
                    'database': order_dict['database'],
                    'total_price': total_price
            }

            stmt = insert(Order).values(result_order)
            await session.execute(stmt)
            await session.commit()

            result_order['date'] = datetime.utcnow()
            result_order['email'] = user.email
            # send_email.delay(data)

            return result_order

    @classmethod
    async def get_orders(cls, limit: int, offset: int, user: User) -> list:
        async with async_session() as session:
            if user.is_superuser:
                query = select(Order).limit(limit).offset(offset)
            else:
                query = select(Order).where(Order.email == user.email).limit(limit).offset(offset)

            resp = await session.execute(query)

            return resp.scalars().all()

    @staticmethod
    async def get_order_by_id(order_id: int, user: User) -> ResponseOrder:
        async with async_session() as session:
            if user.is_superuser:
                order = await session.scalar(
                    select(Order).where(Order.order_id == order_id)
                )
            else:
                order = await session.scalar(
                    select(Order).where(
                        Order.order_id == order_id, Order.user_id == user.id
                    )
                )
            if not order:
                raise HTTPException(status_code=404)

            result_order = ResponseOrder(**order.as_dict(), email=user.email)

            return result_order

    @staticmethod
    async def delete_order(order_id: int, user: User):
        async with async_session() as session:
            if user.is_superuser:
                await session.execute(
                    delete(Order).where(Order.order_id == order_id)
                )
            else:
                await session.execute(
                    delete(Order).where(
                        Order.order_id == order_id, Order.user_id == user.id
                    )
                )
            await session.commit()


orders = OrdersORM()
