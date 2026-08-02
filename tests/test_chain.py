from unittest.mock import MagicMock, patch

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from policybuddy.llm.chains import (
    create_rag_chain,
    format_documents,
    load_prompt,
)


def test_load_prompt():

    prompt = load_prompt(
        "system_prompt.txt"
    )

    assert isinstance(
        prompt,
        str,
    )

    assert len(prompt) > 0



def test_format_documents():

    documents = [
        Document(
            page_content="Data protection policy"
        ),
        Document(
            page_content="Access control policy"
        ),
    ]

    result = format_documents(
        documents
    )

    assert result == (
        "Data protection policy\n\n"
        "Access control policy"
    )



@patch(
    "policybuddy.llm.chains.create_retriever"
)
@patch(
    "policybuddy.llm.chains.create_llm"
)
def test_create_rag_chain(
    mock_create_llm,
    mock_create_retriever,
):

    mock_create_retriever.return_value = (
        MagicMock()
    )

    mock_create_llm.return_value = (
        RunnableLambda(
            lambda _: AIMessage(
                content="Test answer"
            )
        )
    )


    chain = create_rag_chain()


    assert chain is not None




@patch(
    "policybuddy.llm.chains.create_llm"
)
def test_rag_chain_execution(
    mock_create_llm,
):

    #
    # Mock LLM
    #

    llm = RunnableLambda(
        lambda _: AIMessage(
            content=(
                "Confidential information "
                "must be protected."
            )
        )
    )

    mock_create_llm.return_value = llm


    #
    # Create chain
    #

    chain = create_rag_chain()


    #
    # Execute
    #

    response = chain.invoke(
        {
            "question": (
                "Can I share confidential data?"
            ),
            "context": (
                "Employees must protect "
                "confidential information."
            ),
        }
    )


    #
    # Evidence
    #

    print("\n===== CHAIN RESPONSE =====")

    print(
        response.content
    )


    #
    # Assertions
    #

    assert response.content == (
        "Confidential information "
        "must be protected."
    )