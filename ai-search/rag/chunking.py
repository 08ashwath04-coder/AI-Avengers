import re
from typing import List

def clean_text(text: str) -> str:
    """
    Cleans unnecessary whitespace and normalizes newlines in text.
    """
    if not text:
        return ""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 80) -> List[str]:
    """
    Splits document text into meaningful chunks respecting paragraph boundaries
    and size constraints.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    paragraphs = cleaned.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if not current_chunk:
            proposed = paragraph
        else:
            proposed = current_chunk + "\n\n" + paragraph

        if len(proposed) <= chunk_size:
            current_chunk = proposed
        else:
            if current_chunk:
                chunks.append(current_chunk)

            if len(paragraph) > chunk_size:
                sub_sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                sub_chunk = ""
                for sentence in sub_sentences:
                    if len(sub_chunk) + len(sentence) + 1 <= chunk_size:
                        sub_chunk = (sub_chunk + " " + sentence).strip()
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        overlap = (
                            sub_chunk[-chunk_overlap:]
                            if len(sub_chunk) >= chunk_overlap
                            else sub_chunk
                        )
                        sub_chunk = (
                            (overlap + " " + sentence).strip()
                            if overlap
                            else sentence
                        )
                current_chunk = sub_chunk
            else:
                overlap = (
                    current_chunk[-chunk_overlap:]
                    if len(current_chunk) >= chunk_overlap
                    else current_chunk
                )
                current_chunk = (
                    (overlap + "\n\n" + paragraph).strip()
                    if overlap
                    else paragraph
                )

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

