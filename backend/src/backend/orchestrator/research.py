import time
import asyncio
import logging
from typing import List
from backend.models.research import (
    ResearchRequest, ResearchResponse, KeyClaim, SourceMetadata, ResearchMetadata
)
from backend.models.search import SearchResult
from backend.providers.base import BaseSearchProvider
from backend.providers.serper import SerperSearchProvider
from backend.providers.duckduckgo import DuckDuckGoSearchProvider
from backend.providers.wikipedia import WikipediaSearchProvider
from backend.services.planner import ResearchPlanner
from backend.services.deduplicator import SourceDeduplicator
from backend.services.fetcher import PageFetcher
from backend.services.ranker import SourceRanker
from backend.services.verifier import ClaimVerifier
from backend.services.synthesizer import ResearchSynthesizer
from backend.core.config import settings
from backend.core.exceptions import BaseResearchException, ProviderException, LLMUnavailableException
from backend.observability.langfuse import observer

logger = logging.getLogger(__name__)


class ResearchOrchestrator:
    """Core Python Async Orchestrator bringing together research stages."""

    def __init__(self):
        self.planner = ResearchPlanner()
        self.verifier = ClaimVerifier()
        self.synthesizer = ResearchSynthesizer()

    def _get_providers(self) -> List[BaseSearchProvider]:

        """Instantiates active search providers based on environment configuration."""
        providers: List[BaseSearchProvider] = []

        if settings.SERPER_API_KEY:
            providers.append(SerperSearchProvider())

        # Zero-API key providers: Wikipedia and DuckDuckGo
        providers.append(WikipediaSearchProvider())
        providers.append(DuckDuckGoSearchProvider())

        return providers




    async def execute_research(self, request: ResearchRequest) -> ResearchResponse:
        start_time = time.time()
        providers = self._get_providers()
        
        failed_providers = []
        warning_notes = []

        # 1. Planning Phase
        queries = [request.question]
        if request.enable_planning:
            queries = await self.planner.plan_queries(request.question)
        
        # 2. Multi-Source Retrieval Phase (Parallel across providers and queries)
        search_tasks = []
        search_metadata_map = []  # keep track of (provider_instance, query)

        for query in queries:
            for provider in providers:
                search_tasks.append(provider.search(query, max_results=settings.MAX_SEARCH_RESULTS_PER_QUERY))
                search_metadata_map.append((provider.name, query))

        search_results_nested = await asyncio.gather(*search_tasks, return_exceptions=True)

        all_raw_results: List[SearchResult] = []
        successful_providers = set()

        for idx, res in enumerate(search_results_nested):
            provider_name, query = search_metadata_map[idx]
            if isinstance(res, Exception):
                logger.warning(f"Search provider '{provider_name}' failed for query '{query}': {res}")
                if provider_name not in failed_providers:
                    failed_providers.append(provider_name)
            elif isinstance(res, list):
                successful_providers.add(provider_name)
                all_raw_results.extend(res)

        # Fallback trigger: If all primary providers failed, try DuckDuckGo as last resort
        if not all_raw_results and "duckduckgo" not in successful_providers:
            logger.info("Primary providers returned no results. Triggering emergency DuckDuckGo search.")
            ddg = DuckDuckGoSearchProvider()
            try:
                for query in queries:
                    res = await ddg.search(query, max_results=settings.MAX_SEARCH_RESULTS_PER_QUERY)
                    all_raw_results.extend(res)
                successful_providers.add(ddg.name)
            except Exception as exc:
                logger.error(f"Emergency DuckDuckGo fallback search failed: {exc}")
                failed_providers.append(ddg.name)

        if not all_raw_results:
            raise BaseResearchException(
                "All search providers failed to retrieve results for your query.",
                code="RETRIEVAL_FAILED"
            )

        if len(successful_providers) < 2:
            warning_notes.append("Multi-source retrieval partial: Fewer than two independent search providers succeeded.")

        # 3. Deduplication Phase
        normalized_sources = SourceDeduplicator.deduplicate(all_raw_results)
        sources_found_count = len(normalized_sources)

        # 4. Web Page Content Fetching Phase
        max_fetch = min(request.max_sources or settings.MAX_SOURCES_TO_FETCH, len(normalized_sources))
        sources_to_fetch = normalized_sources[:max_fetch]
        fetched_sources = await PageFetcher.fetch_sources(sources_to_fetch)
        sources_fetched_count = sum(1 for s in fetched_sources if s.content_fetched)

        # 5. Ranking Phase
        ranked_sources = SourceRanker.rank_and_filter(
            fetched_sources,
            query=request.question,
            top_k=request.max_sources or settings.MAX_SOURCES_TO_FETCH
        )

        # 6. Verification Phase
        verification_output = await self.verifier.verify_claims(request.question, ranked_sources)

        # 7. Synthesis Phase
        synthesis_output = await self.synthesizer.synthesize(request.question, ranked_sources, verification_output)

        # 8. Assemble Metadata and Response
        key_claims = [
            KeyClaim(claim=c.claim, sources=c.supporting_sources, status=c.status.value)
            for c in verification_output.claims
        ]

        source_metadata_list = [
            SourceMetadata(
                id=s.id,
                title=s.title,
                url=s.canonical_url,
                providers=s.providers,
                score=s.score
            )
            for s in ranked_sources
        ]

        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        metadata = ResearchMetadata(
            providers_used=list(successful_providers),
            failed_providers=failed_providers,
            total_queries=len(queries),
            sources_found=sources_found_count,
            sources_fetched=sources_fetched_count,
            sources_used=len(ranked_sources),
            execution_time_ms=execution_time_ms,
            partial_results=bool(failed_providers),
            warning_notes=warning_notes
        )

        observer.flush()

        return ResearchResponse(
            question=request.question,
            answer=synthesis_output.answer,
            key_claims=key_claims,
            sources=source_metadata_list,
            conflicts=verification_output.conflicts,
            uncertainties=verification_output.uncertainties,
            metadata=metadata
        )

