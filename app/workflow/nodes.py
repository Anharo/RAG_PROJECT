from app.retrieval.retriever import retrieve_chunks
from app.llm.generator import generate_answer


# 🔹 Intent detection (simple for now)
def detect_intent(state):
    query = state["query"].lower()

    if "complaint" in query or "not working" in query:
        return {**state, "intent": "ESCALATE"}

    return {**state, "intent": "FAQ"}


# 🔹 Retrieval node
def retrieve_node(state):
    chunks = retrieve_chunks(state["query"])
    return {**state, "chunks": chunks}


# 🔹 LLM generation
def generate_node(state):
    answer = generate_answer(state["query"], state["chunks"])

    # simple confidence logic
    escalate = "couldn't find" in answer.lower()

    return {
        **state,
        "answer": answer,
        "escalate": escalate
    }


# 🔹 HITL node
def hitl_node(state):
    return {
        **state,
        "answer": "Your query has been escalated to a human agent."
    }