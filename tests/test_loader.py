from pathlib import Path

from policybuddy.rag.loader import load_documents


def test_loader():

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    assert len(documents) > 0