"""Figure 4: acquisition validation -- Gaussian-process posterior variance
computed in the it5 latent space BEFORE labelling, against the force and energy
error subsequently measured against DFT-FE on the newly labelled structures.

Reads data/uq_pv_vs_error_35.csv (PV at lambda=0.1 recomputed from
it5_final/latent_extraction/{seed_embeddings_it5_77train,combined_pool_it5_latents_meanpool}.jsonl,
errors from it6_final/uq_fps_validation/testB_errors_35.csv) and writes
figs/fig_uq.pdf/png.  Run:  python figs/make_fig_uq.py
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "uq_pv_vs_error_35.csv"))))
pv = np.array([float(r["pv"]) for r in rows])
fr = np.array([float(r["f_rmse_meV_A"]) for r in rows])
em = np.array([float(r["e_mae_meV_atom"]) for r in rows])
is_fps = np.array([r["it6_set"] == "fps31" for r in rows])

GROUPS = [(is_fps, "FPS selections (31)", "#2E5E8E", "o"),
          (~is_fps, "held-out labels (4)", "#B5651D", "^")]


def pearson(x, y):
    xc, yc = x - x.mean(), y - y.mean()
    return float(xc @ yc / np.sqrt((xc @ xc) * (yc @ yc)))


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
PANELS = [(axes[0], fr, "it5 force RMSE (meV/Å)", "a"),
          (axes[1], em, "it5 energy MAE (meV/atom)", "b")]

for ax, y, ylab, tag in PANELS:
    # least-squares line over all 35 points
    s, i = np.polyfit(pv, y, 1)
    xs = np.linspace(pv.min(), pv.max(), 50)
    ax.plot(xs, s * xs + i, color="0.35", lw=1.1, zorder=1)
    for mask, lab, col, mk in GROUPS:
        ax.scatter(pv[mask], y[mask], s=26, c=col, marker=mk, lw=0.5,
                   edgecolors="white", label=lab, zorder=3)
    ax.set_xlabel("posterior variance before labelling (arb.)")
    ax.set_ylabel(ylab)
    ax.text(0.04, 0.93, f"$r={pearson(pv, y):+.2f}$", transform=ax.transAxes,
            va="top", fontsize=10)
    ax.text(-0.22, 1.04, tag, transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="top")
    ax.grid(alpha=0.25, lw=0.5)
    ax.set_axisbelow(True)

axes[0].legend(frameon=False, fontsize=8, loc="lower right")
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, f"fig_uq.{ext}"), dpi=200, bbox_inches="tight")
print("n =", len(rows),
      "| r_force =", round(pearson(pv, fr), 4),
      "| r_energy =", round(pearson(pv, em), 4))
