from pathlib import Path

from policybuddy.rag.loader import load_documents
from policybuddy.rag.retriever import (
    EvidenceConfidence,
    PolicyRetriever,
    RetrievalStatus,
    retrieve_documents,
)
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import create_vector_store


def create_test_vectorstore(tmp_path: Path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    return vectorstore_path

def test_retrieve_documents_returns_list(tmp_path):

    vectorstore_path = create_test_vectorstore(
        tmp_path
    )

    results = retrieve_documents(
        query="password policy",
        persist_directory=vectorstore_path,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) > 0

def test_policy_retriever_returns_documents_with_metadata(
    tmp_path,
):

    vectorstore_path = create_test_vectorstore(
        tmp_path
    )

    raw_documents = retrieve_documents(
        query="password policy",
        persist_directory=vectorstore_path,
    )

    print("\nRAW RESULTS")

    for doc, score in raw_documents:
        print(score, doc.page_content[:100])


    retriever = PolicyRetriever(
        persist_directory=vectorstore_path,
    )

    documents = retriever.invoke(
        "password policy"
    )

    assert len(documents) > 0

def test_policy_retriever_metadata_values(
    tmp_path,
):

    vectorstore_path = create_test_vectorstore(
        tmp_path
    )

    retriever = PolicyRetriever(
        persist_directory=vectorstore_path,
    )


    documents = retriever.invoke(
        "password policy"
    )


    metadata = documents[0].metadata
    
    print("\nMETADATA:")
    for key, value in metadata.items():
        print(f"- {key}: {value}")
    
    assert metadata["retrieval_status"] == (
        RetrievalStatus.FOUND.value
    )


    assert metadata["evidence_confidence"] == (
        EvidenceConfidence.HIGH.value
    )
    assert isinstance(
        metadata["retrieval_score"],
        float,
    )