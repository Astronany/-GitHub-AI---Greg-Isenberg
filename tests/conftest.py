"""Shared HTTP client for API tests.

Swap environments by setting BASE_URL (and optionally API_TOKEN).
Example tests call paths such as /posts and /users on that base URL.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest

from config import get_api_token, get_base_url

# junitxml does not create parent directories.
Path("reports").mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def base_url() -> str:
    return get_base_url()


@pytest.fixture(scope="session")
def client(base_url: str) -> Iterator[httpx.Client]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "api-test-scaffold/0.1",
    }
    token = get_api_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with httpx.Client(
        base_url=base_url,
        headers=headers,
        timeout=30.0,
        follow_redirects=True,
    ) as http:
        yield http
