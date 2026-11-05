"""Liveness of the demo business API."""

import pytest

pytestmark = pytest.mark.smoke


async def test_health(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_root_names_the_demo_api(client):
    response = await client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Demo Business API"
    assert body["health"] == "/health"
