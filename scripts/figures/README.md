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
| *(none yet: the signature figure comes first, in Phase 1)* | | | |
