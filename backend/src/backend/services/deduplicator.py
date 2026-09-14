from typing import List, Dict
from backend.models.search import SearchResult, NormalizedSource
from backend.services.normalizer import normalize_url


class SourceDeduplicator:
    """Deduplicates search results by normalized URL while tracking provider agreement."""

    @staticmethod
    def deduplicate(results: List[SearchResult]) -> List[NormalizedSource]:
        source_map: Dict[str, NormalizedSource] = {}
        source_counter = 1

        for item in results:
            if not item.url:
                continue
                
            canonical = normalize_url(item.url)
            if not canonical:
                continue

            if canonical in source_map:
                existing = source_map[canonical]
                if item.provider not in existing.providers:
                    existing.providers.append(item.provider)
                    existing.provider_count = len(existing.providers)
                if item.snippet and item.snippet not in existing.snippets:
                    existing.snippets.append(item.snippet)
            else:
                source_id = f"source_{source_counter}"
                source_counter += 1
                source_map[canonical] = NormalizedSource(
                    id=source_id,
                    canonical_url=canonical,
                    title=item.title or canonical,
                    snippets=[item.snippet] if item.snippet else [],
                    providers=[item.provider],
                    provider_count=1,
                    raw_content=None,
                    content_fetched=False
                )

        return list(source_map.values())
