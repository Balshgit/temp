import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from settings.config import AppSettings
from tests.integration.factories.users import UserFactory

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_users_for_not_authorized_user(
    rest_client: AsyncClient,
) -> None:
    response = await rest_client.get("/api/users")
    assert response.status_code == 403


async def test_get_users_empty_list(
    sync_db: Session,
    user_client: AsyncClient,
) -> None:
    response = await user_client.get("/api/users")
    assert response.status_code == 200
    data = response.json()

    assert data == []


async def test_get_users(
    sync_db: Session,
    user_client: AsyncClient,
) -> None:
    users = UserFactory.create_batch(size=3)
    user_1, user_2, user_3 = sorted(users, key=lambda u: u.id)

    response = await user_client.get("/api/users")
    assert response.status_code == 200

    data = response.json()


    assert data == [
        {
            "id": user_1.id,
            "username": user_1.username,
            "first_name": user_1.first_name,
            "last_name": user_1.last_name,
        },
        {
            "id": user_2.id,
            "username": user_2.username,
            "first_name": user_2.first_name,
            "last_name": user_2.last_name,
        },
        {
            "id": user_3.id,
            "username": user_3.username,
            "first_name": user_3.first_name,
            "last_name": user_3.last_name,
        },
    ]


async def test_get_users_by_id_not_found(
    sync_db: Session,
    user_client: AsyncClient,
) -> None:
    user = UserFactory()
    not_existing_user_id = user.id + 9999

    response = await user_client.get(f"/api/users/{not_existing_user_id}")
    assert response.status_code == 404


async def test_get_users_by_id(
    sync_db: Session,
    user_client: AsyncClient,
) -> None:
    user = UserFactory()

    response = await user_client.get(f"/api/users/{user.id}")
    assert response.status_code == 200

    data = response.json()


    assert data == {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_active": user.is_active,
    }