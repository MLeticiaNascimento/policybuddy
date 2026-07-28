from policybuddy.rag.loader import load_documents
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import create_vector_store


if __name__ == "__main__":

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    create_vector_store(
        chunks
    )

    print("Vector store created successfully!")