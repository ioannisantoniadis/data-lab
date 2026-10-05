::: {.callout-tip title="Data card: TF-IDF"}
| | |
|---|---|
| **Changes** | Representation (of a document): term counts, weighted down for terms that occur in many documents, scaled to unit length |
| **Assumption** | Word order does not matter for the task; terms common to every document carry little information |
| **What it does to the learned function** | A fixed-length vector in which rare, distinctive terms dominate and document length matters less |
| **Which models care** | Linear models and distance-based (cosine) models on text |
| **Fit on** | Training documents only: the vocabulary and document frequencies |
| **Failure modes** | Order and context are lost; rare terms are noisy; the vocabulary is fixed at fit time; the default token pattern drops one-character tokens |
| **Alternatives** | Raw counts; hashing; learned embeddings (beyond this book) |
| **Checked by** | `tests/test_encoding.py::test_tfidf_matches_the_documented_formula` |
:::
