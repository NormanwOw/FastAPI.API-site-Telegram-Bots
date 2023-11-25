import pytest
from httpx import AsyncClient
from config import USER


class TestClient:

    @staticmethod
    async def test_register(ac: AsyncClient):
        response = await ac.post('api/v1/auth/register', json={
          'email': USER,
          'password': 'string',
          'is_active': True,
          'is_superuser': False,
          'is_verified': False,
          'phone_number': '+7(952)0810297'
        })

        assert response.status_code == 201

    @staticmethod
    async def test_login(ac: AsyncClient):
        response = await ac.post(url='api/v1/auth/login', data={
            'username': USER,
            'password': 'string'
        })

        assert response.status_code == 204

    @staticmethod
    async def test_me(ac: AsyncClient):
        response = await ac.get(url='api/v1/users/me')

        assert response.status_code == 200

    @staticmethod
    async def test_get_users(ac: AsyncClient):
        response = await ac.get(url='api/v1/users/?limit=1&offset=0')

        assert response.status_code == 403

    @staticmethod
    async def test_get_user_by_id(ac: AsyncClient):
        response = await ac.get(url='api/v1/users/1')

        assert response.status_code == 403

    @staticmethod
    async def test_delete_user(ac: AsyncClient):
        response = await ac.delete(url='api/v1/users/1')

        assert response.status_code == 403

    @staticmethod
    async def test_new_order(ac: AsyncClient, mock_order_id):
        response = await ac.post(url='api/v1/orders/', json={
            'phone_number': '+7(955)9556638',
            'admin_panel': True,
            'database': True
        })

        assert response.status_code == 201

    @staticmethod
    @pytest.mark.parametrize(
        ('order_id', 'code'), [
            (123123, 200),
            (321321, 404)
        ]
    )
    async def test_get_order_by_id(ac: AsyncClient, order_id, code):
        response = await ac.get(url=f'api/v1/orders/{order_id}')

        assert response.status_code == code

    @staticmethod
    async def test_get_orders(ac: AsyncClient):
        response = await ac.get(url='api/v1/orders/?limit=1&offset=0')

        assert response.json()[0]['email'] == USER
        assert response.status_code == 200


@pytest.mark.usefixtures('set_admin', 'mock_order_id')
class TestAdmin:

    @staticmethod
    async def test_get_users(ac: AsyncClient):
        response = await ac.get(url='api/v1/users/?limit=1&offset=0')

        assert response.status_code == 200

    @staticmethod
    async def test_get_user_by_id(ac: AsyncClient):
        response = await ac.get(url='api/v1/users/1')

        assert response.status_code == 200

    @staticmethod
    async def test_get_orders(ac: AsyncClient):
        response = await ac.get(url='api/v1/orders/?limit=1&offset=0')

        assert response.status_code == 200

    @staticmethod
    async def test_get_order_by_id(ac: AsyncClient):
        response = await ac.get(url='api/v1/orders/123123')

        assert response.status_code == 200

    @staticmethod
    async def test_delete_user(ac: AsyncClient):
        response = await ac.delete(url='api/v1/users/1')

        assert response.status_code == 204


