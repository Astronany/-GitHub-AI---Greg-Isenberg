"""Sample checks against JSONPlaceholder /users."""

import pytest

pytestmark = pytest.mark.smoke


def test_get_user_by_id(client):
    response = client.get("/users/1")

    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["username"]
    assert "@" in user["email"]
    assert user["address"]["city"]
