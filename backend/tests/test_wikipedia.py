import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from backend.providers.wikipedia import WikipediaSearchProvider


@pytest.mark.asyncio
async def test_wikipedia_search_provider():
    provider = WikipediaSearchProvider()
    assert provider.name == "wikipedia"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "query": {
            "search": [
                {
                    "title": "FastAPI",
                    "snippet": "FastAPI is a modern web framework."
                }
            ]
        }
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        results = await provider.search("FastAPI", max_results=3)
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0].provider == "wikipedia"
        assert "FastAPI (Wikipedia)" in results[0].title
        assert "https://en.wikipedia.org/wiki/FastAPI" in results[0].url
