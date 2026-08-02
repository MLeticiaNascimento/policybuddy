from unittest.mock import patch

from langchain_core.documents import Document
from policybuddy.service.service.service import answer_question

from policybuddy.app.models import PolicyBuddyResponse
from policybuddy.rag.retriever import EvidenceConfidence, RetrievalStatus


@patch("policybuddy.service.ask_policybuddy")
def test_answer_question_returns_policybuddy_response(
    mock_ask_policybuddy,
):

    mock_ask_policybuddy.return_value = {

        "answer": (
            "Confidential information "
            "must be protected."
        ),

        "evidence_confidence": (
            EvidenceConfidence.HIGH
        ),

        "retrieval_status": (
            RetrievalStatus.FOUND
        ),

        "best_score": 0.21,

        "documents": [
            Document(
                page_content=(
                    "Employees must protect "
                    "confidential information."
                ),
                metadata={
                    "source": (
                        "information_security_policy.md"
                    )
                },
            )
        ],
    }


    result = answer_question(
        "Can I share confidential data?"
    )


    #
    # Response model validation
    #

    assert isinstance(
        result,
        PolicyBuddyResponse,
    )


    #
    # Main answer
    #

    assert result.answer == (
        "Confidential information "
        "must be protected."
    )


    #
    # Retrieval metadata
    #

    assert result.confidence == (
        EvidenceConfidence.HIGH
    )

    assert result.retrieval_status == (
        RetrievalStatus.FOUND
    )

    assert result.best_score == 0.21


    #
    # Sources
    #

    assert len(
        result.sources
    ) == 1


    assert result.sources[0].content == (
        "Employees must protect "
        "confidential information."
    )


    assert result.sources[0].metadata == {
        "source": (
            "information_security_policy.md"
        )
    }


    mock_ask_policybuddy.assert_called_once_with(
        "Can I share confidential data?"
    )


@patch("policybuddy.service.ask_policybuddy")
def test_answer_question_handles_multiple_sources(
    mock_ask_policybuddy,
):

    mock_ask_policybuddy.return_value = {

        "answer": "Allowed.",

        "evidence_confidence": (
            EvidenceConfidence.MEDIUM
        ),

        "retrieval_status": (
            RetrievalStatus.PARTIAL
        ),

        "best_score": 0.45,

        "documents": [
            Document(
                page_content="Policy A",
                metadata={
                    "page": 1
                },
            ),

            Document(
                page_content="Policy B",
                metadata={
                    "page": 2
                },
            ),
        ],
    }


    result = answer_question(
        "Can I share this information?"
    )


    assert isinstance(
        result,
        PolicyBuddyResponse,
    )


    assert len(
        result.sources
    ) == 2


    assert result.sources[0].content == (
        "Policy A"
    )

    assert result.sources[1].content == (
        "Policy B"
    )


@patch("policybuddy.service.ask_policybuddy")
def test_answer_question_calls_pipeline(
    mock_ask_policybuddy,
):

    mock_ask_policybuddy.return_value = {

        "answer": "Allowed.",

        "evidence_confidence": (
            EvidenceConfidence.HIGH
        ),

        "retrieval_status": (
            RetrievalStatus.FOUND
        ),

        "best_score": 0.10,

        "documents": [],
    }


    answer_question(
        "Can I share data?"
    )


    mock_ask_policybuddy.assert_called_once_with(
        "Can I share data?"
    )