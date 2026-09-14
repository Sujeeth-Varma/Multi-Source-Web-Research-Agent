import pytest
from backend.models.search import SearchResult
from backend.services.deduplicator import SourceDeduplicator


def test_deduplication_merges_providers_and_snippets():
    results = [
        SearchResult(
            title="FastAPI Docs",
            url="https://fastapi.tiangolo.com/tutorial/?utm_source=serper",
            snippet="FastAPI framework tutorial overview.",
            provider="serper"
        ),
        SearchResult(
            title="FastAPI Official Documentation",
            url="https://fastapi.tiangolo.com/tutorial/",
            snippet="Build high performance APIs with Python.",
            provider="wikipedia"
        )
    ]

    sources = SourceDeduplicator.deduplicate(results)

    assert len(sources) == 1
    source = sources[0]
    assert source.canonical_url == "https://fastapi.tiangolo.com/tutorial"
    assert "serper" in source.providers
    assert "wikipedia" in source.providers
    assert source.provider_count == 2
    assert len(source.snippets) == 2
