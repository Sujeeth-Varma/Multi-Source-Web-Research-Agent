from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SearchResult(BaseModel):
    """Raw result returned by an individual search provider before deduplication."""
    title: str
    url: str
    snippet: str
    provider: str
    published_at: Optional[str] = None
    relevance_score: Optional[float] = None


class NormalizedSource(BaseModel):
    """Cleaned, deduplicated source aggregated across providers."""
    id: str = Field(description="Unique identifier for the source, e.g., source_1")
    canonical_url: str
    title: str
    snippets: List[str] = Field(default_factory=list)
    providers: List[str] = Field(default_factory=list, description="List of search providers that found this URL")
    provider_count: int = 1
    raw_content: Optional[str] = Field(default=None, description="Extracted web page text")
    content_fetched: bool = False
    fetch_error: Optional[str] = None
    score: float = 0.0
