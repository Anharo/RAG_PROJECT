from langgraph.graph import StateGraph, END
from app.workflow.state import GraphState
from app.workflow.nodes import detect_intent, retrieve_node, generate_node, hitl_node


def build_graph():
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("intent", detect_intent)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_node("hitl", hitl_node)

    # Flow
    graph.set_entry_point("intent")

    graph.add_conditional_edges(
    "intent",
    lambda state: "hitl" if state["intent"] == "ESCALATE" else "retrieve"
)
    graph.add_edge("retrieve", "generate")

    # Conditional routing
    graph.add_conditional_edges(
        "generate",
        lambda state: "hitl" if state["escalate"] else END
    )

    graph.add_edge("hitl", END)

    return graph.compile()