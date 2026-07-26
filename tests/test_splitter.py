from pathlib import Path

from langchain_core.documents import Document

from policybuddy.rag.loader import load_documents
from policybuddy.rag.splitter import split_documents


def test_split_documents_creates_chunks():

    documents = load_documents()

    chunks = split_documents(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    assert len(documents) > 0
    assert len(chunks) > 0


def test_split_documents_returns_documents():

    documents = load_documents()

    chunks = split_documents(documents)

    assert all(isinstance(chunk, Document) for chunk in chunks)


def test_split_documents_preserves_content():

    documents = load_documents(Path("docs/policies"))

    chunks = split_documents(documents)

    assert all(chunk.page_content.strip() for chunk in chunks)


def test_split_documents_preserves_metadata():

    documents = load_documents()

    chunks = split_documents(documents)

    for chunk in chunks:
        assert chunk.metadata is not None
