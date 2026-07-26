from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from policybuddy.llm.providers import create_llm
from policybuddy.rag.retriever import create_retriever


PROMPTS_PATH = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load prompt templates from txt files.
    """

    prompt_file = PROMPTS_PATH / filename

    return prompt_file.read_text(
        encoding="utf-8"
    )


def format_documents(documents):
    """
    Convert retrieved documents into context string.
    """

    return "\n\n".join(
        document.page_content
        for document in documents
    )

def create_rag_chain():
    """
    Create the RAG generation chain.

    Expected input:

    {
        "question": "...",
        "context": "..."
    }
    """

    llm = create_llm()

    system_prompt = load_prompt(
        "system_prompt.txt"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            (
                "human",
                """
Context:

{context}


Question:

{question}
""",
            ),
        ]
    )

    chain = (
        prompt
        | llm
    )

    return chain

   