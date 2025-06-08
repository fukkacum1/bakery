import pytest
from httpx import AsyncClient, Response

from tests.conftest import make_request


@pytest.mark.asyncio
async def test_get_sorted_bakeries(async_client):
    response: Response = await make_request(client=async_client, api_url="/bakeries/sorted")
    assert response.status_code == 200
