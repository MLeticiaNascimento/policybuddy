from policybuddy.graph.graph import build_graph

policybuddy_graph = None


def get_graph():

    global policybuddy_graph

    if policybuddy_graph is None:
        policybuddy_graph = build_graph()

    return policybuddy_graph



def ask_policybuddy(
    question: str
) -> dict:

    graph = get_graph()

    return graph.invoke(
        {
            "question": question
        }
    )