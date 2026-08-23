# Second Brain AI - AI Search

Member 3 module for the AI-Avengers project.

## Stack
- Python
- Sentence Transformers
- FAISS
- Gemini
- FastAPI

## Setup
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key.

## Build index
```powershell
python build_index.py
```

## Run CLI
```powershell
python main.py
```

## Run API
```powershell
uvicorn api:app --reload --port 8000
```

POST endpoint:
`http://localhost:8000/ask`

Request:
```json
{"question":"What is the attendance requirement?"}
```

`data/sample_documents.txt` is temporary test data. Later it should be replaced by output from the `document-processing` module.
