import json
import os
import numpy as np

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

class VectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.numpy_index_path = index_path + ".npy"
        self.index = None
        self.embeddings = None
        self.metadata = []

    def build(self, embeddings, metadata):
        embeddings = np.asarray(embeddings, dtype="float32")
        if len(embeddings) == 0:
            raise ValueError("Cannot build index with empty embeddings.")

        self.embeddings = embeddings
        self.metadata = metadata

        os.makedirs(os.path.dirname(os.path.abspath(self.index_path)), exist_ok=True)

        if HAS_FAISS:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            faiss.write_index(self.index, self.index_path)
            print(f"Indexed {len(metadata)} chunks into FAISS vector store.")
        else:
            print(f"Indexed {len(metadata)} chunks into NumPy vector store (FAISS fallback).")

        # Always save numpy array as backup for environments without FAISS
        np.save(self.numpy_index_path, embeddings)

        os.makedirs(os.path.dirname(os.path.abspath(self.metadata_path)), exist_ok=True)
        with open(self.metadata_path, "w", encoding="utf-8") as file:
            json.dump(metadata, file, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(
                f"Metadata file not found at '{self.metadata_path}'. Please run build_index.py first."
            )

        with open(self.metadata_path, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

        if HAS_FAISS and os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        elif os.path.exists(self.numpy_index_path):
            self.embeddings = np.load(self.numpy_index_path)
        elif os.path.exists(self.index_path):
            # In case index was created with FAISS but faiss is not installed in current env
            raise FileNotFoundError(
                "FAISS index file exists, but 'faiss-cpu' package is not installed in your Python environment."
            )
        else:
            raise FileNotFoundError(
                f"Vector index not found at '{self.index_path}'. Please run build_index.py first."
            )

    def search(self, query_embedding, top_k=3):
        if (self.index is None and self.embeddings is None) or not self.metadata:
            self.load()

        query_embedding = np.asarray(query_embedding, dtype="float32")
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)

        results = []

        if HAS_FAISS and self.index is not None:
            actual_k = min(top_k, self.index.ntotal)
            distances, indices = self.index.search(query_embedding, actual_k)
            for distance, index in zip(distances[0], indices[0]):
                if index < 0 or index >= len(self.metadata):
                    continue
                results.append({
                    "index": int(index),
                    "distance": float(distance),
                    "metadata": self.metadata[index],
                })
        elif self.embeddings is not None:
            # NumPy fallback vector search using Euclidean (L2) distance squared
            diffs = self.embeddings - query_embedding[0]
            dists = np.sum(diffs ** 2, axis=1)
            actual_k = min(top_k, len(dists))
            top_indices = np.argsort(dists)[:actual_k]
            for index in top_indices:
                results.append({
                    "index": int(index),
                    "distance": float(dists[index]),
                    "metadata": self.metadata[index],
                })

        return results


