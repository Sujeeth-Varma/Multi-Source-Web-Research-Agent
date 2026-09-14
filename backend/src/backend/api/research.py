import logging
from fastapi import APIRouter, HTTPException, status
from backend.models.research import ResearchRequest, ResearchResponse
from backend.orchestrator.research import ResearchOrchestrator
from backend.core.exceptions import BaseResearchException

logger = logging.getLogger(__name__)
router = APIRouter()
orchestrator = ResearchOrchestrator()


@router.post("/research", response_model=ResearchResponse, summary="Execute Web Research")
async def execute_research(request: ResearchRequest) -> ResearchResponse:
    """
    Accepts a natural language question, executes multi-provider search, URL deduplication,
    web content fetching, source ranking, Gemini claim verification, and synthesis.
    """
    try:
        response = await orchestrator.execute_research(request)
        return response
    except BaseResearchException as exc:
        logger.warning(f"Research request failed: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if exc.code == "INVALID_REQUEST" else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": exc.code, "message": exc.message}
        )
    except Exception as exc:
        logger.exception("Unexpected error during research execution")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "INTERNAL_SERVER_ERROR", "message": str(exc)}
        )
