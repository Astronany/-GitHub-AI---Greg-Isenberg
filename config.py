"""Runtime settings for the API test suite.

Read BASE_URL and API_TOKEN from the environment or a local .env file.
Blank values fall back to the public JSONPlaceholder demo and no auth,
so a fresh clone can run without secrets.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

DEFAULT_BASE_URL = "https://jsonplaceholder.typicode.com"


def get_base_url() -> str:
    value = os.getenv("BASE_URL", "").strip()
    return (value or DEFAULT_BASE_URL).rstrip("/")


def get_api_token() -> str | None:
    token = os.getenv("API_TOKEN", "").strip()
    return token or None
