from pathlib import Path
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from policybuddy.graph.graph import (
    GraphState,
    build_graph,
    generate_answer_node,
    retrieve_context_node,
)
from policybuddy.rag.loader import load_documents
from policybuddy.rag.retriever import (
    EvidenceConfidence,
    RetrievalStatus,
    create_retriever,
)
from policybuddy.rag.splitter import split_documents
from policybuddy.rag.store import create_vector_store


def test_graph_state_definition():

    state: GraphState = {
        "question": "Can I share confidential data?",
        "documents": [
            Document(
                page_content="Policy"
            )
        ],
        "context": "Policy",
        "retrieval_status": RetrievalStatus.FOUND,
        "evidence_confidence": EvidenceConfidence.HIGH,
        "best_score": 0.52,
        "answer": "No.",
    }

    assert state["question"] == (
        "Can I share confidential data?"
    )

    assert len(
        state["documents"]
    ) == 1

    assert state["retrieval_status"] == (
        RetrievalStatus.FOUND
    )

    assert state["evidence_confidence"] == (
        EvidenceConfidence.HIGH
    )

    assert state["best_score"] == 0.52

    assert state["answer"] == "No."
    
@patch("policybuddy.graph.create_retriever")
def test_retrieve_context_node_updates_state(
    mock_create_retriever,
):

    #
    # Mock document
    #

    document = Document(
        page_content=(
            "Employees must protect "
            "confidential information."
        ),
        metadata={
            "retrieval_status": RetrievalStatus.FOUND,
            "evidence_confidence": EvidenceConfidence.HIGH,
            "best_score": 0.21,
        },
    )

    #
    # Mock retriever
    #

    retriever = MagicMock()

    retriever.invoke.return_value = [
        document
    ]

    mock_create_retriever.return_value = (
        retriever
    )

    #
    # Initial state
    #

    state: GraphState = {
        "question": (
            "Can I share confidential data?"
        )
    }

    #
    # Execute node
    #

    result = retrieve_context_node(
        state
    )

    #
    # Evidence
    #

    print("\n===== GRAPH STATE =====")

    print(
        "Question:",
        result["question"],
    )

    print(
        "Context:",
        result["context"],
    )

    print(
        "Retrieval Status:",
        result["retrieval_status"],
    )

    print(
        "Evidence Confidence:",
        result["evidence_confidence"],
    )

    print(
        "Best Score:",
        result["best_score"],
    )

    print(
        "Documents:",
        len(result["documents"]),
    )

    #
    # Assertions
    #

    retriever.invoke.assert_called_once_with(
        "Can I share confidential data?"
    )

    assert len(
        result["documents"]
    ) == 1

    assert (
        "confidential information"
        in result["context"]
    )

    assert (
        result["retrieval_status"]
        == RetrievalStatus.FOUND
    )

    assert (
        result["evidence_confidence"]
        == EvidenceConfidence.HIGH
    )

    assert (
        result["best_score"]
        == 0.21
    )
 
@patch("policybuddy.graph.create_rag_chain")    
def test_generate_answer_node_updates_state(
    mock_create_rag_chain,
):

    #
    # Mock chain
    #

    chain = MagicMock()

    chain.invoke.return_value = AIMessage(
        content=(
            "Confidential information "
            "must be protected."
        )
    )

    mock_create_rag_chain.return_value = (
        chain
    )


    #
    # Initial state
    #

    state: GraphState = {
        "question": (
            "Can I share confidential data?"
        ),
        "documents": [],
        "context": (
            "Employees must protect "
            "confidential information."
        ),
        "retrieval_status": (
            RetrievalStatus.FOUND
        ),
        "evidence_confidence": (
            EvidenceConfidence.HIGH
        ),
        "best_score": 0.21,
    }


    #
    # Execute
    #

    result = generate_answer_node(
        state
    )


    #
    # Evidence
    #

    print("\n===== GENERATED ANSWER =====")

    print(
        result["answer"]
    )


    #
    # Assertions
    #

    chain.invoke.assert_called_once_with(
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


    assert result["answer"] == (
        "Confidential information "
        "must be protected."
    )

def test_build_graph():
    
    graph = build_graph()

    print("\n===== GRAPH CREATED =====")

    print(graph)

    assert graph is not None

@patch("policybuddy.graph.create_rag_chain")
@patch("policybuddy.graph.create_retriever")
def test_graph_execution(
    mock_create_retriever,
    mock_create_rag_chain,
    tmp_path,
):

    vectorstore_path = create_test_vectorstore(
        tmp_path
    )


    mock_create_retriever.return_value = (
        create_retriever(
            persist_directory=vectorstore_path
        )
    )


    chain = MagicMock()

    chain.invoke.return_value = AIMessage(
        content=(
            "Confidential information "
            "must be protected."
        )
    )

    mock_create_rag_chain.return_value = chain


    graph = build_graph()


    result = graph.invoke(
        {
            "question": (
                "Can I share confidential data?"
            )
        }
    )


    print("\n===== FINAL GRAPH RESULT =====")

    print(
        "Context:",
        result["context"]
    )

    print(
        "Confidence:",
        result["evidence_confidence"]
    )

    print(
        "Answer:",
        result["answer"]
    )


    assert "context" in result

    assert "answer" in result

    assert result["retrieval_status"] == (
        RetrievalStatus.FOUND
    )

    assert result["evidence_confidence"] == (
        EvidenceConfidence.HIGH
    )

    assert result["answer"] == (
        "Confidential information "
        "must be protected."
    )
    
def create_test_vectorstore(tmp_path: Path):

    vectorstore_path = tmp_path / "vectorstore"

    documents = load_documents()

    chunks = split_documents(
        documents
    )

    create_vector_store(
        chunks,
        vectorstore_path,
    )

    return vectorstore_path
