# Figure scripts

Each `fig_<slug>.py` computes something real with the `data_lab` package and writes
`docs/images/<slug>.png` through `save_figure` in `_theme.py` (200 dpi). Quarto does not run
Python; the PNGs are pre-generated and committed. Conventions are in `CONVENTIONS.md`, under
*Figures*.

```bash
uv run python scripts/figures/fig_<slug>.py                       # one figure
for f in scripts/figures/fig_*.py; do uv run python "$f"; done    # all
```

| Script | Image | Chapter | Lesson ("this figure makes visible that …") |
|---|---|---|---|
| `fig_long_tail_signature.py` | `long_tail_signature.png` | [The Testbeds](../../docs/appendix-testbeds.qmd), T2; later [Why Power Laws](../../docs/chapters/13-why-power-laws.qmd) | uniform sampling's error is a power law set by the tail; coverage-driven selection steepens it (to $-\alpha$) but does not escape it, and only an oracle or an unlabeled pool growing like $n^{1+\alpha}$ buys the steeper slope (about 9 s) |
