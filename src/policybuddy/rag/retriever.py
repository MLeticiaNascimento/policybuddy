from enum import Enum
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from policybuddy.rag.store import load_vector_store


DEFAULT_SCORE_THRESHOLD = 0.65


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


class PolicyRetriever(BaseRetriever):
    """
    Custom retriever for PolicyBuddy.

    Returns relevant documents while
    preserving retrieval evaluation metadata.
    """

    persist_directory: Path | None = None
    k: int = 4
    threshold: float = DEFAULT_SCORE_THRESHOLD

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> list[Document]:

        documents = retrieve_documents(
            query=query,
            persist_directory=self.persist_directory,
            k=self.k,
        )

        result = evaluate_context_quality(
            documents,
            threshold=self.threshold,
        )

        return add_retrieval_metadata(
            result.documents,
            result,
        )


def create_retriever(
    persist_directory: Path | None = None,
    k: int = 4,
    threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> PolicyRetriever:
    """
    Factory that creates the PolicyBuddy retriever.
    """

    return PolicyRetriever(
        persist_directory=persist_directory,
        k=k,
        threshold=threshold,
    )


def retrieve_documents(
    query: str,
    persist_directory: Path | None = None,
    k: int = 4,
) -> list[tuple[Document, float]]:
    """
    Retrieve documents from vector store.
    """

    vector_store = (
        load_vector_store(persist_directory)
        if persist_directory is not None
        else load_vector_store()
    )
    
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )


    print(
        "Results returned:",
        len(results)
    )


    return vector_store.similarity_search_with_score(
        query=query,
        k=k,
    )


def filter_relevant_documents(
    documents: list[tuple[Document, float]],
    threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> list[tuple[Document, float]]:
    """
    Filter documents using similarity score threshold.
    """

    return [
        (doc, score)
        for doc, score in documents
        if score <= threshold
    ]


def evaluate_context_quality(
    documents: list[tuple[Document, float]],
    threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> RetrievalResult:
    """
    Evaluate retrieval quality.
    """

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

    scores = [
        score
        for _, score in documents
    ]

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
            confidence=EvidenceConfidence.HIGH,
            best_score=best_score,
        )

    return RetrievalResult(
        documents=[],
        status=RetrievalStatus.EMPTY,
        confidence=EvidenceConfidence.LOW,
        best_score=best_score,
    )


def add_retrieval_metadata(
    documents: list[tuple[Document, float]],
    result: RetrievalResult,
) -> list[Document]:
    """
    Attach retrieval evaluation metadata
    to LangChain documents.
    """

    enriched_documents = []

    for document, score in documents:

        document.metadata.update(
            {
                "retrieval_status": result.status.value,
                "evidence_confidence": result.confidence.value,
                "retrieval_score": score,
                "best_score": result.best_score,
            }
        )

        enriched_documents.append(document)

    return enriched_documents