from datetime import datetime
from random import randint

from sqlalchemy import insert, select
from fastapi.encoders import jsonable_encoder

from src.session import async_session
from src.ordering.models import Order, Product
from src.ordering.schemas import NewOrder
from src.auth.models import User
from src.database import orders
from src.tasks.tasks import send_email


class OrdersORM:

    @classmethod
    async def new_order(cls, user: User, new_order: NewOrder) -> dict:
        async with async_session() as session:
            min_id = 10 ** 6
            max_id = 10 ** 7 - 1
            total_price = 0

            order_id = randint(min_id, max_id)
            orders_len = len(orders)
            orders.add(order_id)

            while len(orders) == orders_len:
                order_id += 1
                orders.add(order_id)
                if order_id == max_id - 1:
                    order_id = min_id

            query = select(Product.product, Product.price)
            resp = await session.execute(query)

            products = resp.all()
            order_dict = new_order.model_dump()
            order_dict['bot_shop'] = Order.bot_shop

            for product, price in products:
                if order_dict[product]:
                    total_price += price
                else:
                    price = 0

                order_dict[product] = price

            data = {
                    'order_id': order_id,
                    'email': user.email,
                    'phone_number': new_order.phone_number,
                    'bot_shop': order_dict['bot_shop'],
                    'admin_panel': order_dict['admin_panel'],
                    'database': order_dict['database'],
                    'total_price': total_price
            }

            stmt = insert(Order).values(data)

            data['date'] = datetime.utcnow().strftime('%d.%m.%Y %H:%m')
            send_email.delay(data)

            await session.execute(stmt)
            await session.commit()

            return data

    @classmethod
    async def get_orders(cls, limit: int, offset: int, user: User) -> list:
        async with async_session() as session:
            if user.is_superuser:
                query = select(Order).limit(limit).offset(offset)
            else:
                query = select(Order).where(Order.email == user.email).limit(limit).offset(offset)

            resp = await session.execute(query)

            return resp.scalars().all()

    @classmethod
    async def get_order_by_id(cls, order_id: int, user: User) -> list:
        async with async_session() as session:
            if user.is_superuser:
                query = select(Order).where(Order.order_id == order_id)
            else:
                query = select(Order).where(Order.order_id == order_id, Order.email == user.email)

            resp = await session.execute(query)
            result = jsonable_encoder(resp.scalar())

            return result
