from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_DOCS_PATH = PROJECT_ROOT / "docs"


SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
    ".pdf",
}


def load_documents(docs_path=DEFAULT_DOCS_PATH):

    documents = []

    docs_path = Path(docs_path)

    print(f"\nPROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DOCS_PATH: {docs_path}")
    print(f"DOCS_PATH EXISTS: {docs_path.exists()}")

    if not docs_path.exists():
        raise FileNotFoundError(
            f"Documents folder not found: {docs_path}"
        )

    print("\nFILES FOUND:")

    files = [
        file
        for file in docs_path.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    for file in files:
        print(f" - {file.name}")

    print("\nLOADING DOCUMENTS...")

    for file_path in files:

        extension = file_path.suffix.lower()

        if extension == ".pdf":

            loader = PyPDFLoader(
                str(file_path)
            )

        elif extension in [".md", ".txt"]:

            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

        else:
            continue

        loaded_documents = loader.load()

        documents.extend(
            loaded_documents
        )

        print(
            f"Loaded {file_path.name}: "
            f"{len(loaded_documents)} pages/documents"
        )

    print(
        f"\nTOTAL DOCUMENTS LOADED: {len(documents)}"
    )
    print(documents)
    return documents