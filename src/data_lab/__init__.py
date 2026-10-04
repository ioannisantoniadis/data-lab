"""data_lab: testbeds and methods for *What the Model Sees: Training Data from First Principles*.

Every figure script and every test imports this package, so a figure is always the real code,
never a re-implementation. The package is local only (DECISIONS D2): ``uv sync`` installs it
into the repository's virtual environment, and the ``Private :: Do Not Upload`` classifier
makes PyPI reject any upload.

Layout (SPEC §16):

- ``testbeds/``: the ground-truth testbeds T1–T5 (SPEC §7). Implemented in Phase 1.
- ``transforms``: scaling, shape-changing transforms, encodings (Part II). Phase 2.
- ``sampling``: resampling, reweighting, prior-shift correction (Part III). Phase 3.
- ``selection``: coverage-driven selection, pruning, deduplication (Part IV). Phases 1 and 3.
"""

__version__ = "0.1.0"
