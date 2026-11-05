"""Runtime settings for the API test suite and the demo app.

BASE_URL and API_TOKEN come from the environment or a local .env file.
Blank BASE_URL means "call the in-repo demo app in-process".
Blank API_TOKEN means the public demo credential, so a fresh clone and
GitHub Actions can run without secrets.

Shell variables already set in the environment win over .env.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Public demo credential. Documented in README and .env.example.
# Replace it via API_TOKEN when the suite points at a real environment.
DEFAULT_API_TOKEN = "demo-token"


def get_base_url() -> str | None:
    """Return the external base URL, or None to use the in-process demo app."""
    value = os.getenv("BASE_URL", "").strip()
    return value.rstrip("/") or None


def get_api_token() -> str:
    token = os.getenv("API_TOKEN", "").strip()
    return token or DEFAULT_API_TOKEN
