import pytest
from httpx import AsyncClient

from sqlalchemy.orm import Session

from settings.config import AppSettings
from tests.integration.factories.users import UserFactory


pytestmark = [
    pytest.mark.asyncio,
]

async def test_get_chatgpt_models(
    sync_db: Session,
    rest_client: AsyncClient,
    test_settings: AppSettings,
) -> None:
    users = UserFactory.create_batch(size=3)

    response = await rest_client.get("/api/users")
    assert response.status_code == 200

    assert response.json() == {}
