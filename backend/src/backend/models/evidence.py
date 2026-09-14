from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class VerificationStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    INSUFFICIENT = "INSUFFICIENT"


class Evidence(BaseModel):
    """Extracted evidence chunk from a normalized source."""
    source_id: str
    url: str
    title: str
    excerpt: str
    relevance_score: float = 0.0


class ClaimVerification(BaseModel):
    """Verification result for a specific claim against available evidence."""
    claim: str
    status: VerificationStatus
    supporting_sources: List[str] = Field(default_factory=list)
    explanation: Optional[str] = None
