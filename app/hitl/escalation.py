import json
import os

QUEUE_FILE = "data/hitl_queue.json"

# ensure file exists
if not os.path.exists(QUEUE_FILE):
    with open(QUEUE_FILE, "w") as f:
        json.dump([], f)


def add_to_queue(query):
    with open(QUEUE_FILE, "r") as f:
        data = json.load(f)

    ticket = {
        "id": len(data) + 1,
        "query": query,
        "status": "pending",
        "response": None
    }

    data.append(ticket)

    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return ticket