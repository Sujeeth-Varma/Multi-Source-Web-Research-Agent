import logging
import asyncio
import httpx
import trafilatura
from bs4 import BeautifulSoup
from typing import List
from backend.models.search import NormalizedSource
from backend.core.config import settings

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class PageFetcher:
    """Async webpage retrieval and main body text extraction service."""

    @staticmethod
    async def fetch_single(source: NormalizedSource, client: httpx.AsyncClient) -> NormalizedSource:
        headers = {"User-Agent": USER_AGENT}
        try:
            response = await client.get(
                source.canonical_url,
                headers=headers,
                follow_redirects=True,
                timeout=settings.HTTP_TIMEOUT_SECONDS
            )
            if response.status_code != 200:
                source.fetch_error = f"HTTP {response.status_code}"
                return source

            html_content = response.text
            # Extract main readable text using trafilatura
            text = trafilatura.extract(html_content, include_comments=False, include_tables=True)
            
            # Fallback to BeautifulSoup if trafilatura extraction returns empty string
            if not text:
                soup = BeautifulSoup(html_content, "html.parser")
                # Remove scripts and styles
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()
                text = soup.get_text(separator=" ", strip=True)

            if text:
                # Cap max content length to avoid overloading LLM prompt
                if len(text.encode("utf-8")) > settings.MAX_CONTENT_BYTES:
                    text = text[: settings.MAX_CONTENT_BYTES] + "... [truncated]"
                source.raw_content = text
                source.content_fetched = True
            else:
                source.fetch_error = "Empty text extracted"

        except httpx.TimeoutException:
            source.fetch_error = "Timeout"
        except httpx.HTTPError as exc:
            source.fetch_error = f"Network error: {type(exc).__name__}"
        except Exception as exc:
            logger.debug(f"Failed to fetch {source.canonical_url}: {exc}")
            source.fetch_error = str(exc)

        return source

    @classmethod
    async def fetch_sources(cls, sources: List[NormalizedSource]) -> List[NormalizedSource]:
        """Concurrently fetches content for a list of normalized sources."""
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
            tasks = [cls.fetch_single(source, client) for source in sources]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            return list(results)
