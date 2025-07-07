import csv
from pathlib import Path
from typing import List

import PyPDF2

from apps.core.config import settings


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extracts text from a PDF file."""

    text = ""
    with pdf_path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_csv(csv_path: Path) -> str:
    """Extracts text from a CSV file by converting it to a readable format."""

    text = ""
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        if headers:
            text += f"CSV Headers: {', '.join(headers)}\n\n"

            for row_num, row in enumerate(reader, 1):
                if len(row) == len(headers):
                    row_text = f"Row {row_num}:\n"
                    for header, value in zip(headers, row):
                        if value.strip():
                            row_text += f"  {header}: {value}\n"
                    text += row_text + "\n"
                else:
                    text += f"Row {row_num}: {', '.join(row)}\n\n"

    return text


def split_text(text: str, chunk_size: int = 2000, overlap: int = 100) -> List[str]:
    """
    Splits text into chunks of roughly `chunk_size` characters with an overlap of `overlap` words between chunks.

    Uses larger chunks and smaller overlap for better efficiency.
    """

    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # add 1 for space
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            # Create overlap for the next chunk
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(w) + 1 for w in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Get embeddings using OpenAI API."""

    response = settings.openai_client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def get_embeddings_rag_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 50,
) -> List[list[float]]:
    """Gets embeddings for a batch of texts."""

    all_embeddings = []

    # Process in batches to avoid rate limits and memory issues
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = settings.openai_client.embeddings.create(input=batch, model=model)
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


def text_to_vector(
    text: str,
    model: str = "text-embedding-3-small",
) -> str:
    """Convert text to PostgreSQL vector format."""

    response = settings.openai_client.embeddings.create(
        model=model,
        input=text,
    )
    embedding = response.data[0].embedding

    return "[" + ",".join(str(x) for x in embedding) + "]"
