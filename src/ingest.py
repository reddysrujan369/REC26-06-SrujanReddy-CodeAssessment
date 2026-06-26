import os
import pickle
import faiss
import numpy as np

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

CORPUS_DIR = "data/corpus"
INDEX_DIR = "index"

CHUNK_SIZE = 500
OVERLAP = 100


def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page_num, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text:

            text += f"\n\n[PAGE {page_num + 1}]\n\n"
            text += page_text

    return text


def chunk_text(text):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += CHUNK_SIZE - OVERLAP

    return chunks


def main():

    os.makedirs(INDEX_DIR, exist_ok=True)

    all_chunks = []
    metadata = []

    for filename in os.listdir(CORPUS_DIR):

        if not filename.endswith(".pdf"):
            continue

        print(f"Processing: {filename}")

        path = os.path.join(CORPUS_DIR, filename)

        text = extract_pdf_text(path)

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            enriched_chunk = f"""
DOCUMENT: {filename}

{chunk}
"""

            all_chunks.append(enriched_chunk)

            metadata.append(
                {
                    "doc": filename,
                    "chunk_id": i,
                    "text": enriched_chunk
                }
            )

    print("\nGenerating embeddings...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        all_chunks,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    faiss.write_index(
        index,
        "index/faiss.index"
    )

    with open(
        "index/metadata.pkl",
        "wb"
    ) as f:

        pickle.dump(metadata, f)

    with open(
        "index/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(all_chunks, f)

    print("\nDone")
    print("Total chunks:", len(all_chunks))


if __name__ == "__main__":
    main()