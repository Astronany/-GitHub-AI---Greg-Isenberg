"""Customers on the demo shop API."""

from uuid import uuid4

import pytest

pytestmark = pytest.mark.smoke


def _new_user() -> dict[str, str]:
    suffix = uuid4().hex[:8]
    return {
        "name": "Casey Example",
        "username": f"casey_{suffix}",
        "email": f"casey_{suffix}@example.com",
    }


async def test_list_users_includes_seed(client):
    response = await client.get("/users")

    assert response.status_code == 200
    by_id = {user["id"]: user for user in response.json()}
    assert by_id[1]["username"] == "ada"
    assert by_id[1]["email"] == "ada@example.com"
    assert by_id[2]["name"] == "Grace Hopper"


async def test_get_user_by_id(client):
    response = await client.get("/users/1")

    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["username"] == "ada"
    assert user["email"] == "ada@example.com"


async def test_missing_user_returns_404(client):
    response = await client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_create_user(client):
    payload = _new_user()
    response = await client.post("/users", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["name"] == payload["name"]
    assert created["username"] == payload["username"]
    assert created["email"] == payload["email"]
    assert isinstance(created["id"], int)

    fetched = await client.get(f"/users/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["username"] == payload["username"]


async def test_create_user_requires_token(anon_client):
    response = await anon_client.post("/users", json=_new_user())

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_list_users_is_public(anon_client):
    response = await anon_client.get("/users")

    assert response.status_code == 200
    assert any(user["id"] == 1 for user in response.json())


async def test_duplicate_email_returns_409(client):
    payload = _new_user()
    first = await client.post("/users", json=payload)
    assert first.status_code == 201

    again = dict(payload)
    again["username"] = f"other_{uuid4().hex[:8]}"
    second = await client.post("/users", json=again)

    assert second.status_code == 409
    assert second.json()["detail"] == "Email already exists"


async def test_create_user_rejects_bad_email(client):
    response = await client.post(
        "/users",
        json={"name": "Casey Example", "username": "casey", "email": "not-an-email"},
    )

    assert response.status_code == 422
