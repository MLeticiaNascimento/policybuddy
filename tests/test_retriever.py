from langchain_core.documents import Document

from policybuddy.rag.loader import load_documents
from policybuddy.rag.retriever import retrieve_documents
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import create_vector_store


def test_retrieve_documents_returns_list(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    results = retrieve_documents(
        query="password policy",
        persist_directory=vectorstore_path,
    )

    assert isinstance(results, list)


def test_retrieve_documents_returns_document_and_score(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    results = retrieve_documents(
        query="password policy",
        persist_directory=vectorstore_path,
    )

    assert len(results) > 0

    document, score = results[0]

    assert isinstance(document, Document)
    assert isinstance(score, float)


def test_retrieve_documents_respects_k(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    results = retrieve_documents(
        query="password policy",
        persist_directory=vectorstore_path,
        k=2,
    )

    assert len(results) == 2


def test_retrieve_documents_returns_relevant_content(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    results = retrieve_documents(
        query="password",
        persist_directory=vectorstore_path,
        k=3,
    )

    text = " ".join(document.page_content.lower() for document, _ in results)

    assert "password" in text
