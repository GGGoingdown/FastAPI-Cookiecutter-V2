import pytest
from httpx import AsyncClient

endpoint = "/health"

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {"detail": "ok"}
