import os
import pickle
import faiss
import numpy as np

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import google.generativeai as genai

# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

print("Gemini API Key Loaded Successfully")

# -------------------------
# Gemini Setup
# -------------------------

genai.configure(api_key=API_KEY)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Quick API Test

try:
    test_response = llm.generate_content(
        "Hello"
    )
    print("Gemini Connection Successful")
except Exception as e:
    print("Gemini Error:", e)
    exit()

# -------------------------
# Load Embedding Model
# -------------------------

print("Loading Embedding Model...")

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -------------------------
# Load FAISS Index
# -------------------------

print("Loading FAISS Index...")

index = faiss.read_index(
    "index/faiss.index"
)

with open(
    "index/metadata.pkl",
    "rb"
) as f:
    metadata = pickle.load(f)

with open(
    "index/chunks.pkl",
    "rb"
) as f:
    all_chunks = pickle.load(f)

print(f"Loaded {len(all_chunks)} chunks")

# -------------------------
# BM25 Setup
# -------------------------

tokenized_chunks = [
    chunk.split()
    for chunk in all_chunks
]

bm25 = BM25Okapi(
    tokenized_chunks
)

# -------------------------
# Hybrid Retrieval
# -------------------------

def retrieve(question, k=5):

    query_embedding = embed_model.encode(
        [question],
        normalize_embeddings=True
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    semantic_scores, semantic_ids = index.search(
        query_embedding,
        20
    )

    bm25_scores = bm25.get_scores(
        question.split()
    )

    combined_scores = {}

    for score, idx in zip(
        semantic_scores[0],
        semantic_ids[0]
    ):

        if idx < 0:
            continue

        combined_scores[idx] = (
            0.7 * float(score)
            + 0.3 * float(bm25_scores[idx])
        )

    ranked = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_docs = []

    for idx, score in ranked[:k]:

        doc = metadata[idx].copy()

        doc["score"] = score

        top_docs.append(doc)

    return top_docs

# -------------------------
# Answer Generation
# -------------------------

def answer(question):

    docs = retrieve(question)

    print("\n========== RETRIEVED ==========\n")

    for d in docs:

        print(
            f"Document: {d['doc']} | "
            f"Chunk: {d['chunk_id']} | "
            f"Score: {d['score']:.4f}"
        )

    print("\n===============================\n")

    context = ""

    sources = set()

    for d in docs:

        sources.add(d["doc"])

        context += f"""
SOURCE: {d['doc']}
CHUNK: {d['chunk_id']}

{d['text']}

----------------------------------------
"""

    prompt = f"""
You are a document QA assistant.

Use ONLY the provided context.

If the answer cannot be found in the context,
reply exactly:

I cannot answer from the provided documents.

Whenever information is used,
cite the source document.

Example:
[Source: document_name.pdf]

Context:

{context}

Question:

{question}
"""

    response = llm.generate_content(
        prompt
    )

    final_answer = response.text

    final_answer += "\n\nSources:\n"

    for source in sorted(sources):
        final_answer += f"- {source}\n"

    return final_answer

# -------------------------
# CLI
# -------------------------

if __name__ == "__main__":

    print("\nHybrid RAG Ready")
    print("Type 'exit' to quit")

    while True:

        question = input(
            "\nQuestion: "
        ).strip()

        if question.lower() == "exit":
            break

        try:

            result = answer(question)

            print("\nAnswer:\n")
            print(result)

        except Exception as e:

            print(
                "\nError:",
                str(e)
            )
