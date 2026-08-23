import json
import os

from extractor import extract_text
from cleaner import clean_text
from chunker import create_chunks


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "processed_documents.json")
SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def process_document(file_path):
    print(f"\nProcessing: {os.path.basename(file_path)}")

    raw_text = extract_text(file_path)
    print("  [1/3] Text extracted successfully.")

    cleaned_text = clean_text(raw_text)
    print("  [2/3] Text cleaned successfully.")

    chunks = create_chunks(cleaned_text)
    print(f"  [3/3] Created {len(chunks)} chunks.")

    return chunks


def process_all_documents():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    documents = []

    for filename in sorted(os.listdir(INPUT_FOLDER)):
        file_path = os.path.join(INPUT_FOLDER, filename)
        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()
        if extension not in SUPPORTED_EXTENSIONS:
            print(f"Skipping unsupported file: {filename}")
            continue

        try:
            chunks = process_document(file_path)
            for index, chunk in enumerate(chunks):
                documents.append({
                    "document": filename,
                    "chunk_id": index,
                    "text": chunk
                })
        except Exception as error:
            print(f"  ERROR processing {filename}: {error}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file, indent=4, ensure_ascii=False)

    print("\nProcessing completed.")
    print(f"Total chunks: {len(documents)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    process_all_documents()
