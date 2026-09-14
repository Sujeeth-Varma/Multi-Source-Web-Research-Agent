import pytest
from backend.models.search import NormalizedSource
from backend.services.ranker import SourceRanker


def test_ranker_scores_trusted_domains_and_provider_agreement_higher():
    trusted_multi_provider = NormalizedSource(
        id="source_1",
        canonical_url="https://docs.python.org/3/library/asyncio.html",
        title="asyncio — Asynchronous I/O",
        snippets=["Python asyncio docs"],
        providers=["wikipedia", "serper"],
        provider_count=2,
        raw_content="Full documentation text",
        content_fetched=True
    )

    unknown_single_provider = NormalizedSource(
        id="source_2",
        canonical_url="https://some-random-blog.xyz/asyncio",
        title="Asyncio tips",
        snippets=["Random blog snippet"],
        providers=["serper"],
        provider_count=1,
        raw_content=None,
        content_fetched=False
    )

    ranked = SourceRanker.rank_and_filter([unknown_single_provider, trusted_multi_provider], query="asyncio python", top_k=2)

    assert len(ranked) == 2
    assert ranked[0].id == "source_1"  # Trusted multi-provider should rank higher
    assert ranked[0].score > ranked[1].score
