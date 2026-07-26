from enum import Enum
from pathlib import Path

from langchain_core.documents import Document

from policybuddy.rag.store import load_vector_store

DEFAULT_SCORE_THRESHOLD = 0.35


class RetrievalStatus(str, Enum):
    FOUND = "found"
    PARTIAL = "partial"
    EMPTY = "empty"


class EvidenceConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RetrievalResult:
    def __init__(
        self,
        documents: list[tuple[Document, float]],
        status: RetrievalStatus,
        confidence: EvidenceConfidence,
        best_score: float | None,
    ):
        self.documents = documents
        self.status = status
        self.confidence = confidence
        self.best_score = best_score


def retrieve_documents(
    query: str,
    persist_directory: Path | None = None,
    k: int = 4,
) -> list[tuple[Document, float]]:

    vector_store = (
        load_vector_store(persist_directory)
        if persist_directory is not None
        else load_vector_store()
    )

    return vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )


def filter_relevant_documents(
    documents: list[tuple[Document, float]],
    threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> list[tuple[Document, float]]:

    return [(doc, score) for doc, score in documents if score <= threshold]


def evaluate_context_quality(
    documents: list[tuple[Document, float]],
    threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> RetrievalResult:

    if not documents:
        return RetrievalResult(
            documents=[],
            status=RetrievalStatus.EMPTY,
            confidence=EvidenceConfidence.LOW,
            best_score=None,
        )

    relevant_documents = filter_relevant_documents(
        documents,
        threshold,
    )

    scores = [score for _, score in documents]

    best_score = min(scores)

    if len(relevant_documents) >= 2:
        return RetrievalResult(
            documents=relevant_documents,
            status=RetrievalStatus.FOUND,
            confidence=EvidenceConfidence.HIGH,
            best_score=best_score,
        )

    if len(relevant_documents) == 1:
        return RetrievalResult(
            documents=relevant_documents,
            status=RetrievalStatus.PARTIAL,
            confidence=EvidenceConfidence.MEDIUM,
            best_score=best_score,
        )

    return RetrievalResult(
        documents=[],
        status=RetrievalStatus.EMPTY,
        confidence=EvidenceConfidence.LOW,
        best_score=best_score,
    )
