"""Orders. This resource is the auth-gated part of the demo shop."""

import pytest

pytestmark = pytest.mark.smoke


async def test_list_orders_includes_seed(client):
    response = await client.get("/orders")

    assert response.status_code == 200
    by_id = {order["id"]: order for order in response.json()}
    assert by_id[1] == {
        "id": 1,
        "user_id": 1,
        "item_id": 1,
        "quantity": 2,
        "status": "placed",
    }


async def test_get_order_by_id(client):
    response = await client.get("/orders/1")

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 1
    assert body["item_id"] == 1
    assert body["status"] == "placed"


async def test_missing_order_returns_404(client):
    response = await client.get("/orders/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


async def test_create_order(client):
    payload = {"user_id": 2, "item_id": 2, "quantity": 3}
    response = await client.post("/orders", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["user_id"] == 2
    assert created["item_id"] == 2
    assert created["quantity"] == 3
    assert created["status"] == "placed"

    fetched = await client.get(f"/orders/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["quantity"] == 3


@pytest.mark.parametrize(
    ("method", "path"),
    [("get", "/orders"), ("get", "/orders/1"), ("post", "/orders")],
)
async def test_orders_require_token(anon_client, method, path):
    kwargs = {}
    if method == "post":
        kwargs["json"] = {"user_id": 1, "item_id": 1, "quantity": 1}
    response = await getattr(anon_client, method)(path, **kwargs)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_orders_reject_wrong_token(anon_client):
    response = await anon_client.get(
        "/orders",
        headers={"Authorization": "Bearer not-the-demo-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid bearer token"


async def test_create_order_missing_user(client):
    response = await client.post(
        "/orders",
        json={"user_id": 999999, "item_id": 1, "quantity": 1},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"


async def test_create_order_missing_item(client):
    response = await client.post(
        "/orders",
        json={"user_id": 1, "item_id": 999999, "quantity": 1},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Item not found"
