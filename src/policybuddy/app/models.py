from pydantic import BaseModel

from policybuddy.rag.retriever import (
    EvidenceConfidence,
    RetrievalStatus,
)


class SourceDocument(BaseModel):
    content: str
    metadata: dict

class PolicyBuddyResponse(BaseModel):
    answer: str
    confidence: EvidenceConfidence
    retrieval_status: RetrievalStatus
    best_score: float | None
    sources: list[SourceDocument]