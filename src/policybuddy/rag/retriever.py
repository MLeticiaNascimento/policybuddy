from pathlib import Path

from langchain_core.documents import Document

from policybuddy.rag.store import load_vector_store


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