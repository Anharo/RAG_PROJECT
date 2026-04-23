from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_text
from app.ingestion.embedder import get_embeddings
from app.ingestion.store import store_chunks

from app.workflow.graph import build_graph

router = APIRouter()

UPLOAD_DIR = "data/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    query: str


# 🔹 Lazy graph init
graph = None

def get_graph():
    global graph
    if graph is None:
        graph = build_graph()
    return graph


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    text = load_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    store_chunks(chunks, embeddings)

    return {
        "filename": file.filename,
        "chunks_created": len(chunks),
        "message": "PDF processed and stored in vector DB"
    }


@router.get("/test-retrieval")
def test_retrieval(q: str):
    from app.retrieval.retriever import retrieve_chunks
    return {"results": retrieve_chunks(q)}


@router.post("/query")
def query_system(payload: QueryRequest):
    state = {
        "query": payload.query,
        "intent": "",
        "chunks": [],
        "answer": "",
        "escalate": False
    }

    result = get_graph().invoke(state)

    chunks = result.get("chunks") or []

    return {
        "query": payload.query,
        "answer": result.get("answer"),
        "chunks_used": [c.get("text") for c in chunks],
        "distances": [c.get("score") for c in chunks],
        "intent": result.get("intent"),
        "escalated": result.get("escalate")
    }