import logging
import httpx
from typing import List
from backend.providers.base import BaseSearchProvider
from backend.models.search import SearchResult
from backend.core.exceptions import ProviderException
from backend.core.config import settings

logger = logging.getLogger(__name__)


class SerperSearchProvider(BaseSearchProvider):
    """Serper (Google Search API) implementation."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.SERPER_API_KEY
        self._url = "https://google.serper.dev/search"

    @property
    def name(self) -> str:
        return "serper"

    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        if not self.api_key:
            raise ProviderException(self.name, "API Key missing")

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": max_results
        }

        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
                response = await client.post(self._url, headers=headers, json=payload)
                
                if response.status_code == 401 or response.status_code == 403:
                    raise ProviderException(self.name, "Invalid API key or unauthorized")

                response.raise_for_status()
                data = response.json()
                
                results = []
                for item in data.get("organic", []):
                    results.append(
                        SearchResult(
                            title=item.get("title", ""),
                            url=item.get("link", ""),
                            snippet=item.get("snippet", ""),
                            provider=self.name,
                            published_at=item.get("date"),
                            relevance_score=None
                        )
                    )
                return results

        except httpx.HTTPStatusError as exc:
            logger.warning(f"Serper search HTTP error: {exc}")
            raise ProviderException(self.name, f"HTTP status error: {exc.response.status_code}")
        except Exception as exc:
            logger.warning(f"Serper search failed: {exc}")
            raise ProviderException(self.name, str(exc))
