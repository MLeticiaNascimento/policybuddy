from unittest.mock import MagicMock, patch

from policybuddy.app.pipeline import (
    ask_policybuddy,
)

from policybuddy.service import (
    answer_question,
)

from policybuddy.rag.retriever import (
    RetrievalStatus,
    EvidenceConfidence,
)


def mock_graph_result():

    return {
        "question": (
            "Can I share confidential data?"
        ),
        "context": (
            "Employees must protect "
            "confidential information."
        ),
        "answer": (
            "Confidential information "
            "must be protected."
        ),
        "documents": [],
        "retrieval_status": (
            RetrievalStatus.FOUND
        ),
        "evidence_confidence": (
            EvidenceConfidence.HIGH
        ),
        "best_score": 0.21,
    }


@patch(
    "policybuddy.app.pipeline.build_graph"
)
def test_policybuddy_pipeline_returns_result(
    mock_build_graph,
):

    graph = MagicMock()

    graph.invoke.return_value = (
        mock_graph_result()
    )

    mock_build_graph.return_value = graph


    result = ask_policybuddy(
        "Can I share confidential data?"
    )


    assert "answer" in result

    assert result["answer"]


    graph.invoke.assert_called_once()


@patch(
    "policybuddy.app.pipeline.build_graph"
)
def test_policybuddy_pipeline_contains_context(
    mock_build_graph,
):

    graph = MagicMock()

    graph.invoke.return_value = (
        mock_graph_result()
    )

    mock_build_graph.return_value = graph


    result = ask_policybuddy(
        "Can I share confidential data?"
    )


    assert "context" in result

    assert result["context"]


@patch(
    "policybuddy.app.pipeline.build_graph"
)
def test_policybuddy_pipeline_preserves_retrieval_metadata(
    mock_build_graph,
):

    graph = MagicMock()

    graph.invoke.return_value = (
        mock_graph_result()
    )

    mock_build_graph.return_value = graph


    result = ask_policybuddy(
        "Can I share confidential data?"
    )


    assert (
        result["retrieval_status"]
        == RetrievalStatus.FOUND
    )

    assert (
        result["evidence_confidence"]
        == EvidenceConfidence.HIGH
    )


@patch(
    "policybuddy.app.pipeline.build_graph"
)
def test_policybuddy_pipeline_returns_documents(
    mock_build_graph,
):

    graph = MagicMock()

    graph.invoke.return_value = (
        mock_graph_result()
    )

    mock_build_graph.return_value = graph


    result = ask_policybuddy(
        "Can I share confidential data?"
    )


    assert "documents" in result



@patch(
    "policybuddy.service.ask_policybuddy"
)
def test_service_returns_user_response(
    mock_pipeline,
):

    mock_pipeline.return_value = (
        mock_graph_result()
    )


    result = answer_question(
        "Can I share confidential data?"
    )


    assert result["answer"]

    assert result["confidence"] == (
        EvidenceConfidence.HIGH
    )



@patch(
    "policybuddy.service.ask_policybuddy"
)
def test_service_preserves_confidence(
    mock_pipeline,
):

    mock_pipeline.return_value = (
        mock_graph_result()
    )


    result = answer_question(
        "Can I share confidential data?"
    )


    assert (
        result["confidence"]
        == EvidenceConfidence.HIGH
    )