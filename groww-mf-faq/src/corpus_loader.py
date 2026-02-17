# Load corpus and extract chunks with source URLs (no langchain)
import re
from pathlib import Path
from typing import List, Tuple

from config import CORPUS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def _extract_source_from_text(text: str) -> str | None:
    """Extract 'Source: https://...' from text."""
    m = re.search(r"Source:\s*(https?://[^\s\n\)]+)", text, re.IGNORECASE)
    return (m.group(1).strip().rstrip(")") if m else None)


def _split_text(text: str) -> List[str]:
    """Split text into chunks by size."""
    chunks = []
    for sep in ["\n\n", "\n", ". ", " "]:
        parts = text.split(sep)
        current = ""
        for p in parts:
            if len(current) + len(p) + len(sep) <= CHUNK_SIZE:
                current += (sep if current else "") + p
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = p
        if current.strip():
            chunks.append(current.strip())
        if chunks:
            break
    if not chunks:
        chunks = [text[:CHUNK_SIZE]] if text else []
    return [c for c in chunks if len(c) >= 20]


def load_and_chunk_corpus() -> List[Tuple[str, str, str]]:
    """
    Load all .md from corpus. Returns list of (content, source_url, source_file).
    """
    result: List[Tuple[str, str, str]] = []
    for path in sorted(CORPUS_DIR.glob("**/*.md")):
        text = path.read_text(encoding="utf-8")
        blocks = [b.strip() for b in text.split("\n\n") if b.strip() and len(b.strip()) >= 25]
        last_url = ""
        for block in blocks:
            source_url = _extract_source_from_text(block) or last_url
            if source_url:
                last_url = source_url
            content = re.sub(r"\n?\s*Source:\s*https?://[^\n]+", "", block, flags=re.IGNORECASE).strip()
            if not content:
                continue
            for chunk_text in _split_text(content):
                if len(chunk_text) < 20:
                    continue
                result.append((chunk_text, source_url or last_url, str(path.name)))
    return result


def get_documents_for_retrieval() -> List[Tuple[str, str, str]]:
    """Load corpus and return list of (content, source_url, source_file)."""
    return load_and_chunk_corpus()
