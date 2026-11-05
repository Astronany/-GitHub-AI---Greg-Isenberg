"""Product catalog on the demo shop API."""

import pytest

pytestmark = pytest.mark.smoke


async def test_list_items_includes_seed(client):
    response = await client.get("/items")

    assert response.status_code == 200
    by_id = {item["id"]: item for item in response.json()}
    assert by_id[1]["sku"] == "NB-100"
    assert by_id[1]["name"] == "Field notebook"
    assert by_id[1]["price_cents"] == 1299
    assert by_id[2]["sku"] == "PN-010"
    assert by_id[2]["price_cents"] == 199


async def test_get_item_by_id(client):
    response = await client.get("/items/2")

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "sku": "PN-010",
        "name": "Graphite pencil",
        "price_cents": 199,
    }


async def test_missing_item_returns_404(client):
    response = await client.get("/items/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
