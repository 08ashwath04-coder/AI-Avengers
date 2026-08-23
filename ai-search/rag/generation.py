from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

class AnswerGenerator:
    def __init__(self):
        if not GEMINI_API_KEY or GEMINI_API_KEY.strip() in [
            "",
            "YOUR_GEMINI_API_KEY",
            "YOUR_REAL_GEMINI_API_KEY",
        ]:
            raise ValueError(
                "GEMINI_API_KEY is missing or unconfigured. "
                "Please add your valid GEMINI_API_KEY to the .env file."
            )

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, question: str, retrieved_chunks: list) -> dict:
        """
        Generates an answer to the question using ONLY the retrieved context.
        """
        if not retrieved_chunks:
            return {
                "answer": "The information could not be found in the provided documents.",
                "sources": [],
                "retrieved_chunks": [],
            }

        context_parts = []
        sources = []

        for item in retrieved_chunks:
            metadata = item.get("metadata", {})
            source = metadata.get("source", "Unknown")
            text = metadata.get("text", "")

            context_parts.append(f"SOURCE: {source}\nCONTENT:\n{text}")

            if source not in sources:
                sources.append(source)

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""You are a knowledge assistant for Second Brain AI.
Answer the user's question using ONLY the provided context.
Do not use outside knowledge.
Do not invent information.
If the answer is not present in the provided context, say that the information could not be found in the provided documents.

USER QUESTION:
{question}

CONTEXT:
{context}

ANSWER:"""

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            answer = response.text.strip() if response.text else "The information could not be found in the provided documents."
        except Exception as err:
            raise RuntimeError(f"Gemini API Error: {str(err)}") from err

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": [
                item["metadata"] for item in retrieved_chunks if "metadata" in item
            ],
        }