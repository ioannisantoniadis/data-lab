::: {.callout-tip title="Data card: Feature hashing"}
| | |
|---|---|
| **Changes** | Representation: each level (or token) is mapped by a hash function to one of $m$ columns, with no stored vocabulary |
| **Assumption** | Collisions between levels are rare enough, or harmless enough, to accept for fixed memory |
| **What it does to the learned function** | Like one-hot, except that colliding levels share a column and so share an effect |
| **Which models care** | Linear models on very many or open-ended categories (text, identifiers) |
| **Fit on** | Nothing: the hash is fixed |
| **Failure modes** | Collisions grow with the number of levels: 2,000 levels in 1,024 columns use only about 880 of them; hashed columns cannot be traced back to levels |
| **Alternatives** | One-hot with a vocabulary; grouping rare levels; target encoding |
| **Checked by** | `tests/test_encoding.py::test_feature_hashing_collides_at_the_expected_rate` |
:::
