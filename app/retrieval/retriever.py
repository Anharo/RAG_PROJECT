from app.ingestion.embedder import get_embeddings
from app.ingestion.store import collection


def retrieve_chunks(query: str, top_k: int = 8):
    # Step 1: Embed query
    query_embedding = get_embeddings([query])[0]

    # Step 2: Query vector DB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # Step 3: Attach scores
    retrieved = []
    for doc, dist in zip(documents, distances):
        retrieved.append({
            "text": doc,
            "score": dist  # higher = better
        })

    # Step 4: Filter weak matches
    filtered = [r for r in retrieved if r["score"] > 0.1]
    print("RAW RESULTS:", retrieved)
    # Step 5: Fallback
    if not filtered:
        return []

    return filtered