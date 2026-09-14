from abc import ABC, abstractmethod
from typing import List
from backend.models.search import SearchResult


class BaseSearchProvider(ABC):
    """Abstract interface for all web search providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns provider name identifier (e.g. 'serper', 'wikipedia', 'duckduckgo')."""
        pass

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """Performs search query and returns list of raw SearchResult objects."""
        pass
