from pathlib import Path
from langchain.document_loaders import TextLoader

from langchain_community.document_loaders import TextLoader


DOCS_PATH = Path("docs")


def load_policies():
    documents = []

    for file_path in DOCS_PATH.rglob("*.md"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        docs = loader.load()

        documents.extend(docs)

    return documents