from pathlib import Path

from langchain_community.document_loaders import TextLoader


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_DOCS_PATH = PROJECT_ROOT / "docs"


def load_documents(docs_path=DEFAULT_DOCS_PATH):

    documents = []

    docs_path = Path(docs_path)

    print(f"\nPROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DOCS_PATH: {docs_path}")
    print(f"DOCS_PATH EXISTS: {docs_path.exists()}")

    if docs_path.exists():
        print("FILES:")
        for file in docs_path.glob("*.md"):
            print(f" - {file.name}")

    for file_path in docs_path.glob("*.md"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    return documents