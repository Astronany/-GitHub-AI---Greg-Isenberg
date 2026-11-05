"""Settings fallbacks. These do not call the network."""

from config import DEFAULT_BASE_URL, get_api_token, get_base_url


def test_blank_base_url_uses_public_demo(monkeypatch):
    monkeypatch.setenv("BASE_URL", "  ")
    assert get_base_url() == DEFAULT_BASE_URL


def test_base_url_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://example.test/api/")
    assert get_base_url() == "https://example.test/api"


def test_blank_token_is_omitted(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "")
    assert get_api_token() is None
