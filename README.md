# Defence Procurement Intelligence System

## Overview

This project implements an intelligent document-question answering system for defence procurement and financial policy documents. The solution combines document retrieval and large language model (LLM) reasoning to provide accurate, context-aware answers grounded in official policy sources.

The system processes a collection of PDF documents, extracts and structures their contents, indexes them for efficient retrieval, and generates responses supported by relevant source citations.

---

## System Architecture

```text
PDF Documents
      │
      ▼
Document Extraction (PyPDF)
      │
      ▼
Rule-Aware Chunking
      │
      ▼
Sentence Embedding Generation
      │
      ▼
FAISS Vector Index
      │
      ▼
BM25 Lexical Retrieval
      │
      ▼
Hybrid Retrieval & Ranking
      │
      ▼
LLM-Based Answer Generation
      │
      ▼
Answer with Source Citations
```

---

## Key Design Decisions

### Rule-Aware Chunking

Government and defence policy documents are typically organized around numbered rules, sections, and clauses. Instead of using fixed-size text chunks, the system preserves these natural boundaries during chunking.

This approach:

* Maintains contextual integrity
* Improves retrieval relevance
* Produces more meaningful citations
* Reduces information fragmentation

---

### Embedding Model

**Model:** `all-MiniLM-L6-v2`

#### Rationale

* Lightweight and computationally efficient
* Fast embedding generation
* Strong semantic search performance
* Well-suited for medium-sized document collections

---

### Vector Storage

**Technology:** FAISS (`IndexFlatIP`)

#### Rationale

* High-performance similarity search
* Simple and reliable implementation
* Industry-standard retrieval baseline
* Scales efficiently for document search workloads

---

### Retrieval Strategy

The system adopts a hybrid retrieval approach by combining:

* **Semantic Retrieval (FAISS)** – captures contextual meaning and intent
* **Lexical Retrieval (BM25)** – captures exact keywords, rule references, and numerical values

#### Benefits

Defence procurement policies often contain:

* Rule numbers
* Financial thresholds
* Procurement categories
* Regulatory references

BM25 excels at retrieving exact matches, while semantic search improves understanding of user intent. Combining both methods improves overall retrieval quality.

---

### Context Selection

The top **5** highest-ranked document chunks are selected and provided to the language model as supporting evidence.

This balances:

* Retrieval accuracy
* Response quality
* Computational efficiency
* Token consumption

---

## Handling Unanswerable Queries

To ensure trustworthy responses, the language model is instructed to answer exclusively from retrieved evidence.

When sufficient information is unavailable within the document corpus, the system returns:

> "I cannot answer from the provided documents."

This approach minimizes hallucinations and ensures that generated responses remain grounded in verifiable source material.

---

## Execution

### Build the Retrieval Index

```bash
python src/ingest.py
```

### Run Queries

```bash
python src/query.py
```

---

## Future Enhancements

Potential improvements include:

1. Cross-encoder re-ranking for improved retrieval precision
2. Fine-grained citation generation at paragraph or clause level
3. Automated evaluation framework and benchmarking
4. Metadata-based filtering and document categorization
5. Query expansion techniques for policy and rule references
6. Retrieval performance analytics and monitoring
7. Multi-document reasoning optimization

---

## Outcome

The resulting system provides a scalable and reliable framework for navigating complex defence procurement policies, enabling users to obtain accurate, evidence-backed answers while maintaining transparency through source citations.

