# Defence Procurement RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system over a corpus of defence procurement and financial policy documents.

The system ingests PDF documents, chunks them into retrievable units, generates embeddings, stores them in a FAISS vector index, retrieves relevant context for a query, and generates grounded answers with citations.

---

## Architecture

PDF Documents
↓
Text Extraction (PyPDF)
↓
Rule-Aware Chunking
↓
Sentence Embeddings (all-MiniLM-L6-v2)
↓
FAISS Vector Index
↓
BM25 Retrieval
↓
Hybrid Ranking
↓
LLM Answer Generation
↓
Citations

---

## Design Choices

### Chunking

A rule-aware chunking strategy was used.

Government policy documents are naturally structured into numbered rules (Rule 1, Rule 2, etc.). Splitting documents around rule boundaries preserves semantic meaning better than fixed-size chunks.

### Embedding Model

Model:
all-MiniLM-L6-v2

Reason:

* Fast
* Lightweight
* Strong semantic retrieval performance
* Suitable for several hundred documents

### Vector Store

FAISS IndexFlatIP

Reason:

* Fast similarity search
* Simple implementation
* Widely used baseline for RAG systems

### Retrieval

Hybrid Retrieval:

* Semantic Retrieval (FAISS)
* Lexical Retrieval (BM25)

Reason:
Government documents contain many exact references such as rule numbers, financial limits, and procurement categories. BM25 improves retrieval of these exact terms.

### Top-K

k = 5

The top five retrieved chunks are provided to the answer generation stage.

---

## Handling Unanswerable Questions

The system is instructed to answer only from retrieved context.

If sufficient evidence is not present in the retrieved documents, the system returns:

"I cannot answer from the provided documents."

This reduces hallucination and ensures grounded responses.

---

## Running

### Build Index

python src/ingest.py

### Query

python src/query.py

---

## Future Improvements

If additional time were available:

1. Cross-encoder reranking
2. Better citation granularity
3. Automatic evaluation pipeline
4. Metadata filtering by document
5. Query expansion for rule references
