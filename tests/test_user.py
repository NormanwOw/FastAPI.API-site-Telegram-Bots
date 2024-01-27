import pytest
from httpx import AsyncClient
from sqlalchemy import update, select, or_

from src.config import SITE_NAME
from src.ordering.models import Order
from src.auth.models import User
from tests.conftest import engine_test


class TestUserAuth:

    @staticmethod
    async def test_logout(authorized_client: AsyncClient):
        response = await authorized_client.post(url='api/v1/auth/logout')

        assert response.status_code == 200
        assert 'success' in response.json().get('detail')
        assert authorized_client.cookies.get(SITE_NAME) is None

        await authorized_client.post('api/v1/auth/login', json={
            'username': 'username',
            'password': 'stringstring'
        })

    @staticmethod
    @pytest.mark.parametrize(
        'pw, new_pw, code', [
            ('stringstring', 'stringstring1', 200),
            ('stringstring1', 'stringstring1', 422),
            ('stringstring1', 'str', 422),
            ('stringstring1', 'stringstring', 200),
        ]
    )
    async def test_change_password(authorized_client: AsyncClient, pw, new_pw, code):
        response = await authorized_client.post(url='api/v1/auth/change-password', json={
            'current_password': pw,
            'new_password': new_pw
        })

        assert response.status_code == code

        if pw != new_pw:
            response = await authorized_client.post('api/v1/auth/login', json={
                'username': 'username',
                'password': new_pw
            })
            assert response.status_code == code


class TestUserUsers:
    @staticmethod
    async def test_get_me(authorized_client: AsyncClient):
        response = await authorized_client.get(url='api/v1/users/me')

        assert response.status_code == 200
        assert authorized_client.cookies.get(SITE_NAME) is not None
        user = response.json()
        assert user.get('username') == 'username'
        assert user.get('username') != 'user'
        assert user.get('email') == 'user@example.com'
        assert user.get('password') is None

    @staticmethod
    async def test_get_user(authorized_client: AsyncClient):
        response = await authorized_client.get(url='api/v1/users/1')
        assert response.status_code == 403

    @staticmethod
    async def test_get_users(authorized_client: AsyncClient):
        response = await authorized_client.get(url='api/v1/users/')
        assert response.status_code == 403

    @staticmethod
    async def test_update_user(authorized_client: AsyncClient):
        response = await authorized_client.patch(url='api/v1/users/1')
        assert response.status_code == 403

    @staticmethod
    @pytest.mark.parametrize(
        'email, f_name, l_name, code', [
            ('user@example.com', 'example', 'example', 200),
            ('example@gmail.com', 'example', 'example', 422),
            (None, 'example', 'example', 200),
            ('userexample.com', 'example', 'example', 422),
            ('user@examplecom', 'example', 'example', 422),
            ('user@example.com', 'example', 'e', 422),
            ('user@example.com', 'e', 'example', 422),
            ('user@example.com', 'example123', 'example', 422),
            ('user@example.com', 'example', 'example123', 422),
        ]
    )
    async def test_update_me(authorized_client: AsyncClient, email, f_name, l_name, code):
        response = await authorized_client.patch(url='api/v1/users/', json={
            'email': email,
            'first_name': f_name,
            'last_name': l_name,
        })
        assert response.status_code == code
        if response.status_code == 200:
            async with engine_test.begin() as conn:
                res = await conn.execute(
                    select(User).where(
                        or_(
                            User.first_name == f_name, User.last_name == l_name,
                            User.email == email
                        )
                    )
                )
                user = res.first()
                if f_name:
                    assert f_name in user
                if l_name:
                    assert l_name in user
                if email:
                    assert email in user

    @staticmethod
    async def test_delete_me(authorized_client: AsyncClient):
        response = await authorized_client.delete(url='api/v1/users/')
        assert response.status_code == 204
        assert authorized_client.cookies.get(SITE_NAME) is None

        await authorized_client.post('api/v1/auth/registration', json={
            'username': 'username',
            'email': 'user@example.com',
            'password': 'stringstring',
            'confirm_password': 'stringstring'
        })

        await authorized_client.post('api/v1/auth/login', json={
            'username': 'username',
            'password': 'stringstring'
        })

    @staticmethod
    async def test_delete_user(authorized_client: AsyncClient):
        response = await authorized_client.delete(url='api/v1/users/1')
        assert response.status_code == 403


class TestUserOrders:

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
    async def test_get_orders(authorized_client: AsyncClient, limit, offset, code,
                              result):
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


class TestUserProducts:

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
