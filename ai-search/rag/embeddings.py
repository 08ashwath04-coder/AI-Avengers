import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingModel:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"Loading embedding model ({model_name})...")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")

    def encode_documents(self, texts: List[str]) -> np.ndarray:
        """
        Encodes a list of document chunks into normalized embedding vectors.
        """
        if not texts:
            return np.empty((0, self.model.get_sentence_embedding_dimension()), dtype="float32")
            
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return np.asarray(embeddings, dtype="float32")

    def encode_query(self, question: Union[str, List[str]]) -> np.ndarray:
        """
        Encodes a single user question (or list of queries) into a normalized embedding vector.
        """
        if isinstance(question, str):
            question = [question]
            
        embeddings = self.model.encode(
            question,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return np.asarray(embeddings, dtype="float32")

