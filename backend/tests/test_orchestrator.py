import pytest
from backend.orchestrator.research import ResearchOrchestrator


def test_orchestrator_get_providers():
    orchestrator = ResearchOrchestrator()
    providers = orchestrator._get_providers()
    assert isinstance(providers, list)
    assert len(providers) >= 2
    provider_names = [p.name for p in providers]
    assert "wikipedia" in provider_names
    assert "duckduckgo" in provider_names
