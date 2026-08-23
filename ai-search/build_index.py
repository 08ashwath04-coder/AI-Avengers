import os
from config import DATA_FILE, INDEX_FILE, METADATA_FILE, CHUNK_SIZE, CHUNK_OVERLAP
from rag.chunking import chunk_text
from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore

def build_index():
    print("=" * 50)
    print("SECOND BRAIN AI - BUILDING KNOWLEDGE INDEX")
    print("=" * 50)

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Source document file not found at: '{DATA_FILE}'")

    print(f"\nReading document from '{DATA_FILE}'...")
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    print("Creating text chunks...")
    chunks = chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"Created {len(chunks)} chunks.")

    metadata = [
        {"chunk_id": i, "source": os.path.basename(DATA_FILE), "text": chunk}
        for i, chunk in enumerate(chunks)
    ]

    print("\nGenerating embeddings...")
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.encode_documents(chunks)

    print("\nBuilding FAISS vector index...")
    vector_store = VectorStore(INDEX_FILE, METADATA_FILE)
    vector_store.build(embeddings, metadata)

    print("\n" + "=" * 50)
    print("INDEX BUILD COMPLETE SUCCESSFUL")
    print("=" * 50)

if __name__ == "__main__":
    build_index()

