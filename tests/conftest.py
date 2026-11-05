"""Shared HTTP client for API tests.

Blank BASE_URL mounts the in-repo FastAPI app with httpx's ASGITransport,
so local runs and GitHub Actions do not need a listening server.

Set BASE_URL to send the same requests to a running uvicorn process or,
later, a real staging environment. API_TOKEN is sent as a bearer token.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest

from config import get_api_token, get_base_url

# junitxml does not create parent directories.
Path("reports").mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def reset_demo_store() -> Iterator[None]:
    """Give each in-process test a fresh seed catalog.

    An external BASE_URL is another process, so its data is left alone.
    Create-tests use unique fields and list-tests look up seed ids.
    """
    if get_base_url() is not None:
        yield
        return
    from app.store import store

    store.reset()
    yield


def _headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "api-test-scaffold/0.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _async_client(token: str | None) -> httpx.AsyncClient:
    headers = _headers(token)
    base_url = get_base_url()
    if base_url is None:
        from app.main import app

        transport = httpx.ASGITransport(app=app)
        return httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )
    return httpx.AsyncClient(
        base_url=base_url,
        headers=headers,
        timeout=30.0,
        follow_redirects=True,
    )


@pytest.fixture
async def client(reset_demo_store: None) -> AsyncIterator[httpx.AsyncClient]:
    async with _async_client(get_api_token()) as http:
        yield http


@pytest.fixture
async def anon_client(reset_demo_store: None) -> AsyncIterator[httpx.AsyncClient]:
    async with _async_client(None) as http:
        yield http
