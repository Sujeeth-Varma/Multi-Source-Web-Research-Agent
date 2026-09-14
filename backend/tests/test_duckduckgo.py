import pytest
from unittest.mock import patch, MagicMock
from backend.providers.duckduckgo import DuckDuckGoSearchProvider


@pytest.mark.asyncio
async def test_duckduckgo_search_provider():
    provider = DuckDuckGoSearchProvider()
    assert provider.name == "duckduckgo"

    mock_results = [
        {"title": "FastAPI Web Framework", "href": "https://fastapi.tiangolo.com", "body": "FastAPI framework tutorial."}
    ]

    with patch("backend.providers.duckduckgo.DDGS") as mock_ddgs:
        instance = MagicMock()
        instance.__enter__.return_value = instance
        instance.text.return_value = mock_results
        mock_ddgs.return_value = instance

        results = await provider.search("FastAPI Python", max_results=3)
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0].title == "FastAPI Web Framework"
        assert results[0].url == "https://fastapi.tiangolo.com"
        assert results[0].provider == "duckduckgo"
