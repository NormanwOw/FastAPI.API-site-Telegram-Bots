import pytest
from httpx import AsyncClient

from src.config import SITE_NAME


class TestAnonym:

    @staticmethod
    async def test_try_locked_endpoints(ac: AsyncClient):
        for response in [
            await ac.get(url='api/v1/users/me'),
            await ac.get(url='api/v1/users/1'),
            await ac.get(url='api/v1/users/'),
            await ac.patch(url='api/v1/users/'),
            await ac.patch(url='api/v1/users/1'),
            await ac.delete(url='api/v1/users/'),
            await ac.delete(url='api/v1/users/1'),
            await ac.get(url='api/v1/orders/'),
            await ac.get(url='api/v1/orders/1'),
            await ac.post(url='api/v1/orders/'),
            await ac.delete(url='api/v1/orders/1'),
            await ac.get(url='api/v1/products/'),
            await ac.post(url='api/v1/products/'),
            await ac.patch(url='api/v1/products/1'),
            await ac.delete(url='api/v1/products/1'),
        ]:
            assert response.status_code == 403


class TestAnonymAuth:

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
    async def test_change_password(ac: AsyncClient):
        response = await ac.post(url='api/v1/auth/change-password')
        assert response.status_code == 403

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
                assert ac.cookies.get(SITE_NAME) is not None

    @staticmethod
    async def test_logout(ac: AsyncClient):
        response = await ac.post(url='api/v1/auth/logout')

        assert response.status_code == 200
        assert 'success' in response.json().get('detail')
        assert ac.cookies.get(SITE_NAME) is None



