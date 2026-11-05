"""Settings fallbacks. These do not call the network."""

from config import DEFAULT_API_TOKEN, get_api_token, get_base_url


def test_demo_token_is_the_documented_default():
    assert DEFAULT_API_TOKEN == "demo-token"


def test_blank_base_url_uses_inprocess_app(monkeypatch):
    monkeypatch.setenv("BASE_URL", "  ")
    assert get_base_url() is None


def test_base_url_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://staging.example.test/api/")
    assert get_base_url() == "https://staging.example.test/api"


def test_blank_token_uses_demo_default(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "  ")
    assert get_api_token() == DEFAULT_API_TOKEN


def test_token_override(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "staging-secret")
    assert get_api_token() == "staging-secret"
