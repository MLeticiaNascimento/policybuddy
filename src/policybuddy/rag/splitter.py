from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

HEADERS_TO_SPLIT_ON = [
    ("#", "title"),
    ("##", "section"),
    ("###", "subsection"),
]


def _split_by_headers(documents: list[Document]) -> list[Document]:
    """
    Split Markdown documents into logical sections based on headers.
    """

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )

    sections = []

    for document in documents:
        docs = splitter.split_text(document.page_content)

        for doc in docs:
            doc.metadata.update(document.metadata)

        sections.extend(docs)

    return sections


def _split_large_sections(sections: list[Document]) -> list[Document]:
    """
    Split oversized sections into smaller chunks while preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )

    return splitter.split_documents(sections)


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Complete splitting pipeline.

    1. Split by Markdown headers.
    2. Split oversized sections into chunks.
    """

    sections = _split_by_headers(documents)

    chunks = _split_large_sections(sections)
    print(chunks)
    return chunks
