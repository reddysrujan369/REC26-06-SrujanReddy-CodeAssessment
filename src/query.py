import os
import pickle
import faiss
import numpy as np

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from rank_bm25 import BM25Okapi

import google.generativeai as genai

import os

print("API KEY:", os.getenv("GEMINI_API_KEY"))

# -------------------------
# Gemini Setup
# -------------------------

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

genai.configure(
    api_key=API_KEY
)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -------------------------
# Load Embedding Model
# -------------------------

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -------------------------
# Load FAISS
# -------------------------

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

# -------------------------
# BM25
# -------------------------

tokenized_chunks = [
    chunk.split()
    for chunk in all_chunks
]

bm25 = BM25Okapi(
    tokenized_chunks
)

# -------------------------
# Retrieval
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

        doc = metadata[idx]

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
            f"Doc: {d['doc']} | Chunk: {d['chunk_id']} | Score: {d['score']:.4f}"
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

"""

    prompt = f"""
You are a document QA assistant.

Answer ONLY from the supplied context.

If the answer is not present,
reply exactly:

I cannot answer from the provided documents.

Always provide citations.

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

    for s in sorted(sources):

        final_answer += f"- {s}\n"

    return final_answer


# -------------------------
# CLI
# -------------------------

if __name__ == "__main__":

    while True:

        q = input("\nQuestion: ")

        if q.lower() == "exit":
            break

        print("\n")

        try:

            print(answer(q))

        except Exception as e:

            print("Error:", e)