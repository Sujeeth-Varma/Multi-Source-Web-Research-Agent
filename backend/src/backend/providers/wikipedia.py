import logging
import httpx
from urllib.parse import quote
from typing import List
from backend.providers.base import BaseSearchProvider
from backend.models.search import SearchResult
from backend.core.exceptions import ProviderException
from backend.core.config import settings

logger = logging.getLogger(__name__)

USER_AGENT = "MultiSourceResearchAgent/1.0 (contact: research-agent@example.com)"



class WikipediaSearchProvider(BaseSearchProvider):
    """Wikipedia MediaWiki Search API implementation (Zero API Key required)."""

    def __init__(self):
        self._url = "https://en.wikipedia.org/w/api.php"

    @property
    def name(self) -> str:
        return "wikipedia"

    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "format": "json",
            "srlimit": max_results
        }
        headers = {
            "User-Agent": USER_AGENT,
            "Api-User-Agent": USER_AGENT
        }


        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
                response = await client.get(self._url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

                results = []
                query_data = data.get("query", {})
                for item in query_data.get("search", []):
                    title = item.get("title", "")
                    # Clean HTML tags like <span class="searchmatch"> from snippet
                    raw_snippet = item.get("snippet", "")
                    clean_snippet = raw_snippet.replace('<span class="searchmatch">', '').replace('</span>', '')
                    
                    page_url = f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
                    
                    results.append(
                        SearchResult(
                            title=f"{title} (Wikipedia)",
                            url=page_url,
                            snippet=clean_snippet,
                            provider=self.name,
                            published_at=None,
                            relevance_score=None
                        )
                    )
                return results

        except httpx.HTTPStatusError as exc:
            logger.warning(f"Wikipedia search HTTP error: {exc}")
            raise ProviderException(self.name, f"HTTP status error: {exc.response.status_code}")
        except Exception as exc:
            logger.warning(f"Wikipedia search failed: {exc}")
            raise ProviderException(self.name, str(exc))
