import logging
import asyncio
from typing import List
from duckduckgo_search import DDGS


from backend.providers.base import BaseSearchProvider
from backend.models.search import SearchResult
from backend.core.exceptions import ProviderException

logger = logging.getLogger(__name__)


class DuckDuckGoSearchProvider(BaseSearchProvider):
    """DuckDuckGo Search implementation (Zero API Key Fallback)."""

    @property
    def name(self) -> str:
        return "duckduckgo"

    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        def _sync_search():
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                return list(results) if results else []

        try:
            raw_results = await asyncio.to_thread(_sync_search)
            results = []
            for item in raw_results:
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("href", ""),
                        snippet=item.get("body", ""),
                        provider=self.name,
                        published_at=None,
                        relevance_score=None
                    )
                )
            return results

        except Exception as exc:
            logger.warning(f"DuckDuckGo search failed: {exc}")
            raise ProviderException(self.name, str(exc))
