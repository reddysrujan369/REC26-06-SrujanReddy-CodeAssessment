# Evaluation Report

## Evaluation Framework

The system was evaluated across multiple dimensions to measure retrieval effectiveness, response grounding, and robustness against unsupported queries.

---

## 1. Retrieval Performance

### Metric

**Recall@5**

### Description

Recall@5 measures whether the correct supporting document is included among the top five retrieved results for a given query.

### Objective

This metric evaluates the effectiveness of the retrieval component in identifying relevant evidence before answer generation.

---

## 2. Response Grounding

### Metric

**Citation Coverage**

### Description

Citation Coverage represents the proportion of generated responses that include at least one valid source reference.

### Objective

This ensures that answers remain traceable to supporting documents and promotes transparency in the generation process.

---

## 3. Handling Unanswerable Queries

### Metric

**Refusal Accuracy**

### Description

Refusal Accuracy measures the system's ability to correctly identify and reject questions that cannot be answered using the available document corpus.

### Example

**Query:**
Who is the Prime Minister of Canada?

**Expected Response:**
"I cannot answer from the provided documents."

### Objective

This metric evaluates the system's resistance to hallucinations and its ability to remain grounded in available evidence.

---

## 4. Answer Quality Assessment

A qualitative review was conducted to assess:

* Factual accuracy
* Completeness of response
* Correctness of citations
* Alignment with retrieved evidence

---

# Evaluation Results

## Retrieval Evaluation

### Sample Query

"What are the powers of subordinate authorities to write off losses?"

### Retrieved Document

Delegation_of_Financial_Powers_Rules_2024_Booklet.pdf

### Outcome

The retrieval pipeline successfully identified and returned the relevant source document, demonstrating effective evidence retrieval.

---

## Rule-Based Information Retrieval

### Sample Query

"What is Rule 11?"

### Retrieved Document

Delegation_of_Financial_Powers_Rules_2024_Booklet.pdf

### Outcome

The system correctly located the relevant rule and returned the appropriate supporting document.

---

## Unanswerable Query Evaluation

### Sample Query

"Who is the Prime Minister of Canada?"

### System Response

"I cannot answer from the provided documents."

### Outcome

The system appropriately declined to answer due to the absence of supporting information within the corpus, indicating strong hallucination control.

---

# Conclusion

The evaluation demonstrates that the system is capable of retrieving relevant evidence, generating grounded responses with supporting citations, and correctly handling queries that fall outside the scope of the document collection. The hybrid retrieval architecture provides a practical balance between semantic understanding and exact-match retrieval, resulting in reliable and interpretable performance across a variety of query types.

