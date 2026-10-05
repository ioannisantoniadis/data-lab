"""Claim tests: Part IV, data pruning (SPEC §8 claim 17; T3)."""


from data_lab.selection import pruning_experiment


def test_pruning_crossover_hard_when_abundant_easy_when_scarce():
    """Claim 17. On T3 (dimension 100, keep half, probe = teacher), keeping the hardest examples
    beats keeping the easiest ones when the initial data is abundant, and the reverse when it is
    scarce (Sorscher et al. 2022). Over 20 seeds: at P/N = 1 and 2, easy beats hard in every
    seed; at P/N = 16, hard beats easy in at least 15 of 20 seeds, and on average."""
    res = pruning_experiment(ratios=(1.0, 2.0, 16.0))
    hard_wins = res["hard"] < res["easy"]
    assert not hard_wins[:, 0].any() and not hard_wins[:, 1].any()
    assert hard_wins[:, 2].sum() >= 15
    assert res["hard"][:, 2].mean() < res["easy"][:, 2].mean()
