from pathlib import Path
import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document

from policybuddy.rag.embeddings import create_embeddings


VECTOR_STORE_PATH = Path("vectorstore")

def create_vector_store(documents: list[Document],persist_directory: Path = VECTOR_STORE_PATH) -> Chroma:
    """
    Create a new Chroma vector store from the provided documents.

    If a vector store already exists, it will be replaced.
    """

    if persist_directory.exists():
        shutil.rmtree(persist_directory)

    return Chroma.from_documents(
        documents=documents,
        embedding=create_embeddings(),
        persist_directory=str(persist_directory),
    )


def load_vector_store(persist_directory: Path = VECTOR_STORE_PATH) -> Chroma:
    """
    Load an existing Chroma vector store.
    """

    return Chroma(
        persist_directory=str(persist_directory),
        embedding_function=create_embeddings(),
    )