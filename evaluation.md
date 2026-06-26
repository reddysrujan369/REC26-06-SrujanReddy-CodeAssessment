# Evaluation Notes

## Metrics

### 1. Retrieval Quality

Metric:
Recall@5

Definition:
Whether the relevant document appears in the top 5 retrieved results.

Purpose:
Measures if retrieval returns the correct evidence.

---

### 2. Grounding Quality

Metric:
Citation Coverage

Definition:
Percentage of answers containing at least one source citation.

Purpose:
Ensures generated answers are traceable to retrieved evidence.

---

### 3. Unanswerable Handling

Metric:
Refusal Accuracy

Definition:
Percentage of unanswerable questions correctly rejected.

Example:

Question:
Who is the Prime Minister of Canada?

Expected:

"I cannot answer from the provided documents."

Purpose:
Measures hallucination resistance.

---

### 4. Answer Quality

Manual inspection of:

* factual correctness
* completeness
* citation correctness

---

## Results

### Retrieval

Example Query:

"What are the powers of subordinate authorities to write off losses?"

Retrieved:
Delegation_of_Financial_Powers_Rules_2024_Booklet.pdf

Result:
Relevant document successfully retrieved.

---

### Rule Retrieval

Example Query:

"What is Rule 11?"

Retrieved:
Delegation_of_Financial_Powers_Rules_2024_Booklet.pdf

Result:
Correct source document retrieved.

---

### Unanswerable Question

Example Query:

"Who is the Prime Minister of Canada?"

Output:

"I cannot answer from the provided documents."

Result:
Correct refusal.

---

## Conclusion

The system demonstrates effective retrieval, grounded responses, and correct handling of unanswerable questions using a simple and interpretable RAG architecture.
