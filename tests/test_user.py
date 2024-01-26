import pytest
from httpx import AsyncClient
from src.config import SITE_NAME


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
