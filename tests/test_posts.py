"""Sample checks against JSONPlaceholder /posts.

Replace or extend these when BASE_URL points at a real test environment.
"""

import pytest

pytestmark = pytest.mark.smoke


def test_get_post_by_id(client):
    response = client.get("/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert isinstance(body["title"], str) and body["title"]
    assert isinstance(body["body"], str) and body["body"]
    assert body["userId"] == 1


def test_list_posts_for_user(client):
    response = client.get("/posts", params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert posts
    assert all(post["userId"] == 1 for post in posts)


def test_create_post(client):
    payload = {
        "title": "scaffold example",
        "body": "created by the api test scaffold",
        "userId": 1,
    }
    response = client.post("/posts", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]


def test_missing_post_returns_404(client):
    response = client.get("/posts/999999")
    assert response.status_code == 404
