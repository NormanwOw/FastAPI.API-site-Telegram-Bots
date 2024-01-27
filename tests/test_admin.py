from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert

from tests.conftest import engine_test
from src.auth.models import User
from src.products.models import Product


class TestAdminUsers:

    @staticmethod
    async def test_get_user(admin: AsyncClient):
        response = await admin.get(url='api/v1/users/10')
        assert response.status_code == 200
        assert 'admin' in response.json().values()

        response = await admin.get(url='api/v1/users/111')
        assert response.status_code == 404

    @staticmethod
    @pytest.mark.parametrize(
        'username, email, f_name, l_name, superuser, staff, active, code', [
            ('admin', 'user@example.com', 'string', 'string', True, True, True, 200),
        ]
    )
    async def test_update_user(
            admin: AsyncClient, username, email, f_name, l_name, superuser, staff,
            active, code
    ):
        response = await admin.patch(url='api/v1/users/10', json={
            'username': username,
            'email': email,
            'first_name': f_name,
            'last_name': l_name,
            'is_superuser': superuser,
            'is_staff': staff,
            'is_active': active
        })
        assert response.status_code == code
        assert response.json().get('detail') == 'success'

        response = await admin.patch(url='api/v1/users/111', json={
            'username': username,
            'email': email,
            'first_name': f_name,
            'last_name': l_name,
            'is_superuser': superuser,
            'is_staff': staff,
            'is_active': active
        })
        assert response.status_code == 404

    @staticmethod
    async def test_delete_user(admin: AsyncClient):
        response = await admin.delete(url='api/v1/users/10')
        assert response.status_code == 204

        async with engine_test.begin() as conn:
            query = await conn.execute(
                select(User).where(User.id == 1)
            )
            assert query.first() is None

        response = await admin.delete(url='api/v1/users/111')
        assert response.status_code == 404

        async with engine_test.begin() as conn:
            await conn.execute(
                insert(User).values(
                    (10,
                     'pbkdf2_sha256$720000$IVtwOaY2WoUoR6ks39yRyT$lRda490enZstOAkqdFD15DP'
                     'SafQn2XyEWjtpMcZdfcg=', datetime.utcnow(),
                     True, 'admin', 'admin@example.com', True, True, None, None,
                     datetime.utcnow())
                )
            )


class TestAdminProducts:

    @staticmethod
    async def test_new_product(admin: AsyncClient):
        response = await admin.post(url='api/v1/products/', json={
            'name': 'example',
            'title': 'example',
            'description': 'example text',
            'price': 1111
        })
        assert response.status_code == 201

        async with engine_test.begin() as conn:
            result = await conn.execute(
                select(Product).where(
                    Product.name == 'example', Product.title == 'example',
                    Product.description == 'example text', Product.price == 1111
                )
            )
            assert result.first() is not None

    @staticmethod
    async def test_update_product(admin: AsyncClient):
        response = await admin.patch(url='api/v1/products/example', json={
            'name': 'string',
            'title': 'string',
            'description': 'string',
            'price': 2222
        })

        assert response.status_code == 200

        async with engine_test.begin() as conn:
            result = await conn.execute(
                select(Product).where(
                    Product.name == 'string', Product.title == 'string',
                    Product.description == 'string', Product.price == 2222
                )
            )
            assert result.first() is not None

    @staticmethod
    async def test_delete_product(admin: AsyncClient):
        response = await admin.delete(url='api/v1/products/string')
        assert response.status_code == 204

        async with engine_test.begin() as conn:
            result = await conn.execute(
                select(Product).where(
                    Product.name == 'string', Product.title == 'string',
                    Product.description == 'string', Product.price == 2222
                )
            )
            assert result.first() is None
