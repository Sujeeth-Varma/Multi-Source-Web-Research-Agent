import logging
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.models.search import NormalizedSource
from backend.services.verifier import VerificationOutput
from backend.core.config import settings
from backend.core.exceptions import LLMUnavailableException

logger = logging.getLogger(__name__)


class SynthesisOutput(BaseModel):
    """Pydantic schema for final research synthesis."""
    answer: str = Field(
        description="Detailed, comprehensive research answer grounded strictly in the provided evidence. Cite sources inline like [source_1]."
    )


SYNTHESIZER_PROMPT = """You are an expert technical researcher synthesizing a grounded answer to a user's question.

User Question: {question}

Evidence & Verification Summary:
- Verified Claims: {verified_claims_summary}
- Identified Conflicts: {conflicts_summary}
- Identified Uncertainties: {uncertainties_summary}

Source Evidence:
{sources_text}

Strict Synthesis Rules:
1. Base your answer strictly on the provided sources and verified claims.
2. DO NOT invent citations or facts. Use inline citations such as [source_1], [source_2] matching the provided Source IDs.
3. Explicitly mention any conflicts or contradictory evidence if relevant.
4. Clearly state any uncertainties or aspects where evidence is lacking.
5. Provide a well-structured, clear markdown answer.
"""


class ResearchSynthesizer:
    """Uses Gemini via LangChain structured output to generate the final grounded answer."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def synthesize(
        self,
        question: str,
        sources: List[NormalizedSource],
        verification: VerificationOutput
    ) -> SynthesisOutput:
        if not self.api_key:
            raise LLMUnavailableException("Gemini API key missing. Cannot generate synthesis.")

        sources_text = ""
        for src in sources:
            content = src.raw_content if src.content_fetched and src.raw_content else "\n".join(src.snippets)
            if len(content) > 3000:
                content = content[:3000] + "... [truncated]"
            sources_text += f"Source ID: [{src.id}]\nTitle: {src.title}\nURL: {src.canonical_url}\nContent:\n{content}\n---\n"

        verified_claims_summary = "\n".join([f"- {c.claim} (Status: {c.status}, Sources: {c.supporting_sources})" for c in verification.claims]) or "None"
        conflicts_summary = "\n".join([f"- {c}" for c in verification.conflicts]) or "None"
        uncertainties_summary = "\n".join([f"- {u}" for u in verification.uncertainties]) or "None"

        try:
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=self.api_key,
                temperature=0.2
            )

            structured_llm = llm.with_structured_output(SynthesisOutput)
            prompt = ChatPromptTemplate.from_template(SYNTHESIZER_PROMPT)
            chain = prompt | structured_llm

            from backend.observability.langfuse import observer
            callbacks = observer.get_callbacks()
            config = {"callbacks": callbacks} if callbacks else None

            result: SynthesisOutput = await chain.ainvoke({

                "question": question,
                "verified_claims_summary": verified_claims_summary,
                "conflicts_summary": conflicts_summary,
                "uncertainties_summary": uncertainties_summary,
                "sources_text": sources_text
            }, config=config)
            return result


        except Exception as exc:
            logger.error(f"Synthesis generation failed: {exc}")
            raise LLMUnavailableException(f"Synthesis LLM generation error: {str(exc)}")
