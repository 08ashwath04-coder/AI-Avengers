from config import TOP_K, SIMILARITY_THRESHOLD

class Retriever:
    def __init__(self, embedding_model, vector_store, similarity_threshold: float = SIMILARITY_THRESHOLD):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold

    def search(self, question: str, top_k: int = TOP_K):
        """
        Retrieves top_k relevant chunks for a user question and filters out low-similarity chunks.
        """
        if not question or not question.strip():
            return []

        query_embedding = self.embedding_model.encode_query(question)
        results = self.vector_store.search(query_embedding, top_k=top_k)

        filtered_results = []
        for result in results:
            distance = result["distance"]
            # For normalized vectors, L2 distance range is [0, 2].
            # Cosine similarity is 1 - (L2_distance / 2).
            similarity = max(0.0, min(1.0, 1.0 - (distance / 2.0)))
            result["similarity"] = similarity

            if similarity >= self.similarity_threshold:
                filtered_results.append(result)

        return filtered_results

