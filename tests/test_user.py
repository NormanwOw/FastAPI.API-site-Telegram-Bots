import pytest
from httpx import AsyncClient
from sqlalchemy import update, select

from src.config import SITE_NAME
from src.ordering.models import Order
from tests.conftest import engine_test


class TestUser:

    @staticmethod
    @pytest.mark.parametrize(
        'username, email, pw1, pw2, msg, code', [
            ('example', 'example@gmail.com', 'stringstring', 'stringstring', None, 201),
            ('example', 'examplegmail.com', 'stringstring', 'stringstring', 'email', 422),
            ('example', 'example@gmail.com', 'stringstring', 'string', 'Passwords', 422),
            ('ex', 'example@gmail.com', 'stringstring', 'stringstring', 'username', 422),
            ('example@', 'example@gmail.com', 'stringstring', 'stringstring', 'username',
             422),
            ('example', 'example@gmail.com', 'st', 'st', 'password', 422),
        ]
    )
    async def test_registration(ac: AsyncClient, username, email, pw1, pw2, msg, code):
        response = await ac.post('api/v1/auth/registration', json={
            'username': username,
            'email': email,
            'password': pw1,
            'confirm_password': pw2
        })

        assert response.status_code == code
        detail = response.json().get('detail')
        if detail:
            assert msg in detail.get('msg')

    @staticmethod
    @pytest.mark.parametrize(
        'username, pw, msg, code', [
            ('example', 'stringstring', 'success', 200),
            ('examplee', 'stringstring', 'Username', 404),
            ('example', 'asdasdasd', 'Password', 422),
        ]
    )
    async def test_login(ac: AsyncClient, username, pw, msg, code):
        response = await ac.post(url='api/v1/auth/login', json={
            'username': username,
            'password': pw
        })

        assert response.status_code == code
        detail = response.json().get('detail')
        if detail:
            if isinstance(detail, dict):
                assert msg in detail.get('msg')
            elif isinstance(detail, str):
                assert msg in detail

            if response.status_code == 200:
                assert response.cookies[SITE_NAME] != 0

    @staticmethod
    async def test_logout(ac: AsyncClient):
        response = await ac.post(url='api/v1/auth/logout')

        assert response.status_code == 200
        assert 'success' in response.json().get('detail')
        assert response.cookies.get(SITE_NAME) is None

    @staticmethod
    async def test_get_products(authorized_client: AsyncClient):
        response = await authorized_client.get(url='api/v1/products/')

        assert response.status_code == 200

    @staticmethod
    async def test_new_product(authorized_client: AsyncClient):
        response = await authorized_client.post(url='api/v1/products/')

        assert response.status_code == 403

    @staticmethod
    async def test_update_product(authorized_client: AsyncClient):
        response = await authorized_client.patch(url='api/v1/products/product-name')

        assert response.status_code == 403

    @staticmethod
    async def test_delete_product(authorized_client: AsyncClient):
        response = await authorized_client.delete(url='api/v1/products/product-name')

        assert response.status_code == 403

    @staticmethod
    @pytest.mark.parametrize(
        'phone, ap, db, code, result', [
            ('+79999999999', True, True, 201, 'Оформлен'),
            ('+7999999999', True, True, 422, None),
            ('+79999999999', None, None, 422, None),
        ]
    )
    async def test_new_order(authorized_client: AsyncClient, phone, ap, db, code, result):
        response = await authorized_client.post(url='api/v1/orders/', json={
            'phone_number': phone,
            'admin_panel': ap,
            'database': db
        })

        assert response.status_code == code
        assert response.json().get('status') == result

        # MOCK ORDER NUMBER
        async with engine_test.begin() as conn:
            await conn.execute(
                update(Order).values(order_id=1111111)
            )

    @staticmethod
    @pytest.mark.parametrize(
        'limit, offset, code, result', [
            (1, 0, 200, 1111111),
            (0, 0, 422, None),
        ]
    )
    async def test_get_orders(authorized_client: AsyncClient, limit, offset, code, result):
        response = await authorized_client.get(
            url=f'api/v1/orders/?limit={limit}&offset={offset}'
        )

        assert response.status_code == code
        if isinstance(response.json(), list):
            assert response.json()[0].get('order_id') == result

    @staticmethod
    @pytest.mark.parametrize(
        'order_id, code', [
            (1111111, 200),
            (111111, 404),
        ]
    )
    async def test_get_order(authorized_client: AsyncClient, order_id, code):
        response = await authorized_client.get(url=f'api/v1/orders/{order_id}')

        assert response.status_code == code

    @staticmethod
    @pytest.mark.parametrize(
        'order_id, code, quan', [
            (1111111, 204, 0),
            (111111, 204, 0),
        ]
    )
    async def test_delete_order(authorized_client: AsyncClient, order_id, code, quan):
        response = await authorized_client.delete(url=f'api/v1/orders/{order_id}')

        assert response.status_code == code
        async with engine_test.begin() as conn:
            result = await conn.execute(
                select(Order).where(Order.order_id == order_id)
            )
            assert len(result.scalars().all()) == quan
