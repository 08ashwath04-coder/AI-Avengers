import os
import re
import json

from config import DATA_FILE, INDEX_FILE, METADATA_FILE, TOP_K

UPLOADED_DATA_FILE = os.path.join(os.path.dirname(DATA_FILE), "uploaded_documents.json")
SUMMARY_TERMS = {"summarize", "summary", "summarise", "document", "file", "about"}
IGNORED_WORDS = {"a", "an", "and", "are", "ask", "about", "could", "do", "file", "for", "give", "how", "i", "in", "is", "me", "of", "please", "the", "this", "to", "what", "who", "with"}

try:
    from rag.embeddings import EmbeddingModel
    from rag.vector_store import VectorStore
    from rag.retrieval import Retriever
    from rag.generation import AnswerGenerator
    FULL_RAG_AVAILABLE = True
except ImportError as error:
    FULL_RAG_AVAILABLE = False
    RAG_IMPORT_ERROR = str(error)

class RAGPipeline:
    def __init__(self):
        print("Initializing RAG pipeline...")
        self.fallback_chunks = []
        self.fallback_records = []
        self.uploaded_data_mtime = None

        if not FULL_RAG_AVAILABLE:
            self._load_fallback_documents()
            print(f"Using document-search fallback because ML dependencies are unavailable: {RAG_IMPORT_ERROR}")
            return

        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(INDEX_FILE, METADATA_FILE)
        self.vector_store.load()
        self.retriever = Retriever(self.embedding_model, self.vector_store)
        self.generator = AnswerGenerator()
        self._refresh_uploaded_index()
        print("RAG pipeline ready!")

    def _load_fallback_documents(self):
        self.fallback_records = []
        if os.path.exists(UPLOADED_DATA_FILE):
            with open(UPLOADED_DATA_FILE, "r", encoding="utf-8") as file:
                self.fallback_records = json.load(file)
        if self.fallback_records:
            self.fallback_chunks = [record.get("text", "") for record in self.fallback_records]
            return

        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError(f"Source document file not found at '{DATA_FILE}'.")
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            text = file.read().strip()

        paragraphs = [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]
        current_chunk = ""
        self.fallback_chunks = []
        for paragraph in paragraphs:
            is_heading = paragraph == paragraph.upper() and any(char.isalpha() for char in paragraph)
            if is_heading and current_chunk:
                self.fallback_chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                current_chunk = f"{current_chunk}\n\n{paragraph}".strip()
        if current_chunk:
            self.fallback_chunks.append(current_chunk)
        self.fallback_records = [
            {"chunk_id": index, "source": os.path.basename(DATA_FILE), "text": chunk}
            for index, chunk in enumerate(self.fallback_chunks)
        ]

    def _refresh_uploaded_index(self):
        if not os.path.exists(UPLOADED_DATA_FILE):
            return
        modified = os.path.getmtime(UPLOADED_DATA_FILE)
        if modified == self.uploaded_data_mtime:
            return
        with open(UPLOADED_DATA_FILE, "r", encoding="utf-8") as file:
            records = [record for record in json.load(file) if record.get("text")]
        if not records:
            return
        metadata = [{"chunk_id": index, **record} for index, record in enumerate(records)]
        self.vector_store.build(self.embedding_model.encode_documents([item["text"] for item in metadata]), metadata)
        self.uploaded_data_mtime = modified

    def _summary(self):
        unique_sources = []
        excerpts = []
        for record in self.fallback_records:
            source = record.get("source", "uploaded document")
            if source not in unique_sources:
                unique_sources.append(source)
            text = record.get("text", "")
            if text and len(excerpts) < 5:
                excerpts.append(text)
        if not excerpts:
            return "The information is not available in the provided documents.", []
        summary = " ".join(excerpts)
        if len(summary) > 1200:
            summary = summary[:1200].rsplit(" ", 1)[0] + "…"
        return summary, unique_sources

    def _spreadsheet_answer(self, question_words):
        rows = [record for record in self.fallback_records if isinstance(record.get("row"), dict)]
        if not rows:
            return None
        if {"many", "records"}.issubset(question_words):
            return f"There are {len(rows)} records in the uploaded spreadsheet.", rows[0]
        header_words = [
            key for row in rows for key in row["row"]
            if any(word in key.lower() for word in question_words) and key.lower() != "name"
        ]
        requested_column = header_words[0] if header_words else None
        if not requested_column:
            return None
        matching_key = requested_column
        if "highest" in question_words or "maximum" in question_words:
            numeric_rows = []
            for row in rows:
                try:
                    numeric_rows.append((float(str(row["row"].get(matching_key, "")).replace("%", "")), row))
                except ValueError:
                    continue
            if numeric_rows:
                _, best = max(numeric_rows, key=lambda item: item[0])
                name = next((value for key, value in best["row"].items() if key.lower() == "name"), "The record")
                return f"{name} has the highest {matching_key}: {best['row'][matching_key]}.", best
        for row in rows:
            values = " ".join(str(value).lower() for value in row["row"].values())
            if any(word in values for word in question_words):
                name = next((value for key, value in row["row"].items() if key.lower() == "name"), "The record")
                return f"{name}'s {matching_key} is {row['row'].get(matching_key, '')}.", row
        return None

    def _ask_with_fallback(self, question: str):
        self._load_fallback_documents()
        question_words = {
            word for word in re.findall(r"[a-z0-9]+", question.lower())
            if len(word) > 1 and word not in IGNORED_WORDS
        }
        if question_words.intersection(SUMMARY_TERMS):
            answer, sources = self._summary()
            records = [record for record in self.fallback_records if record.get("source") in sources]
            return {"answer": answer, "sources": sources, "retrieved_chunks": records[:3]}

        spreadsheet_answer = self._spreadsheet_answer(question_words)
        if spreadsheet_answer:
            answer, record = spreadsheet_answer
            return {"answer": answer, "sources": [record["source"]], "retrieved_chunks": [record]}

        ranked_chunks = sorted(
            self.fallback_records,
            key=lambda record: len(question_words.intersection(re.findall(r"[a-z0-9]+", record.get("text", "").lower()))),
            reverse=True,
        )
        best_record = ranked_chunks[0] if ranked_chunks else {}
        best_chunk = best_record.get("text", "")

        if not best_chunk or not question_words.intersection(re.findall(r"[a-z0-9]+", best_chunk.lower())):
            return {
                "answer": "The information could not be found in the provided documents.",
                "sources": [],
                "retrieved_chunks": [],
            }

        return {
            "answer": best_chunk,
            "sources": [best_record["source"]],
            "retrieved_chunks": [best_record],
        }

    def ask(self, question: str):
        if not question or not question.strip():
            return {
                "answer": "Please enter a valid question.",
                "sources": [],
                "retrieved_chunks": []
            }

        question = question.strip()
        if not FULL_RAG_AVAILABLE:
            return self._ask_with_fallback(question)

        self._refresh_uploaded_index()
        retrieved_chunks = self.retriever.search(question, top_k=TOP_K)
        return self.generator.generate(question, retrieved_chunks)

