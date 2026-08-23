from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from rag.pipeline import RAGPipeline

app = FastAPI(
    title="Second Brain AI Search API",
    description="AI Search & RAG Module for Second Brain AI (Member 3)",
    version="1.0.0"
)

pipeline: Optional[RAGPipeline] = None
pipeline_error: Optional[str] = None

class QuestionRequest(BaseModel):
    question: str

class ChunkMetadata(BaseModel):
    chunk_id: int
    source: str
    text: str

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]
    retrieved_chunks: List[Dict[str, Any]]

@app.on_event("startup")
def startup_event():
    global pipeline, pipeline_error
    print("Initializing RAG pipeline for FastAPI...")
    try:
        pipeline = RAGPipeline()
        pipeline_error = None
        print("AI Search API is fully initialized and ready!")
    except Exception as err:
        pipeline = None
        pipeline_error = str(err)
        print(f"Warning: RAG Pipeline failed to load during startup: {err}")

@app.get("/")
def root():
    return {
        "status": "online" if pipeline else "degraded",
        "service": "Second Brain AI Search",
        "module": "Member 3",
        "ready": pipeline is not None,
        "error": pipeline_error
    }

@app.get("/health")
def health():
    if pipeline is None and pipeline_error:
        return {"status": "degraded", "error": pipeline_error}
    return {"status": "healthy"}

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    global pipeline
    if pipeline is None:
        # Try initializing on request if startup failed previously
        try:
            pipeline = RAGPipeline()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"RAG Pipeline unavailable: {str(err)}"
            )

    question_text = request.question.strip() if request.question else ""
    if not question_text:
        return {
            "answer": "Please enter a valid question.",
            "sources": [],
            "retrieved_chunks": []
        }

    try:
        return pipeline.ask(question_text)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating answer: {str(err)}"
        )

