from langchain_huggingface import HuggingFaceEmbeddings

from policybuddy.rag.embeddings import create_embeddings


def test_create_embeddings_returns_model():

    embeddings = create_embeddings()

    assert isinstance(embeddings, HuggingFaceEmbeddings)


def test_embeddings_generate_vector():

    embeddings = create_embeddings()

    vector = embeddings.embed_query("data privacy policy")

    assert len(vector) > 0
