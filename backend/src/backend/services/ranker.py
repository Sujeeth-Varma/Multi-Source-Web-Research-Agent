from urllib.parse import urlparse
from typing import List
from backend.models.search import NormalizedSource

HIGH_TRUST_DOMAINS = {
    "docs.python.org", "github.com", "developer.mozilla.org", "arxiv.org",
    "wikipedia.org", "fastapi.tiangolo.com", "pydantic.dev", "langchain.com",
    "cloud.google.com", "aws.amazon.com", "microsoft.com", "nips.cc"
}


class SourceRanker:
    """Ranks and sorts sources based on relevance, domain trust, provider agreement, and content depth."""

    @staticmethod
    def score_source(source: NormalizedSource, query: str) -> float:
        score = 0.5  # Base score
        
        # 1. Provider Agreement signal (+0.25 per additional provider)
        score += (source.provider_count - 1) * 0.25
        
        # 2. Content completeness signal (+0.35 if full page fetched vs snippet only)
        if source.content_fetched and source.raw_content:
            score += 0.35
            
        # 3. Domain Trust signal
        parsed = urlparse(source.canonical_url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
            
        if any(domain.endswith(trust) for trust in HIGH_TRUST_DOMAINS) or domain.endswith(".gov") or domain.endswith(".edu"):
            score += 0.3
            
        # 4. Relevance keywords in title / snippets
        query_words = set(query.lower().split())
        title_words = set(source.title.lower().split())
        matches = len(query_words.intersection(title_words))
        if query_words:
            score += (matches / len(query_words)) * 0.2
            
        return round(score, 3)

    @classmethod
    def rank_and_filter(cls, sources: List[NormalizedSource], query: str, top_k: int = 8) -> List[NormalizedSource]:
        """Calculates scores for all sources and returns top_k ranked sources."""
        for src in sources:
            src.score = cls.score_source(src, query)
            
        ranked = sorted(sources, key=lambda x: x.score, reverse=True)
        return ranked[:top_k]
