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
| `fig_long_tail_signature.py` | `long_tail_signature.png` | [The Testbeds](../../docs/appendix-testbeds.qmd), T2; [Why Power Laws](../../docs/chapters/13-why-power-laws.qmd) | uniform sampling's error is a power law set by the tail; per label, skipping repeats steepens it to $-\alpha$ (frequency order adds only a constant) without escaping a power law, at a cost of about $n^{1+\alpha}$ draws; a pool proportional to $n$ only shifts the uniform line (about 20 s) |
| `fig_selection_bias.py` | `selection_bias.png` | [The Data-Generating Process](../../docs/chapters/01-the-data-generating-process.qmd) | selection on x leaves the regression intact but biases summaries; selection on y biases the regression |
| `fig_label_noise.py` | `label_noise.png` | [Labels](../../docs/chapters/02-labels.qmd) | symmetric noise keeps the boundary, asymmetric noise moves it; label errors are findable only when classes barely overlap |
| `fig_data_types.py` | `data_types.png` | [Data Types](../../docs/chapters/03-data-types.qmd) | the spectrogram makes frequency usable by a linear model; shuffled CV on a time series leaks |
| `fig_missingness.py` | `missingness.png` | [Cleaning](../../docs/chapters/04-cleaning.qmd) | which treatment of missing values is biased depends on the mechanism |
| `fig_leakage.py` | `leakage.png` | [Cleaning](../../docs/chapters/04-cleaning.qmd) | duplicates inflate test scores past the Bayes accuracy; supervised steps leak far more than unsupervised ones |
| `fig_affine_scaling.py` | `affine_scaling.png` | [Affine Scaling](../../docs/chapters/05-affine-scaling.qmd) | units decide distances and conditioning; only the robust scaler survives outliers |
| `fig_changing_shape.py` | `changing_shape.png` | [Changing the Shape](../../docs/chapters/06-changing-the-shape.qmd) | affine scaling keeps skew, nonlinear transforms remove it; a log target aims at the median; smearing needs constant noise |
| `fig_encoding.py` | `encoding.png` | [Encoding and Features](../../docs/chapters/07-encoding-and-features.qmd) | target encoding without cross-fitting turns noise into a training signal; bins and splines let a linear model fit curves |
| `fig_sampling_weighting.py` | `sampling_weighting.png` | [Sampling and Weighting](../../docs/chapters/08-sampling-and-weighting.qmd) | resampling and reweighting aim at the same tilted posterior, undone by prior-shift correction, with different variance; importance-weight variance explodes with shift; SMOTE fills gaps once k exceeds a cluster |
| `fig_augmentation.py` | `augmentation.png` | [Augmentation](../../docs/chapters/09-augmentation.qmd) | an augmentation helps exactly when its assumption about the label is true; a label-changing transform is useful once the change is known |
| `fig_distribution_shift.py` | `distribution_shift.png` | [Distribution Shift](../../docs/chapters/10-distribution-shift.qmd) | input-only tests detect covariate shift and miss concept shift |
| `fig_learning_curves.py` | `learning_curves.png` | [Learning Curves](../../docs/chapters/11-learning-curves.qmd) | noise sets the floor and dimension the approach; a small pilot can bound the error far out but not the data needed near the floor |
| `fig_scaling_laws.py` | `scaling_laws.png` | [Scaling Laws](../../docs/chapters/12-scaling-laws.qmd) | a scaling curve is a power law only within a regime; without a floor, extrapolation goes below the entropy rate |
| `fig_choosing_data.py` | `choosing_data.png` | [Choosing Data](../../docs/chapters/14-choosing-data.qmd) | every way of choosing data rests on a condition: pruning, deduplication, uncertainty sampling and synthetic data each fail when theirs does (about 60 s) |
