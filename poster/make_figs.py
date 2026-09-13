"""Generate the poster's data figures as vector PDFs, from the real data."""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/scratch/users/phanim/mehuldarak/it6_final/poster/figs"
LLZO, LIM, ACC, GOOD, INK, DIM = "#2f4f70", "#7d745f", "#a02a44", "#276b55", "#12181e", "#7a848d"

plt.rcParams.update({
    "font.family": "serif", "font.size": 15,
    "axes.edgecolor": INK, "axes.linewidth": 1.0,
    "xtick.color": INK, "ytick.color": INK, "text.color": INK, "axes.labelcolor": INK,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
})

# ---------------- 1. latent map, full pool ----------------
D = json.load(open("/scratch/users/phanim/mehuldarak/it6_final/epoch_sweep/fps_figure_data.json"))
fig, ax = plt.subplots(figsize=(9.2, 6.2))
ax.scatter(D["pool_x"], D["pool_y"], s=0.55, c="#9aa8b4", alpha=0.30, linewidths=0,
           rasterized=True, label=f"candidate pool ({D['n_pool']:,})")
ax.scatter(D["seed_x"], D["seed_y"], s=42, c=LLZO, linewidths=0, label="already labelled (77)")
ax.scatter(D["sel_x"], D["sel_y"], s=95, facecolors="none", edgecolors=ACC, linewidths=2.0,
           label="FPS-selected (31)")
ax.set_xlabel(f"PC1  ({D['evr'][0]*100:.1f}% of variance)", labelpad=2)
ax.set_ylabel(f"PC2   ({D['evr'][1]*100:.1f}%)")
ax.set_xticks([]); ax.set_yticks([])
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3, frameon=False,
          fontsize=13, handletextpad=.5, columnspacing=1.4)
fig.savefig(f"{OUT}/fig_latent.pdf", dpi=300); plt.close(fig)

# ---------------- 2. coverage radius vs FPS step ----------------
rows = [l.split(",") for l in open(
    "/scratch/users/phanim/mehuldarak/it5_final/latent_extraction/fps_coverage_curve.csv").read().strip().split("\n")[1:]]
step = [int(r[0]) for r in rows if r[2]]
rho  = [float(r[2]) for r in rows if r[2]]
d99  = 0.020844862338889197
fig, ax = plt.subplots(figsize=(7.6, 4.9))
ax.plot(step, rho, "-", color=LLZO, lw=2.4)
ax.plot(step[0], rho[0], "o", color=LLZO, ms=8)
ax.plot(step[-1], rho[-1], "o", color=ACC, ms=10)
ax.axhline(d99, color=ACC, ls="--", lw=1.8)
ax.text(step[-1], d99 - 0.0009, "d99 threshold = 0.0208", ha="right", va="top", color=ACC, fontsize=13)
ax.annotate(f"{rho[0]:.4f}", (step[0], rho[0]), xytext=(9, 2), textcoords="offset points", fontsize=13, color=DIM)
ax.set_xlabel("FPS structures added"); ax.set_ylabel(r"coverage radius  $\rho=\max_k\,\delta_k$")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.savefig(f"{OUT}/fig_coverage.pdf"); plt.close(fig)

# ---------------- 3. error trend, dual axis ----------------
models = ["univ", "it0", "it1", "it2", "it3", "it4", "it5", "it6"]
rms = [120.5, 188.2, 118.4, 97.2, 92.5, 84.2, 78.2, 72.0]
mc  = [799.5, 1315.5, 782.6, 658.3, 624.2, 575.9, 523.6, 482.5]
x = np.arange(len(models))
fig, ax = plt.subplots(figsize=(7.6, 4.9))
ax.plot(x, rms, "-o", color=LLZO, lw=2.4, ms=7, label=r"$\Delta F$ rms mean")
ax.plot(x[-1], rms[-1], "o", color=ACC, ms=12, zorder=5)
ax.annotate("72.0", (x[-1], rms[-1]), xytext=(-6, -20), textcoords="offset points",
            fontsize=15, color=ACC, fontweight="bold", ha="center")
ax.set_ylabel(r"$\Delta F$ rms  (meV/$\mathrm{\AA}$)", color=LLZO)
ax.tick_params(axis="y", colors=LLZO); ax.set_ylim(0, 200)
ax2 = ax.twinx()
ax2.plot(x, mc, "--s", color=LIM, lw=2.0, ms=6, label=r"$\Delta F$ max-comp mean")
ax2.set_ylabel(r"$\Delta F$ max-component  (meV/$\mathrm{\AA}$)", color=LIM)
ax2.tick_params(axis="y", colors=LIM); ax2.set_ylim(0, 1400)
ax.set_xticks(x); ax.set_xticklabels(models)
ax.get_xticklabels()[-1].set_color(ACC); ax.get_xticklabels()[-1].set_fontweight("bold")
for sp in ("top",): ax.spines[sp].set_visible(False); ax2.spines[sp].set_visible(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False, fontsize=13)
fig.savefig(f"{OUT}/fig_error.pdf"); plt.close(fig)

# ---------------- 4. campaign: pool screened per round ----------------
rounds = ["it1→it2", "it2→it3", "it3→it4", "it4→it5", "it5→it6"]
pool   = [5429, 7200, 18000, 321361, 62029]
added  = [5, 5, 9, 30, 31]
fig, ax = plt.subplots(figsize=(7.6, 4.4))
cols = [LLZO]*4 + [ACC]
ax.barh(range(len(rounds)), pool, color=cols, alpha=.85, height=.62)
ax.set_xscale("log"); ax.set_xlim(1e3, 6e5)
ax.set_yticks(range(len(rounds))); ax.set_yticklabels(rounds)
ax.invert_yaxis()
ax.set_xlabel("configurations screened (log scale)")
for i, (p, a) in enumerate(zip(pool, added)):
    ax.annotate(f"{p:,}   →  +{a}", (p, i), xytext=(8, 0), textcoords="offset points",
                va="center", fontsize=13, color=INK)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.savefig(f"{OUT}/fig_campaign.pdf"); plt.close(fig)

print("figures written to", OUT)
