from pathlib import Path
import shutil

from langchain_chroma import Chroma

from policybuddy.rag.loader import load_documents
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import (
    VECTOR_STORE_PATH,
    create_vector_store,
    load_vector_store,
)


def teardown_module():
    if VECTOR_STORE_PATH.exists():
        shutil.rmtree(VECTOR_STORE_PATH)


def test_create_vector_store_returns_chroma(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    print(f"\nDocuments: {len(documents)}")
    assert len(documents) > 0

    chunks = split_documents(documents)
    print(f"Chunks: {len(chunks)}")
    assert len(chunks) > 0

    vector_store = create_vector_store(
        chunks,
        vectorstore_path,
    )

    assert isinstance(vector_store, Chroma)

def test_create_vector_store_creates_directory(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    assert vectorstore_path.exists()
    assert vectorstore_path.is_dir()


def test_load_vector_store_returns_chroma(tmp_path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()
    chunks = split_documents(documents)

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    vector_store = load_vector_store(
        vectorstore_path,
    )

    assert isinstance(vector_store, Chroma)