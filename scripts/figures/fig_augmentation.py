"""Chapter 9: augmentation is an assumption about p (T5 side task; claims 13 and 38).

Panel A: one digit image, its up-down flip and its left-right flip, with the synthetic side
label (1 if the left half holds more ink) of each.
Panel B: test accuracy of a logistic regression against training size, with no augmentation,
with up-down flips (a true invariance), with left-right flips keeping the label (a false
invariance) and with left-right flips and the reversed label (the flip's true effect);
mean and 10-90% band over 20 seeds.

This figure makes visible that an augmentation helps exactly when its assumption about how
the transform acts on the label is true, and that a transform which changes the label is
useful once the change is known.

Also publishes the chapter's quoted numbers (namespace "ch9") to docs/_variables.yml.

Run: uv run python scripts/figures/fig_augmentation.py   (about 5 s)
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _theme import (  # noqa: E402
    INK_SECONDARY,
    LEVER_COLOR,
    MUTED,
    apply_theme,
    save_figure,
)
from publish import fmt, publish  # noqa: E402

from data_lab.augment import augmentation_experiment  # noqa: E402
from data_lab.testbeds.t5_signals import (  # noqa: E402
    flip_left_right,
    flip_up_down,
    side_label,
    side_task,
)

apply_theme()
fig = plt.figure(figsize=(12, 4.4), layout="constrained")
grid = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 0.15, 4.2])

x, y = side_task()
example = x[np.argmax(np.abs(x[:, :, :4].sum(axis=(1, 2)) - x[:, :, 4:].sum(axis=(1, 2))))]
panels = [("original", example), ("up-down flip", flip_up_down(example[None])[0]),
          ("left-right flip", flip_left_right(example[None])[0])]
for k, (title, img) in enumerate(panels):
    ax = fig.add_subplot(grid[0, k])
    ax.imshow(img, cmap="Greys")
    ax.axvline(3.5, color=LEVER_COLOR["labels"], lw=1)
    ax.set_title(f"{title}\nlabel {side_label(img[None])[0]}", fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
note = fig.add_subplot(grid[1, :3])
note.axis("off")
note.text(0, 0.9, "label = 1 if the left half\n(left of the line) holds\nmore ink than the right",
          fontsize=9.5, color=INK_SECONDARY, va="top")
note.set_title("A. A label with exact symmetries", loc="left", fontsize=12)

sizes = (10, 20, 50, 100, 400)
res = augmentation_experiment(sizes)
ax = fig.add_subplot(grid[:, 4])
series = [
    ("none", "no augmentation", INK_SECONDARY, "-", "o"),
    ("invariant", "up-down flip (true invariance)", LEVER_COLOR["q"], "-", "s"),
    ("label_changing", "left-right flip, label reversed", LEVER_COLOR["q"], (0, (4, 2)), "D"),
    ("wrong_label", "left-right flip, label kept (false)", LEVER_COLOR["labels"], "-", "v"),
]
for key, label, color, style, marker in series:
    vals = res[key]
    ax.fill_between(sizes, np.nanpercentile(vals, 10, axis=0), np.nanpercentile(vals, 90, axis=0),
                    color=color, alpha=0.12, lw=0)
    ax.semilogx(sizes, np.nanmean(vals, axis=0), color=color, ls=style, marker=marker, ms=5,
                label=label)
ax.legend(loc="lower right", fontsize=9)
ax.axhline(0.5, color=MUTED, lw=0.8)
ax.annotate("chance", xy=(9, 0.5), xytext=(0, 3), textcoords="offset points", fontsize=8.5,
            color=INK_SECONDARY)
ax.set_xlim(8, 600)
ax.set_ylim(0.45, 1.0)
ax.set_xlabel("training images $n$")
ax.set_ylabel("test accuracy")
ax.set_title("B. Augmentation helps only if its assumption is true")

save_figure(fig, "augmentation")

m = {k: np.nanmean(v, axis=0) for k, v in res.items()}
publish("ch9", {
    "n_images": fmt(len(y)),
    "none_10": fmt(m["none"][0], 2), "inv_10": fmt(m["invariant"][0], 2),
    "chg_10": fmt(m["label_changing"][0], 2), "wrong_10": fmt(m["wrong_label"][0], 2),
    "none_400": fmt(m["none"][-1], 3), "inv_400": fmt(m["invariant"][-1], 3),
    "chg_400": fmt(m["label_changing"][-1], 3), "wrong_400": fmt(m["wrong_label"][-1], 2),
    "wrong_min": fmt(np.min(m["wrong_label"]), 2), "wrong_max": fmt(np.max(m["wrong_label"]), 2),
})
