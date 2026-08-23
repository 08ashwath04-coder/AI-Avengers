from config import INDEX_FILE, METADATA_FILE, TOP_K
from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from rag.retrieval import Retriever
from rag.generation import AnswerGenerator

class RAGPipeline:
    def __init__(self):
        print("Initializing RAG pipeline...")
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(INDEX_FILE, METADATA_FILE)
        self.vector_store.load()
        self.retriever = Retriever(self.embedding_model, self.vector_store)
        self.generator = AnswerGenerator()
        print("RAG pipeline ready!")

    def ask(self, question: str):
        if not question or not question.strip():
            return {
                "answer": "Please enter a valid question.",
                "sources": [],
                "retrieved_chunks": []
            }

        question = question.strip()
        retrieved_chunks = self.retriever.search(question, top_k=TOP_K)
        return self.generator.generate(question, retrieved_chunks)

