# Groww MF FAQ – config
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT_DIR / "corpus"
SOURCES_CSV = ROOT_DIR / "sources" / "sources.csv"
CHROMA_DIR = ROOT_DIR / "chroma_db"

# RAG
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 3
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # local, no API key

# Refusal – educational link when we don't give advice (Groww blog)
EDUCATIONAL_LINK = "https://groww.in/blog/mutual-fund-factsheet-key-information-it-holds-and-how-to-read-it"
AMFI_FAQ_LINK = "https://www.amfiindia.com/investor-corner/faqs"

# Disclaimer
LAST_UPDATED_PREFIX = "Last updated from sources: "
SOURCES_NOTE = "February 2026. Check the linked source for current details."
