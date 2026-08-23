import os
from pypdf import PdfReader
from docx import Document


def extract_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_from_docx(file_path):
    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".txt":
        return extract_from_txt(file_path)
    if extension == ".pdf":
        return extract_from_pdf(file_path)
    if extension == ".docx":
        return extract_from_docx(file_path)
    raise ValueError(f"Unsupported file type: {extension}")
