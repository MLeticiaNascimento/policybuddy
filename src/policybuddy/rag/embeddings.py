from langchain_huggingface import HuggingFaceEmbeddings

from policybuddy.config import EMBEDDING_MODEL


def create_embeddings() -> HuggingFaceEmbeddings:
    """
    Create the embedding model used by the application.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )
