from policybuddy.app.models import (
    PolicyBuddyResponse,
    SourceDocument,
)
from policybuddy.app.pipeline import ask_policybuddy


def answer_question(question: str) -> PolicyBuddyResponse:
    """
    Application service layer.

    Converts the internal pipeline result into
    a validated response model for the UI.
    """

    result = ask_policybuddy(question)

    return PolicyBuddyResponse(
        answer=result["answer"],
        confidence=result["evidence_confidence"],
        retrieval_status=result["retrieval_status"],
        best_score=result["best_score"],
        sources=[
            SourceDocument(
                content=document.page_content,
                metadata=document.metadata,
            )
            for document in result["documents"]
        ],
    )