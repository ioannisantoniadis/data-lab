"""Claim tests: Part IV, deduplication (SPEC §8 claim 18; T4)."""

import numpy as np

from data_lab.selection import dedup_experiment


def test_deduplication_reduces_overlap_optimism():
    """Claim 18. With duplicates in a text corpus (50 of 400 documents copied 5 extra times)
    and a model that can memorize (a trigram model on T4), a test split that overlaps the
    training split reports a cross-entropy more than 0.3 nats below the same model's
    cross-entropy on fresh documents, in every seed. Removing duplicates before splitting brings
    the measured value to within 0.15 nats of the fresh-document value (20 seeds)."""
    res = dedup_experiment()
    optimism = res["fresh"] - res["contaminated"]
    optimism_dedup = res["fresh_dedup"] - res["dedup"]
    assert np.all(optimism > 0.3)
    assert np.all(np.abs(optimism_dedup) < 0.15)
