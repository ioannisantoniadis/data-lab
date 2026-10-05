## [The Data-Generating Process](chapters/01-the-data-generating-process.qmd#sec-dgp) {.unnumbered}

T1 knows $s(x, y)$ exactly. Real selection rules are rarely written down, usually depend on
variables that are not in the dataset, and mix both cases. The demonstration also uses a
correctly specified linear model. With a misspecified model, selection on $x$ is no longer
harmless, and how much it hurts depends on the model.

## [Labels](chapters/02-labels.qmd#sec-labels) {.unnumbered}

T1's noise is exactly class-conditional and its classes overlap by a known amount. Real label
noise mixes systematic confusions, annotator disagreement and ambiguity that no relabeling
could resolve. The figure's separability axis is unobservable in practice, and so is the noise
rate.

## [Data Types and Their Structure](chapters/03-data-types.qmd#sec-data-types) {.unnumbered}

The tones differ in one obvious feature and the series has one source of dependence. Real
audio needs perceptual frequency scales and longer context. Real time series mix trends,
seasonality and changes in regime. Both demonstrations show the direction and the mechanism of
an effect, not its size on real data.

## [Cleaning: Missing Values, Duplicates, Outliers, Leakage](chapters/04-cleaning.qmd#sec-cleaning) {.unnumbered}

The testbed's missingness depends on one column through a known curve, and its duplicates are
exact. Real missingness mixes mechanisms, and which one holds cannot be tested from the
observed data. The demonstrations show what each treatment does under each mechanism, not
which mechanism a real dataset has.

## [Affine Scaling](chapters/05-affine-scaling.qmd#sec-affine) {.unnumbered}

T1's features are Gaussian or exactly log-normal, and the outliers are a clean 1% at one
location. Real features
mix units, have ties and gaps, and contain outliers at many scales. The demonstrations show
which models are sensitive, not by how much on a given dataset.

## [Changing the Shape](chapters/06-changing-the-shape.qmd#sec-shape) {.unnumbered}

T1's target is exactly log-normal, so the log is exactly right and the shortfall factor is
known. Real targets are only roughly log-normal, and the right transform, if one exists, is
unknown. The demonstrations show what each transform aims at and when its correction holds,
not which transform to choose for a given dataset.

## [Encoding and Features](chapters/07-encoding-and-features.qmd#sec-encoding) {.unnumbered}

The noise category is pure noise, and the curve is a single smooth function of one feature.
Real categories carry some signal and some noise in unknown proportions, and real text needs
far more than counts. The demonstrations show what each encoding can represent and how target
encoding leaks, not which encoding is best for a given dataset.

## [Sampling and Weighting](chapters/08-sampling-and-weighting.qmd#sec-sampling) {.unnumbered}

T1's posterior is exactly logistic, its density ratio is known in closed form, and its
minority clusters are Gaussian. Real class-conditional distributions change along with the
priors, density ratios must be estimated, and the geometry of a minority class is unknown. The
demonstrations show what each lever targets and what it costs, not how well a given estimate of
a prior or a ratio will work on real data.

## [Augmentation](chapters/09-augmentation.qmd#sec-augmentation) {.unnumbered}

The side label is exactly symmetric, so whether an augmentation is right can be decided by
construction. Real symmetries are approximate, partial and strength-dependent, and nothing
measures them except held-out data. The demonstration uses a linear model on tiny images.
Networks that learn their own features may gain more, or less, from the same augmentation.

## [Distribution Shift](chapters/10-distribution-shift.qmd#sec-shift) {.unnumbered}

T1's shifts are clean: one factor changes, by a known amount, at a known time. Real shifts mix
kinds, drift gradually, and arrive with labels that are late, sparse or biased. The
demonstrations show what each test can see in principle, not what it will catch in a given
monitoring setup.

## [Learning Curves](chapters/11-learning-curves.qmd#sec-learning-curves) {.unnumbered}

The task is linear, its noise Gaussian and its model correctly specified, so the curve is
smooth and its floor known. Real learning curves can be ill-behaved, "showing worse learning
performance with more training data", for example when the model is misspecified, and they change shape as hyperparameters are
retuned [@viering2021shape]. Classical generalization bounds give worst-case rates; they are not
covered here.

## [Scaling Laws](chapters/12-scaling-laws.qmd#sec-scaling-laws) {.unnumbered}

A bigram model on a 50-token Markov source is not a transformer on natural text. Its exponents,
regimes and crossover points are properties of the toy, not predictions about real models. What
the toy does show is general: any curve with a floor bends away from a pure power law, and a fit
on one regime misreads the next.

## [Why Power Laws: The Long Tail](chapters/13-why-power-laws.qmd#sec-long-tail) {.unnumbered}

The learner memorizes, the labels are deterministic, and cases are exact identities. Real models
share structure between cases, so one example teaches about many, and "covered" is a matter of
degree. The demonstration shows how a long tail can produce power-law returns, and what selection
can and cannot buy when it does. It does not show that a given real scaling law arises this way.

## [Choosing Data](chapters/14-choosing-data.qmd#sec-choosing-data) {.unnumbered}

Each testbed isolates one condition. Real selection methods face several at once, use estimated
scores instead of true margins and posteriors, and run at scales where comparing with random
selection is itself expensive. The large-scale results above are reported by their authors, on
their data, as of their publication; they are not reproduced here.

## [A Data Decision Guide](chapters/15-decision-guide.qmd#sec-decision-guide) {.unnumbered}

Here the truth is known, so every check is exact. In practice the checks use held-out data,
which carries its own noise and its own shift, and the deployment question is often vague.
Real tabular data has more fields, missing for less tidy reasons; real audio has noise,
reverberation and gains that differ by frequency. The procedure transfers; the numbers do not.
