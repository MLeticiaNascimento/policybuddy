from typing import NotRequired, TypedDict

from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph

from policybuddy.llm.chains import (
    create_rag_chain,
    format_documents,
)
from policybuddy.rag.retriever import (
    EvidenceConfidence,
    RetrievalStatus,
    create_retriever,
)


class GraphState(TypedDict):
    question: str
    documents: NotRequired[list[Document]]
    context: NotRequired[str]
    retrieval_status: NotRequired[RetrievalStatus]
    evidence_confidence: NotRequired[EvidenceConfidence]
    best_score: NotRequired[float | None]
    answer: NotRequired[str]


def retrieve_context_node(
    state: GraphState,
) -> GraphState:
    """
    Retrieve relevant documents and enrich the graph state.
    """

    retriever = create_retriever()

    documents = retriever.invoke(
        state["question"]
    )
    print(f"Documents found: {len(documents)}")
    context = format_documents(documents)

    metadata = (
        documents[0].metadata
        if documents
        else {}
    )

    return {
        **state,
        "documents": documents,
        "context": context,
        "retrieval_status": metadata.get(
            "retrieval_status",
            RetrievalStatus.EMPTY,
        ),
        "evidence_confidence": metadata.get(
            "evidence_confidence",
            EvidenceConfidence.LOW,
        ),
        "best_score": metadata.get(
            "best_score",
        ),
    }


def generate_answer_node(
    state: GraphState,
) -> GraphState:
    print(f"Generating answer for question: {state['question']}")
    """
    Generate the final answer using the RAG chain.
    """

    chain = create_rag_chain()
  
    print("===== CONTEXT SENT TO LLM =====")
    print(state["context"])
    print("===== END CONTEXT =====")
    print("Calling LLM")
  
    response = chain.invoke(
        {
            "question": state["question"],
            "context": state["context"],
        }
    )
    print("LLM response")

    content = response.content

    if isinstance(content, list):
        content = "\n".join(
            item["text"]
            for item in content
            if item.get("type") == "text"
        )

    return {
        **state,
        "answer": content,
    }
    
def build_graph():
    print("Building graph")
    """
    Build PolicyBuddy LangGraph workflow.

    Flow:

    START
      |
      v
    retrieve_context_node
      |
      v
    generate_answer_node
      |
      v
    END
    """

    workflow = StateGraph(
        GraphState
    )

    #
    # Add nodes
    #

    workflow.add_node(
        "retrieve_context",
        retrieve_context_node,
    )

    workflow.add_node(
        "generate_answer",
        generate_answer_node,
    )


    #
    # Define edges
    #

    workflow.add_edge(
        START,
        "retrieve_context",
    )

    workflow.add_edge(
        "retrieve_context",
        "generate_answer",
    )

    workflow.add_edge(
        "generate_answer",
        END,
    )


    return workflow.compile()

