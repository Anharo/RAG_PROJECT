from app.retrieval.retriever import retrieve_chunks
from app.llm.generator import generate_answer
from app.hitl.escalation import add_to_queue

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

    chunks = state["chunks"]

    # 🔥 Better logic
    avg_distance = (
        sum([c["score"] for c in chunks]) / len(chunks)
        if chunks else 999
    )

    escalate = (
        not chunks or
        avg_distance > 1.25 or   # 🔥 key fix
        len(answer.strip()) < 25
    )

    print("DEBUG → avg_distance:", avg_distance)
    print("DEBUG → escalate:", escalate)

    return {
        **state,
        "answer": answer,
        "escalate": escalate
    }

# 🔹 HITL node
def hitl_node(state):
    ticket = add_to_queue(state["query"])

    return {
        **state,
        "answer": f"Your query has been escalated to a human agent. Ticket ID: {ticket['id']}",
        "escalate": True
    }