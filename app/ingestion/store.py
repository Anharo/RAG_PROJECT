import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="rag_collection")

def store_chunks(chunks, embeddings):
    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )