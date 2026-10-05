::: {.callout-tip title="Data card: One-hot and ordinal encoding"}
| | |
|---|---|
| **Changes** | Representation (of a categorical $x$): one indicator column per level (one-hot), or one integer code (ordinal) |
| **Assumption** | One-hot: none about order; ordinal: the levels are ordered and the code's spacing means something to the model |
| **What it does to the learned function** | One-hot lets a linear model give every level its own effect; an ordinal code forces a linear model to treat the effect as a straight line in the code |
| **Which models care** | Linear and distance-based models depend on the choice; a tree can separate any level of an ordinal code, but one interval of codes per split, so unordered levels cost extra splits |
| **Fit on** | Training data only: the list of levels |
| **Failure modes** | Ordinal codes for unordered categories; unseen levels at test time; one-hot with very many levels (wide, sparse, rare columns) |
| **Alternatives** | Target encoding (cross-fitted); hashing; grouping rare levels |
| **Checked by** | `tests/test_encoding.py::test_ordinal_codes_impose_an_order_one_hot_does_not` |
:::
