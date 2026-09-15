import logging
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.models.search import NormalizedSource
from backend.models.evidence import ClaimVerification, VerificationStatus
from backend.core.config import settings

logger = logging.getLogger(__name__)


class VerificationOutput(BaseModel):
    """Pydantic model for verification stage output."""
    claims: List[ClaimVerification] = Field(description="List of verified factual claims extracted from evidence.")
    conflicts: List[str] = Field(description="Explicit contradictions or conflicting facts found across sources.")
    uncertainties: List[str] = Field(description="Aspects where sources lack sufficient evidence.")


VERIFIER_PROMPT = """You are a rigorous evidence verification assistant.
Your goal is to evaluate candidate factual claims based STRICTLY on the retrieved sources below.

Question: {question}

Retrieved Evidence:
{evidence_text}

Instructions:
1. Extract key factual claims relevant to the question.
2. For each claim, evaluate if it is:
   - SUPPORTED: Clearly backed by one or more sources. Specify source IDs.
   - CONTRADICTED: Directly contradicted by another source.
   - INSUFFICIENT: Insufficient evidence in the provided sources to confirm.
3. List any explicit conflicts or conflicting numbers/facts found between sources.
4. List any key uncertainties where information is missing.
"""


class ClaimVerifier:
    """Uses Gemini via LangChain structured output to verify claims against evidence."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def verify_claims(self, question: str, sources: List[NormalizedSource]) -> VerificationOutput:
        if not self.api_key:
            return VerificationOutput(claims=[], conflicts=[], uncertainties=["LLM API key not available for claim verification."])

        # Prepare formatted evidence text
        evidence_chunks = []
        for src in sources:
            content = src.raw_content if src.content_fetched and src.raw_content else "\n".join(src.snippets)
            # Limit individual source snippet size for verifier prompt
            if len(content) > 3000:
                content = content[:3000] + "... [truncated]"
            evidence_chunks.append(f"Source ID: [{src.id}]\nURL: {src.canonical_url}\nTitle: {src.title}\nContent:\n{content}\n")

        evidence_text = "\n---\n".join(evidence_chunks)

        try:
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=self.api_key
            )

            structured_llm = llm.with_structured_output(VerificationOutput)
            prompt = ChatPromptTemplate.from_template(VERIFIER_PROMPT)
            chain = prompt | structured_llm

            from backend.observability.langfuse import observer
            callbacks = observer.get_callbacks()
            config = {"callbacks": callbacks} if callbacks else None

            result: VerificationOutput = await chain.ainvoke({

                "question": question,
                "evidence_text": evidence_text
            }, config=config)
            return result


        except Exception as exc:
            logger.warning(f"Claim verification failed: {exc}")
            return VerificationOutput(
                claims=[],
                conflicts=[],
                uncertainties=[f"Claim verification error: {str(exc)}"]
            )
