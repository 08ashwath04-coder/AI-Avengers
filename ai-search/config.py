import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.35
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

DATA_FILE = "data/sample_documents.txt"
INDEX_FILE = "index/faiss.index"
METADATA_FILE = "index/metadata.json"
