from typing import TypedDict, List, Dict

class GraphState(TypedDict):
    query: str
    intent: str
    chunks: List[Dict]
    answer: str
    escalate: bool