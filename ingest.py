from policybuddy.rag.loader import load_documents
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import create_vector_store


def main():

    print("Loading documents...")

    documents = load_documents()

    print(
        f"Documents loaded: {len(documents)}"
    )

    print("Splitting documents...")

    chunks = split_documents(
        documents
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    print("Creating vector store...")

    create_vector_store(
        chunks
    )

    print(
        "Vector store created successfully!"
    )


if __name__ == "__main__":
    main()