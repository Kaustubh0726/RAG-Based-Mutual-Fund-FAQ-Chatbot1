# RAG: build index, retrieve, format answer with one citation (Chroma + sentence-transformers only)
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_DIR,
    EMBEDDING_MODEL,
    TOP_K,
    LAST_UPDATED_PREFIX,
    SOURCES_NOTE,
)
from corpus_loader import get_documents_for_retrieval


def get_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL)


def build_and_persist_index(force_rebuild: bool = False):
    """Load corpus, embed, persist to Chroma. Returns (client, collection, model)."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    model = get_embedding_model()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    collection_name = "groww_mf_faq"
    if force_rebuild and collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(collection_name)
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    docs = get_documents_for_retrieval()
    if not docs:
        return client, collection, model
    # Check if already populated (idempotent)
    existing = collection.count()
    if existing == 0:
        ids = [f"doc_{i}" for i in range(len(docs))]
        texts = [d[0] for d in docs]
        metas = [{"source_url": d[1], "source_file": d[2]} for d in docs]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        collection.add(ids=ids, documents=texts, metadatas=metas, embeddings=embeddings)
    return client, collection, model


def _first_sentences(text: str, max_sentences: int = 3) -> str:
    """Keep up to max_sentences sentences."""
    text = text.replace("\n", " ").strip()
    sentences = []
    for s in text.split(". "):
        s = s.strip()
        if s and "Source:" not in s[:20]:
            sentences.append(s + "." if not s.endswith(".") else s)
            if len(sentences) >= max_sentences:
                break
    return " ".join(sentences) if sentences else (text[:400].rsplit(". ", 1)[0] + "." if ". " in text[:400] else text[:400])


def answer_factual_query(question: str, collection=None, model=None) -> Tuple[str, str]:
    """
    Run retrieval and return (answer_text, citation_url).
    Answer is ≤3 sentences; includes "Last updated from sources: ...".
    """
    if collection is None or model is None:
        _, collection, model = build_and_persist_index()
    q_emb = model.encode([question], show_progress_bar=False).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=min(TOP_K, collection.count()), include=["documents", "metadatas"])
    if not results or not results["documents"] or not results["documents"][0]:
        return (
            "We couldn't find a specific answer in our FAQ corpus. Please check the scheme's official factsheet or AMC website.",
            "https://groww.in/mutual-funds/amc/groww-mutual-funds",
        )
    best_doc = results["documents"][0][0]
    best_meta = results["metadatas"][0][0] if results["metadatas"] and results["metadatas"][0] else {}
    source_url = (best_meta.get("source_url") or "").strip()
    if not source_url and results["metadatas"] and results["metadatas"][0] and len(results["metadatas"][0]) > 1:
        source_url = results["metadatas"][0][1].get("source_url", "")
    if not source_url:
        source_url = "https://www.amfiindia.com/investor-corner/faqs"
    answer = _first_sentences(best_doc, max_sentences=3)
    answer = answer + " " + LAST_UPDATED_PREFIX + SOURCES_NOTE
    return answer, source_url


# Lazy singleton for the app
_client, _collection, _model = None, None, None


def get_app_store():
    global _client, _collection, _model
    if _collection is None:
        _client, _collection, _model = build_and_persist_index()
    return _collection, _model
