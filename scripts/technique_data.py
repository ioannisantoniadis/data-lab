"""Single source of truth for the data cards and the decision-guide table (SPEC §2.2, §10).

Each technique is one record. Running this file writes:

- ``docs/includes/cards/<slug>.md``: the data card (a ``callout-tip``), included in the
  chapter right after the technique's definition box;
- ``docs/includes/decision-guide.md``: the table chapter 15 shows, one row per card.

Edit a card here, never in the generated files, then run
``uv run python scripts/technique_data.py``.

The format mirrors ``rl-for-llms/scripts/method_data.py`` (a list of ``dict(...)`` records plus
``FIELDS`` and ``HEADERS``), so the records can later be merged with ``objectives-book``'s
method records (DECISIONS D6).

Fields
------
slug            file-safe id; the card is written to docs/includes/cards/<slug>.md
name            display name
chapter         chapter file stem where the card appears
levers          which of the four levers it pulls: subset of LEVERS. More than one is
                allowed, and the card must then say why (SPEC §2.2, falsifiability).
                Or exactly ["evaluation"] for a technique that acts only on evaluation
status          "draft" = transcribed from SPEC and not yet checked against sources and tests;
                "verified" = every field sourced (research-log.md) and its test passes
sources         bibliography keys (docs/references.bib) the card's claims rest on
changes ... checked_by   the eight card fields of SPEC §2.2, in order. checked_by is a test
                (tests/test_x.py::test_y) or, for a technique only stated from a source and
                not demonstrated in the book, "source: <bibkey>" (rendered as such)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LEVERS = ("representation", "q", "w", "labels")
# Techniques that act only on evaluation (splits, leakage control, shift detection,
# learning-curve estimation) pull no lever; their cards say so (SPEC §2.2, DECISIONS D7).
EVALUATION = "evaluation"
LEVER_LABEL = {
    "representation": "Representation",
    "q": "Sampling distribution $q$",
    "w": "Weights $w$",
    "labels": "Labels",
    EVALUATION: "Evaluation only",
}

# The card fields, in the order SPEC §2.2 fixes.
FIELDS = [
    "changes",
    "assumption",
    "effect",
    "models",
    "fit_on",
    "failure_modes",
    "alternatives",
    "checked_by",
]
HEADERS = {
    "changes": "Changes",
    "assumption": "Assumption",
    "effect": "What it does to the learned function",
    "models": "Which models care",
    "fit_on": "Fit on",
    "failure_modes": "Failure modes",
    "alternatives": "Alternatives",
    "checked_by": "Checked by",
}

T = [
    dict(
        slug="stratified-sampling",
        name="Stratified sampling",
        chapter="01-the-data-generating-process",
        levers=["q"],
        status="verified",
        sources=["cetinkayarundel2024ims"],
        changes="Sampling distribution $q$: fixes how many examples come from each stratum",
        assumption="Strata are known for the whole population before sampling, and the target varies more between strata than within them",
        effect="None on $q(y \\mid x)$; with proportional allocation, $q$ matches $p$ on the strata exactly instead of on average, so estimates vary less",
        models="Every model, through the variance of what it is fit on; most visible for rare strata",
        fit_on="The population frame: stratum sizes",
        failure_modes="Strata unrelated to the target (no gain); disproportionate allocation without weights (biased estimates)",
        alternatives="Simple random sampling; post-stratification weights ($w$)",
        checked_by="tests/test_selection.py::test_stratified_sampling_lowers_the_variance_of_the_mean",
    ),
    # The worked example of SPEC §2.2, transcribed verbatim. Status stays "draft" until
    # chapter 6 is researched (Duan 1983 read; the test passes).
    dict(
        slug="log-target",
        name="Log-transforming a skewed target",
        chapter="06-changing-the-shape",
        levers=["representation"],
        status="verified",
        sources=["duan1983smearing"],
        changes="Representation (of $y$)",
        assumption="$y > 0$, with multiplicative noise or right skew",
        effect="With MSE, the model learns $\\mathbb{E}[\\log y \\mid x]$: on the original scale, the geometric mean (the median under log-normal noise), not the mean",
        models="Linear and GLM-type models, neural nets; trees much less",
        fit_on="None (a fixed function); the smearing correction is fit on training residuals",
        failure_modes="Retransformation bias; zeros and negatives; smearing fails when the log-scale noise depends on $x$, and its factor is unstable when residuals are heavy-tailed",
        alternatives="Box-Cox / Yeo-Johnson; a log-link GLM; a loss matched to the noise",
        checked_by="tests/test_transforms.py::test_log_target_mse_predicts_geometric_mean",
    ),
    dict(
        slug="confident-learning",
        name="Finding label errors by confident learning",
        chapter="02-labels",
        levers=["labels"],
        status="verified",
        sources=["northcutt2019confident"],
        changes="Labels: flags examples whose given label disagrees confidently with an out-of-sample model, to drop or relabel",
        assumption="Class-conditional noise (flips independent of $x$ given the true class); out-of-sample probabilities that rank examples well; classes that overlap little",
        effect="If the flagged examples really are flips, removing them moves the learned posterior back toward $\\eta(x)$ and the boundary back to the clean one",
        models="Every model trained on the cleaned labels; the detector itself needs calibrated-enough probabilities",
        fit_on="Out-of-sample predictions (cross-validation), never the model's own training fit",
        failure_modes="Overlapping classes: genuine ambiguity looks like noise (precision near the noise rate); flips near the boundary are missed; noise that depends on $x$ breaks the assumption",
        alternatives="Repeated annotation and adjudication; noise-robust losses (loss-functions-lab); modeling the noise rates explicitly",
        checked_by="tests/test_labels.py::test_confident_learning_precision_depends_on_separability",
    ),
    dict(
        slug="spectrogram",
        name="Spectrogram (short-time Fourier magnitude)",
        chapter="03-data-types",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of $x$): from samples over time to energy per frequency per time window",
        assumption="The task depends on which frequencies are present and when, not on their phase; the window is long enough to resolve the frequencies that matter",
        effect="Makes frequency content a feature a linear or local model can use; discards phase, so phase-dependent targets become harder",
        models="Linear and distance-based models, which cannot build the transform themselves; whether a flexible model learns an equivalent front end from raw audio is not tested here",
        fit_on="None: a fixed transform (window length and overlap chosen in advance)",
        failure_modes="Window too short to resolve close frequencies or too long to localize changes in time; aliasing of frequencies above half the sampling rate happens before the transform and cannot be undone",
        alternatives="Raw waveform with a learned front end; mel or other perceptual frequency scales",
        checked_by="tests/test_data_types.py::test_spectrogram_representation_makes_tone_classes_linearly_separable",
    ),
    dict(
        slug="time-ordered-split",
        name="Time-ordered evaluation splits",
        chapter="03-data-types",
        levers=["evaluation"],
        status="verified",
        sources=["kaufman2011leakage"],
        changes="Evaluation only: validation examples always come after the training examples in time",
        assumption="Predictions will be made about later times than the training data; the series is autocorrelated or drifts",
        effect="None on the model; makes the error estimate match the error on the following period on average instead of on interpolated neighbors",
        models="All, most of all those that can interpolate (nearest neighbors, trees, flexible networks)",
        fit_on="Split boundaries set by time stamps",
        failure_modes="Features computed over the whole series (rolling statistics, normalizers) still carry the future into the past; a single future window gives a noisy estimate",
        alternatives="Blocked cross-validation with gaps; a final held-out future period",
        checked_by="tests/test_data_types.py::test_shuffled_cross_validation_leaks_time",
    ),
    dict(
        slug="complete-case",
        name="Complete-case analysis (dropping rows with missing values)",
        chapter="04-cleaning",
        levers=["q"],
        status="verified",
        sources=["vanbuuren2018fimd"],
        changes="Sampling distribution $q$: keeps only rows whose value was observed",
        assumption="MCAR: whether a value is missing is unrelated to anything",
        effect="Under MCAR, none beyond a smaller sample; under MAR or MNAR the kept rows follow a different distribution, so means shift, and so do fitted relationships unless the missingness depends only on the model's inputs (selection on $x$)",
        models="Every model",
        fit_on="Nothing is fit; the selection is made by the missingness itself",
        failure_modes="MAR or MNAR missingness (biased estimates); many columns with a little missingness each (few complete rows left)",
        alternatives="Regression or multiple imputation (MAR); modeling the missingness (MNAR)",
        checked_by="tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased",
    ),
    dict(
        slug="mean-imputation",
        name="Mean imputation",
        chapter="04-cleaning",
        levers=["representation"],
        status="verified",
        sources=["vanbuuren2018fimd"],
        changes="Representation: a missing value is encoded as the observed mean",
        assumption="MCAR, and only the column's mean matters downstream",
        effect="Keeps the mean under MCAR; shrinks the variance by the share imputed and weakens correlations; biases the mean under MAR or MNAR",
        models="Linear and distance-based models see a spike at the mean; trees can split it off",
        fit_on="Training rows only (the observed mean)",
        failure_modes="Non-MCAR missingness; heavy missingness (variance collapses); downstream use of variances or correlations",
        alternatives="Regression imputation; multiple imputation; a missing-indicator feature",
        checked_by="tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased",
    ),
    dict(
        slug="regression-imputation",
        name="Regression imputation",
        chapter="04-cleaning",
        levers=["representation"],
        status="verified",
        sources=["vanbuuren2018fimd"],
        changes="Representation: a missing value is encoded as its prediction from observed columns",
        assumption="MAR on the observed columns used as predictors, and a correctly specified imputation model",
        effect="Removes the bias of the mean under MAR; still understates the variance (imputed values have no noise) and overstates correlations",
        models="Every model; downstream uncertainty estimates are too narrow",
        fit_on="Training rows with the value observed",
        failure_modes="MNAR (the missing values differ in ways the predictors do not show); treating imputed values as observed",
        alternatives="Multiple imputation, which adds the missing noise back (van Buuren); stochastic regression imputation",
        checked_by="tests/test_missing.py::test_mcar_mean_imputation_shrinks_variance_mar_complete_case_biased",
    ),
    dict(
        slug="dedup-train-test",
        name="Removing train/test duplicates",
        chapter="04-cleaning",
        levers=["evaluation"],
        status="verified",
        sources=[],
        changes="Evaluation only: test rows that also appear in training are removed from the test set",
        assumption="Deployment inputs will not be copies of training inputs",
        effect="None on the model; the test score stops rewarding memorization",
        models="Most visible for models that can memorize (nearest neighbors, deep trees, large networks)",
        fit_on="Exact (or near-duplicate) matching of test rows against training rows",
        failure_modes="Near-duplicates that exact matching misses; deployment that genuinely repeats inputs, where duplicates are part of $p$",
        alternatives="Group-aware splits (all copies of an entity on one side)",
        checked_by="tests/test_leakage.py::test_train_test_duplicates_inflate_the_test_score",
    ),
    dict(
        slug="train-only-fitting",
        name="Fitting preprocessing on training data only",
        chapter="04-cleaning",
        levers=["evaluation"],
        status="verified",
        sources=["kaufman2011leakage"],
        changes="Evaluation only: every fitted step (scaler, imputer, selector, encoder) sees training data only",
        assumption="The evaluation should mimic deployment, where test labels and test inputs are not available at fit time",
        effect="None on what the model can learn; removes optimism, which is large for supervised steps and small for unsupervised ones on i.i.d. data",
        models="All",
        fit_on="Training folds only (inside each cross-validation fold)",
        failure_modes="Steps fit outside the pipeline (feature selection, target encoding, resampling) before splitting",
        alternatives="A scikit-learn Pipeline cross-validated as one estimator",
        checked_by="tests/test_leakage.py::test_fitting_preprocessing_on_test_is_optimistic",
    ),
    dict(
        slug="affine-scaling",
        name="Affine scaling (standard, min-max, max-abs)",
        chapter="05-affine-scaling",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of $x$): each feature is shifted and divided by a positive constant",
        assumption="The model's behavior depends on the features' units; a feature's typical spread is a fair yardstick for its importance",
        effect="None on the shape of any feature (skewness and kurtosis unchanged); equalizes the units that distances and penalties compare; improves the conditioning of a least-squares fit",
        models="Distance-based models (nearest neighbors, kernels, clustering), penalized models, gradient-trained models; not trees, and not unpenalized linear models' predictions",
        fit_on="Training data only: mean and standard deviation, or minimum and maximum, or maximum absolute value",
        failure_modes="Outliers set the scale (standard and min-max); a feature that should matter more is made to matter equally; test values outside the training range (min-max)",
        alternatives="Robust scaling; a shape-changing transform when the problem is skew, not units",
        checked_by="tests/test_scaling.py::test_affine_scalers_preserve_skewness_and_kurtosis",
    ),
    dict(
        slug="robust-scaling",
        name="Robust scaling (median and interquartile range)",
        chapter="05-affine-scaling",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of $x$): each feature is centered at its median and divided by its interquartile range",
        assumption="Outliers are a small share of each feature (fewer than a quarter on each side)",
        effect="Same as affine scaling for the bulk of the data, with a scale that outliers cannot inflate; the outliers themselves stay extreme",
        models="The same models as affine scaling",
        fit_on="Training data only: median and quartiles",
        failure_modes="Outliers are left in place at large values; features with an interquartile range of zero (mostly constant)",
        alternatives="Removing errors before scaling; clipping; a shape-changing transform; a robust loss (loss-functions-lab)",
        checked_by="tests/test_scaling.py::test_robust_scaler_keeps_inlier_spread_under_outliers",
    ),
    dict(
        slug="box-cox",
        name="Box-Cox and Yeo-Johnson power transforms",
        chapter="06-changing-the-shape",
        levers=["representation"],
        status="verified",
        sources=["box1964analysis", "yeo2000new"],
        changes="Representation: a power transform whose exponent $\\lambda$ is chosen by maximum likelihood to make the data as close to normal as the family allows",
        assumption="Some power of the data is close to normal; Box-Cox needs strictly positive data, Yeo-Johnson does not",
        effect="Reduces skew; for a target, the model learns a mean on the transformed scale, which back-transforms to the median of $y$ when the transformed noise is symmetric, not to the mean",
        models="Linear, GLM-type and distance-based models; trees are unaffected (monotone)",
        fit_on="Training data only: $\\lambda$ by maximum likelihood",
        failure_modes="No power makes the data normal (multimodal data); $\\lambda$ estimated on few points is noisy; retransformation bias as for the log",
        alternatives="A fixed log; a quantile transform; modeling the skew in the loss",
        checked_by="tests/test_transforms.py::test_box_cox_mle_recovers_known_lambda",
    ),
    dict(
        slug="quantile-transform",
        name="Quantile transform",
        chapter="06-changing-the-shape",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation: each feature is replaced by its estimated quantile, then mapped to a uniform or normal distribution",
        assumption="Only the order of values within a feature matters, not their spacing",
        effect="Any marginal shape becomes the chosen one; ranks within a feature are kept, distances and linear correlations are not",
        models="Distance-based and linear models change most; trees are unaffected on the training data (monotone)",
        fit_on="Training data only: the quantiles of each feature",
        failure_modes="Distances lose their meaning (two values far apart in the tail become neighbors); no extrapolation: everything beyond the training range maps to the boundary",
        alternatives="A log or power transform, which keeps the spacing's order of magnitude",
        checked_by="tests/test_transforms.py::test_quantile_transform_changes_distances_preserves_ranks",
    ),
    dict(
        slug="one-hot-ordinal",
        name="One-hot and ordinal encoding",
        chapter="07-encoding-and-features",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of a categorical $x$): one indicator column per level (one-hot), or one integer code (ordinal)",
        assumption="One-hot: none about order; ordinal: the levels are ordered and the code's spacing means something to the model",
        effect="One-hot lets a linear model give every level its own effect; an ordinal code forces a linear model to treat the effect as a straight line in the code",
        models="Linear and distance-based models depend on the choice; a tree can separate any level of an ordinal code, but one interval of codes per split, so unordered levels cost extra splits",
        fit_on="Training data only: the list of levels",
        failure_modes="Ordinal codes for unordered categories; unseen levels at test time; one-hot with very many levels (wide, sparse, rare columns)",
        alternatives="Target encoding (cross-fitted); hashing; grouping rare levels",
        checked_by="tests/test_encoding.py::test_ordinal_codes_impose_an_order_one_hot_does_not",
    ),
    dict(
        slug="feature-hashing",
        name="Feature hashing",
        chapter="07-encoding-and-features",
        levers=["representation"],
        status="verified",
        sources=["weinberger2009feature"],
        changes="Representation: each level (or token) is mapped by a hash function to one of $m$ columns, with no stored vocabulary",
        assumption="Collisions between levels are rare enough, or harmless enough, to accept for fixed memory",
        effect="Like one-hot, except that colliding levels share a column and so share an effect",
        models="Linear models on very many or open-ended categories (text, identifiers)",
        fit_on="Nothing: the hash is fixed",
        failure_modes="Collisions grow with the number of levels: 2,000 levels in 1,024 columns use only about 880 of them; hashed columns cannot be traced back to levels",
        alternatives="One-hot with a vocabulary; grouping rare levels; target encoding",
        checked_by="tests/test_encoding.py::test_feature_hashing_collides_at_the_expected_rate",
    ),
    dict(
        slug="target-encoding",
        name="Target encoding",
        chapter="07-encoding-and-features",
        levers=["representation"],
        status="verified",
        sources=["miccibarreca2001preprocessing"],
        changes="Representation: each level is replaced by a shrunk estimate of the mean target among training rows with that level",
        assumption="Levels with few rows are shrunk toward the global mean; each row's encoding is computed without that row's own label (cross-fitting)",
        effect="One informative column per categorical feature, however many levels; without cross-fitting, each row's own label leaks into its feature",
        models="Every model; most useful for high-cardinality categories with linear or tree models",
        fit_on="Training labels, cross-fitted on the training rows (out-of-fold), and fit on all training rows for test data",
        failure_modes="Encoding training rows with an encoder fit on those same rows: noise becomes a training signal that fails on new data; leakage across a time order",
        alternatives="One-hot; hashing; grouping rare levels",
        checked_by="tests/test_leakage.py::test_target_encoding_without_cross_fitting_leaks",
    ),
    dict(
        slug="splines-bins",
        name="Splines and discretization",
        chapter="07-encoding-and-features",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of a numeric $x$): a basis of piecewise polynomials (splines) or of interval indicators (bins)",
        assumption="The effect of $x$ is smooth (splines) or roughly constant within intervals (bins); enough data per knot or bin",
        effect="A linear model can fit a curve in $x$; bins give a step function, splines a smooth one",
        models="Linear and GLM-type models; trees already cut a feature into intervals",
        fit_on="Training data only: knot or bin positions (quantiles or a uniform grid)",
        failure_modes="Too many knots or bins (variance); extrapolation beyond the training range; bins hide variation within an interval",
        alternatives="A shape-changing transform; a model that is nonlinear in $x$ itself",
        checked_by="tests/test_encoding.py::test_splines_and_bins_let_a_linear_model_fit_a_curve",
    ),
    dict(
        slug="tf-idf",
        name="TF-IDF",
        chapter="07-encoding-and-features",
        levers=["representation"],
        status="verified",
        sources=[],
        changes="Representation (of a document): term counts, weighted down for terms that occur in many documents, scaled to unit length",
        assumption="Word order does not matter for the task; terms common to every document carry little information",
        effect="A fixed-length vector in which rare, distinctive terms dominate and document length matters less",
        models="Linear models and distance-based (cosine) models on text",
        fit_on="Training documents only: the vocabulary and document frequencies",
        failure_modes="Order and context are lost; rare terms are noisy; the vocabulary is fixed at fit time; the default token pattern drops one-character tokens",
        alternatives="Raw counts; hashing; learned embeddings (beyond this book)",
        checked_by="tests/test_encoding.py::test_tfidf_matches_the_documented_formula",
    ),
    dict(
        slug="balanced-resampling",
        name="Rebalancing classes (undersampling or oversampling)",
        chapter="08-sampling-and-weighting",
        levers=["q"],
        status="verified",
        sources=["king2001logistic", "saerens2002adjusting"],
        changes="Sampling distribution $q$: class proportions in training differ from those under $p$",
        assumption="Only the class priors change: $q(x \\mid y) = p(x \\mid y)$",
        effect="The model learns the posterior tilted to the training priors; at threshold 1/2 a balanced model decides as the true posterior would at threshold $p(y = 1)$",
        models="Every probabilistic classifier",
        fit_on="Training labels (class counts)",
        failure_modes="Probabilities are wrong unless corrected; undersampling discards data and raises variance; oversampling by copying repeats examples",
        alternatives="Class weights ($w$); training on $p$ and moving the threshold; prior-shift correction afterwards",
        checked_by="tests/test_imbalance.py::test_prior_shift_correction_restores_calibration",
    ),
    dict(
        slug="class-weights",
        name="Class weights",
        chapter="08-sampling-and-weighting",
        levers=["w"],
        status="verified",
        sources=["king2001logistic"],
        changes="Weights $w$: each example's loss is multiplied by its class's weight",
        assumption="As for rebalancing: only the class priors are to be changed",
        effect="Same tilted posterior as resampling to the same proportions, with less variance because no example is discarded",
        models="Every model trained by a weighted loss",
        fit_on="Training labels (class counts); scikit-learn's \"balanced\" uses n / (classes x count)",
        failure_modes="Probabilities are wrong unless corrected; very large weights on very rare classes make training noisy",
        alternatives="Resampling ($q$); moving the threshold; prior-shift correction",
        checked_by="tests/test_imbalance.py::test_resampling_and_reweighting_share_a_target_not_a_variance",
    ),
    dict(
        slug="prior-shift-correction",
        name="Prior-shift correction (and EM prior estimation)",
        chapter="08-sampling-and-weighting",
        levers=["w"],
        status="verified",
        sources=["saerens2002adjusting"],
        changes="Weights $w$ on the model's output: each class's posterior is multiplied by $p(y)/q(y)$ and renormalized",
        assumption="Only the priors differ between training and target data; the model's posteriors are calibrated under $q$; for EM, the new data are unlabeled draws from the target",
        effect="Turns posteriors learned under $q$ into posteriors under $p$; EM also estimates the unknown target prior",
        models="Any classifier with calibrated probabilities",
        fit_on="The training prior (counts) and the target prior (known, or estimated by EM on unlabeled target data)",
        failure_modes="$p(x \\mid y)$ also changed (not prior shift); miscalibrated training posteriors; EM converging slowly or to a biased value with few target examples",
        alternatives="Retraining on data from $p$; recalibration on labeled target data",
        checked_by="tests/test_imbalance.py::test_em_prior_estimation_recovers_test_prior",
    ),
    dict(
        slug="importance-weighting",
        name="Importance weighting for covariate shift",
        chapter="08-sampling-and-weighting",
        levers=["w"],
        status="verified",
        sources=[],
        changes="Weights $w(x) = p(x)/q(x)$ on each training example's loss",
        assumption="Covariate shift: $p(y \\mid x) = q(y \\mid x)$; $q(x) > 0$ wherever $p(x) > 0$; the density ratio is known or well estimated",
        effect="Weighted averages under $q$ estimate averages under $p$ without bias",
        models="Any model trained or evaluated by an average loss",
        fit_on="The density ratio: known here; in practice estimated, which adds its own error",
        failure_modes="Variance grows with $\\mathbb{E}_q[w^2]$, which grows exponentially with a Gaussian shift; regions where $q$ is tiny dominate; an estimated ratio can be badly wrong where data is sparse",
        alternatives="Collecting data from $p$; clipping or normalizing the weights (adds bias)",
        checked_by="tests/test_shift.py::test_importance_weighting_unbiased_with_growing_variance",
    ),
    dict(
        slug="smote",
        name="SMOTE (synthetic minority oversampling)",
        chapter="08-sampling-and-weighting",
        levers=["q"],
        status="verified",
        sources=["chawla2002smote"],
        changes="Sampling distribution $q$: adds synthetic minority examples on segments between a minority example and one of its $k$ nearest minority neighbors",
        assumption="The minority class occupies the space between nearby minority examples (locally convex); features are on comparable scales",
        effect="More minority examples near existing ones; the minority region looks broader and smoother",
        models="Models whose boundary depends on where minority examples lie (nearest neighbors, trees, kernels)",
        fit_on="Training minority examples only, inside each training fold",
        failure_modes="Minority clusters smaller than $k$, or separated by majority regions: synthetic points land between clusters; noisy minority labels are interpolated; applied before the split it leaks",
        alternatives="Class weights; random oversampling; prior-shift correction",
        checked_by="tests/test_imbalance.py::test_smote_fills_the_gap_when_k_exceeds_cluster_size",
    ),
    dict(
        slug="invariant-augmentation",
        name="Label-preserving augmentation (flips, crops, color, SpecAugment, RandAugment)",
        chapter="09-augmentation",
        levers=["q"],
        status="verified",
        sources=["cubuk2019randaugment", "park2019specaugment"],
        changes="Sampling distribution $q$: adds transformed copies of training inputs with their labels unchanged",
        assumption="The target is invariant under the transform: $p(y \\mid T(x)) = p(y \\mid x)$ for every transform $T$ used, at the strengths used",
        effect="More training data consistent with $p$, so less variance; the model is pushed toward the assumed invariance",
        models="Every model; most valuable at small $n$ and for models that cannot build the invariance in",
        fit_on="Training data only, transformed during training",
        failure_modes="The invariance is false, or false beyond some strength: augmented examples are then mislabeled; test-time inputs never look like the augmented ones",
        alternatives="An architecture that has the invariance built in; label-changing augmentation when the transform's effect is known",
        checked_by="tests/test_augmentation.py::test_invariant_augmentation_helps_noninvariant_hurts",
    ),
    dict(
        slug="label-changing-augmentation",
        name="Label-changing augmentation",
        chapter="09-augmentation",
        levers=["q", "labels"],
        status="verified",
        sources=[],
        changes="Sampling distribution $q$ and labels: adds transformed inputs with labels changed as the transform is known to change them",
        assumption="The transform's effect on the label is known exactly (here: a left-right flip reverses which half holds more ink)",
        effect="As much new, correctly labeled data as a label-preserving augmentation, including examples near the boundary from the other side",
        models="Every model",
        fit_on="Training data only",
        failure_modes="A wrongly assumed label change is label noise by construction; the effect may be known only for some inputs",
        alternatives="Label-preserving augmentation with a different transform; collecting the transformed cases",
        checked_by="tests/test_augmentation.py::test_label_changing_augmentation_helps_when_the_change_is_known",
    ),
    dict(
        slug="mixup",
        name="mixup",
        chapter="09-augmentation",
        levers=["q", "labels"],
        status="verified",
        sources=["zhang2017mixup"],
        changes="Sampling distribution $q$ and labels: trains on convex combinations of pairs of inputs, with the same combination of their labels",
        assumption="Between two training examples, the target changes linearly along the segment joining them (a vicinal distribution around the data)",
        effect="Trains the model on targets that change linearly between examples, so the learned function is pushed toward that behavior between them",
        models="Models trained by gradient on a loss that accepts soft labels, mostly neural networks",
        fit_on="Training batches, with the mixing weight drawn from Beta($\\alpha$, $\\alpha$)",
        failure_modes="Mixed inputs that are not plausible inputs; targets that are not linear between examples; small $\\alpha$ changes little, large $\\alpha$ blurs classes",
        alternatives="Label-preserving augmentation; label smoothing",
        checked_by="tests/test_augmentation.py::test_mixup_forms_the_same_convex_combination_of_inputs_and_labels",
    ),
    dict(
        slug="shift-detection",
        name="Detecting shift with two-sample tests",
        chapter="10-distribution-shift",
        levers=["evaluation"],
        status="verified",
        sources=["lopezpaz2016revisiting", "morenotorres2012unifying"],
        changes="Evaluation only: compares new inputs with reference inputs (and, with labels, new accuracy with reference accuracy)",
        assumption="Samples within each period are i.i.d.; for input-only tests, the shift that matters shows up in $p(x)$",
        effect="None on the model; an alarm that the training distribution no longer matches deployment",
        models="All",
        fit_on="A reference sample from training time; for the classifier test, half of each sample (the other half is held out)",
        failure_modes="Concept shift leaves the inputs unchanged and is invisible to input-only tests; small shifts need large samples; a detected shift may not hurt the model, and an undetected one may",
        alternatives="Monitoring the deployed model's accuracy on a stream of labeled cases; monitoring its predicted-class distribution (prior shift)",
        checked_by="tests/test_shift_detection.py::test_input_tests_detect_covariate_and_prior_shift_not_concept_shift",
    ),
    dict(
        slug="learning-curve-extrapolation",
        name="Estimating data needs from a pilot learning curve",
        chapter="11-learning-curves",
        levers=["evaluation"],
        status="verified",
        sources=["viering2021shape"],
        changes="Evaluation only: fits a parametric curve (here POW3, $A n^{-B} + C$) to errors measured on subsets of a pilot dataset, and extrapolates",
        assumption="The fitted form holds beyond the pilot range; the pilot range already shows the asymptotic behavior; the floor $C$ is identifiable from the pilot",
        effect="None on the model; an estimate, with an interval, of the error at a larger $n$ or of the $n$ needed for a target error",
        models="Any model; the estimate is specific to the model and its settings",
        fit_on="The pilot data only, with train/test splits that never put copies of a row on both sides (bootstrap included)",
        failure_modes="The floor is poorly determined, so targets near it are often judged unreachable; the pre-asymptotic curve is steeper than the asymptote, so needed sizes are underestimated; intervals are wide",
        alternatives="An independent estimate of the noise floor (repeated measurements or labels); collecting a second, larger pilot",
        checked_by="tests/test_learning_curves.py::test_extrapolated_data_requirement_is_biased_and_needs_the_floor",
    ),
    dict(
        slug="coverage-selection",
        name="Coverage-driven selection",
        chapter="13-why-power-laws",
        levers=["q"],
        status="verified",
        sources=["hutter2021learning", "michaud2023quantization", "dohmatob2024tale"],
        changes="Sampling distribution $q$: labels only examples that cover what is not yet covered (optionally most frequent first) instead of every draw from $p$",
        assumption="What counts as covered can be recognized; unlabeled draws are cheap relative to labels or training steps",
        effect="On Hutter's model the error per label falls as $n^{-\\alpha}$ instead of $n^{-\\alpha/(1+\\alpha)}$: a steeper power law, still a power law. Skipping repeats buys the exponent; frequency order adds only a constant factor (about 1.5)",
        models="Models that learn one case per example (memorization-like); the gain for models that generalize between cases is not measured here",
        fit_on="An unlabeled pool (or an oracle) and the record of what has been labeled",
        failure_modes="The gain is per label: it costs about $n^{1+\\alpha}$ unlabeled draws, and per draw nothing beats uniform sampling; a pool proportional to the labeling budget gives only a constant-factor gain; recognizing coverage is trivial here and hard for real data (near-duplicates, semantic similarity)",
        alternatives="Uniform sampling; active learning by model uncertainty; deduplication",
        checked_by="tests/test_long_tail.py::test_deduplicated_stream_reaches_the_oracle_exponent_per_label",
    ),
    dict(
        slug="difficulty-pruning",
        name="Pruning by difficulty (keep hard or easy examples)",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["sorscher2022beyond", "paul2021deep", "toneva2018empirical"],
        changes="Sampling distribution $q$: keeps a fraction of the training set ranked by a difficulty score (margin, EL2N, GraNd, forgetting events)",
        assumption="The score ranks examples as the true margin would; the right end to keep depends on how much data there is",
        effect="Keeping hard examples sharpens the boundary when data is abundant; keeping easy ones gives coarse information first when it is scarce",
        models="Demonstrated for a max-margin perceptron; reported for image networks",
        fit_on="Scores from a probe model trained on the training data (a few epochs, or a different architecture)",
        failure_modes="Keeping hard examples with scarce data; noisy scores at high pruning rates, where random pruning can win (Ayed and Hayou); hard examples that are mislabeled",
        alternatives="Random subsampling; self-supervised scores; reweighting instead of discarding",
        checked_by="tests/test_pruning.py::test_pruning_crossover_hard_when_abundant_easy_when_scarce",
    ),
    dict(
        slug="deduplication",
        name="Deduplicating training data",
        chapter="14-choosing-data",
        levers=["q", "w"],
        status="verified",
        sources=["lee2021deduplicating"],
        changes="Sampling distribution $q$ and weights: removes repeated examples, which also removes their extra weight in the loss",
        assumption="Repeats are artifacts of collection, not part of $p$; what counts as a repeat (exact or near) can be defined",
        effect="Less memorization of repeated content; evaluation that measures generalization rather than recall; on a long tail, labels are not spent on covered cases",
        models="Most visible for models that memorize (large language models, nearest neighbors)",
        fit_on="The whole corpus, before any split",
        failure_modes="Near-duplicates missed by exact matching; deduplicating genuine frequency information away; deduplicating after splitting",
        alternatives="Down-weighting repeats; group-aware splits",
        checked_by="tests/test_dedup.py::test_deduplication_reduces_overlap_optimism",
    ),
    dict(
        slug="uncertainty-sampling",
        name="Active learning by uncertainty sampling",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["settles2009active"],
        changes="Sampling distribution $q$: the next example to label is the pool example the current model is least sure about",
        assumption="Uncertainty reflects what the model has not learned, not irreducible label noise; the pool represents $p$",
        effect="Labels concentrate near the current boundary, which helps when classes are nearly separable",
        models="Probabilistic classifiers that are refit as labels arrive",
        fit_on="The labeled set so far and an unlabeled pool",
        failure_modes="Noisy labels: uncertainty points at noise, and the gain vanishes; the labeled set is no longer a sample of $p$ (biased estimates); querying outliers",
        alternatives="Random labeling; diversity- or density-weighted selection; RHO-LOSS-style criteria",
        checked_by="tests/test_active_learning.py::test_uncertainty_sampling_gains_shrink_with_label_noise",
    ),
    dict(
        slug="synthetic-data",
        name="Training on model-generated data",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["shumailov2024ai", "dohmatob2024tale", "gerstgrasser2024model"],
        changes="Sampling distribution $q$: training examples are drawn from a fitted model instead of from $p$",
        assumption="The generator's distribution covers $p$, including its tail",
        effect="A generator fit to finite data misses the unseen tail; a learner trained on its output plateaus at that missing mass",
        models="Every model trained on generated data",
        fit_on="The generator's own training data",
        failure_modes="Replacing real data generation after generation loses more of the tail each time; accumulating real and synthetic data does not",
        alternatives="Keeping and reusing the real data; mixing a share of fresh real data",
        checked_by="tests/test_collapse.py::test_refitting_on_own_samples_loses_tail",
    ),
    dict(
        slug="rho-loss",
        name="RHO-LOSS (reducible holdout loss selection)",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["mindermann2022prioritized"],
        changes="Sampling distribution $q$: within each batch, trains on the points whose training loss most exceeds the loss of a small model trained on holdout data",
        assumption="Holdout data from $p$ is available; a small model's loss estimates what is irreducible (noise) for each point",
        effect="Skips points that are already learned and points that are noisy or unlearnable, which plain high-loss selection would pick",
        models="Reported for neural networks trained by SGD",
        fit_on="A holdout set, through the irreducible-loss model",
        failure_modes="A poor irreducible-loss model misjudges noise; holdout data that is not from $p$",
        alternatives="Uniform sampling; uncertainty or high-loss selection",
        checked_by="source: mindermann2022prioritized",
    ),
    dict(
        slug="domain-mixtures",
        name="Choosing domain mixtures (DoReMi)",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["xie2023doremi"],
        changes="Sampling distribution $q$: the proportion of training data drawn from each domain",
        assumption="Weights found by a small proxy model transfer to a larger model",
        effect="Reported to reach a baseline's downstream accuracy in fewer steps",
        models="Reported for language models",
        fit_on="A small proxy model trained with group distributionally robust optimization over domains",
        failure_modes="Weights that do not transfer to the larger model or to the target task",
        alternatives="Default or hand-tuned proportions; mixture scaling laws",
        checked_by="source: xie2023doremi",
    ),
    dict(
        slug="filtering",
        name="Filtering web-scale data",
        chapter="14-choosing-data",
        levers=["q"],
        status="verified",
        sources=["gadre2023datacomp", "penedo2024fineweb", "goyal2024scaling"],
        changes="Sampling distribution $q$: keeps the documents a quality filter scores highly",
        assumption="The filter's notion of quality predicts usefulness for the target; enough data remains for the compute available",
        effect="Reported to give better models for the same training budget when the filter is good; benchmarks such as DataComp compare filters directly",
        models="Large models trained on web data",
        fit_on="Heuristics or classifiers, sometimes trained on reference data",
        failure_modes="Filtering away rare but needed content (the tail); filtering choices that are right for one compute budget and wrong for another (Goyal et al.)",
        alternatives="Deduplication only; reweighting by quality instead of discarding",
        checked_by="source: goyal2024scaling",
    ),
]

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "docs" / "includes" / "cards"
GUIDE = ROOT / "docs" / "includes" / "decision-guide.md"
CHECKED_BY = re.compile(r"^(tests/test_[a-z0-9_]+\.py::test_[a-z0-9_]+|source: [a-z0-9]+)$")


def validate(records: list[dict]) -> list[str]:
    """Return a list of problems; empty means the records are well formed."""
    problems = []
    slugs = set()
    required = {"slug", "name", "chapter", "levers", "status", "sources", *FIELDS}
    for r in records:
        tag = r.get("slug", "<no slug>")
        missing = required - set(r)
        if missing:
            problems.append(f"{tag}: missing fields {sorted(missing)}")
            continue
        if r["slug"] in slugs:
            problems.append(f"{tag}: duplicate slug")
        slugs.add(r["slug"])
        levers = r["levers"]
        if levers != [EVALUATION] and (not levers or any(lv not in LEVERS for lv in levers)):
            problems.append(
                f"{tag}: levers must be a non-empty subset of {LEVERS}, or ['{EVALUATION}']"
            )
        if r["status"] not in ("draft", "verified"):
            problems.append(f"{tag}: status must be 'draft' or 'verified'")
        if not CHECKED_BY.match(r["checked_by"]):
            problems.append(f"{tag}: checked_by must be tests/test_x.py::test_y or source: key")
        if not (ROOT / "docs" / "chapters" / f"{r['chapter']}.qmd").exists():
            problems.append(f"{tag}: chapter file {r['chapter']}.qmd does not exist")
    return problems


def cell(text: str) -> str:
    """Escape a table cell. A bare | inside math breaks Markdown tables (playbook pitfall)."""
    return str(text).replace("|", r"\|")


def card(r: dict) -> str:
    draft = " (draft: not yet verified)" if r["status"] == "draft" else ""
    lines = [f'::: {{.callout-tip title="Data card: {r["name"]}{draft}"}}', "| | |", "|---|---|"]
    for f in FIELDS:
        value = r[f]
        if f == "checked_by":
            value = (f"Not tested here; stated from [@{r[f][8:]}]" if r[f].startswith("source: ")
                     else f"`{r[f]}`")
        lines.append(f"| **{HEADERS[f]}** | {cell(value)} |")
    lines.append(":::")
    return "\n".join(lines) + "\n"


def guide_table(records: list[dict]) -> str:
    cols = ["assumption", "fit_on", "failure_modes"]
    head = "| Technique | Lever | " + " | ".join(HEADERS[c] for c in cols) + " |"
    sep = "|" + "---|" * (len(cols) + 2)
    rows = []
    for r in sorted(records, key=lambda rec: rec["chapter"]):
        # The guide is included from a chapter file, so links are relative to docs/chapters/.
        name = f"[{r['name']}]({r['chapter']}.qmd)"
        lever = ", ".join(LEVER_LABEL[lv] for lv in r["levers"])
        if r["status"] == "draft":
            name += " (draft)"
        rows.append(f"| {name} | {lever} | " + " | ".join(cell(r[c]) for c in cols) + " |")
    return "\n".join([head, sep, *rows]) + "\n"


def main() -> int:
    problems = validate(T)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    CARDS.mkdir(parents=True, exist_ok=True)
    for r in T:
        (CARDS / f"{r['slug']}.md").write_text(card(r))
    GUIDE.write_text(guide_table(T))
    print(f"wrote {len(T)} card(s) and the decision guide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
