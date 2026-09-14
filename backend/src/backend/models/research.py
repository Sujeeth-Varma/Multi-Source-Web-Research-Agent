from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ResearchRequest(BaseModel):
    """User input for research endpoint."""
    question: str = Field(..., min_length=3, description="Natural language research question")
    max_sources: Optional[int] = Field(default=8, ge=1, le=20, description="Max sources to retrieve & analyze")
    enable_planning: Optional[bool] = Field(default=True, description="Decompose complex question into sub-queries")


class KeyClaim(BaseModel):
    """Supported or evaluated key claim with citation links."""
    claim: str
    sources: List[str] = Field(default_factory=list, description="List of source IDs backing this claim")
    status: Optional[str] = "SUPPORTED"


class SourceMetadata(BaseModel):
    """Clean reference to a source in the final output."""
    id: str
    title: str
    url: str
    providers: List[str]
    score: float


class ResearchMetadata(BaseModel):
    """Execution metadata and telemetry for the research request."""
    providers_used: List[str]
    failed_providers: List[str] = Field(default_factory=list)
    total_queries: int
    sources_found: int
    sources_fetched: int
    sources_used: int
    execution_time_ms: float
    partial_results: bool = False
    warning_notes: List[str] = Field(default_factory=list)


class ResearchResponse(BaseModel):
    """Final grounded research response."""
    question: str
    answer: str
    key_claims: List[KeyClaim] = Field(default_factory=list)
    sources: List[SourceMetadata] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list, description="Contradictions found among sources")
    uncertainties: List[str] = Field(default_factory=list, description="Gaps or unverified claims")
    metadata: ResearchMetadata
