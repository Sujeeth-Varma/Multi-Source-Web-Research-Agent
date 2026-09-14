import logging
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.core.config import settings
from backend.core.exceptions import LLMUnavailableException

logger = logging.getLogger(__name__)


class QueryPlanOutput(BaseModel):
    """Pydantic model for structured research query breakdown."""
    queries: List[str] = Field(
        description="List of 2 to 4 targeted, independent search engine queries designed to research the question."
    )


PLANNER_PROMPT = """You are a senior technical research planner. 
Decompose the following user question into 2 to 4 distinct, highly effective web search engine queries.
Each query should target different aspects, subtopics, or perspectives (e.g. documentation, benchmarks, comparisons, direct definitions).

User Question: {question}
"""


class ResearchPlanner:
    """Uses Gemini via LangChain structured output to decompose complex research questions."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def plan_queries(self, question: str) -> List[str]:
        if not self.api_key:
            logger.warning("No Gemini API key provided. Skipping planning decomposition.")
            return [question]

        try:
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=self.api_key,
                temperature=0.1
            )

            structured_llm = llm.with_structured_output(QueryPlanOutput)
            prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
            from backend.observability.langfuse import observer
            callbacks = observer.get_callbacks()
            config = {"callbacks": callbacks} if callbacks else None

            result: QueryPlanOutput = await chain.ainvoke({"question": question}, config=config)

            if result and result.queries:
                # Ensure queries are capped at max limit
                cleaned = [q.strip() for q in result.queries if q.strip()]
                return cleaned[: settings.MAX_PLANNING_QUERIES]
            return [question]

        except Exception as exc:
            logger.warning(f"Research planner failed, falling back to original query: {exc}")
            return [question]
