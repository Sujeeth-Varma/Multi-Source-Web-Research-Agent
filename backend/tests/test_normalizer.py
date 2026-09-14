import pytest
from backend.services.normalizer import normalize_url


def test_url_normalization_strips_tracking_params():
    url1 = "https://example.com/article?utm_source=google&utm_medium=cpc&ref=123"
    url2 = "https://example.com/article"
    assert normalize_url(url1) == "https://example.com/article"
    assert normalize_url(url2) == "https://example.com/article"


def test_url_normalization_trailing_slash_and_case():
    url1 = "HTTP://Example.COM/docs/API/"
    url2 = "http://example.com/docs/API"
    assert normalize_url(url1) == "http://example.com/docs/API"
    assert normalize_url(url2) == "http://example.com/docs/API"


def test_url_normalization_preserves_legitimate_params():
    url = "https://example.com/search?q=fastapi&page=2&utm_source=twitter"
    normalized = normalize_url(url)
    assert "q=fastapi" in normalized
    assert "page=2" in normalized
    assert "utm_source" not in normalized
