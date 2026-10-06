"""Supplementary figure: stratified random audit of 50 MD snapshots (0-5 ns).
(a) each hard check as a fraction of its pass limit, one dot per snapshot;
(b) one side view per 0.5 ns time window.
Inputs: data/snapshot_audit.csv, data/snapshot_audit_50.extxyz (from scripts/13_snapshot_audit.py)."""
import csv, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import read

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data")
R = list(csv.DictReader(open(os.path.join(DATA, "snapshot_audit.csv"))))
frames = read(os.path.join(DATA, "snapshot_audit_50.extxyz"), ":")
COV = {"Li": 1.28, "O": 0.66, "La": 2.07, "Zr": 1.75}
PAIRS = {"LiLi": ("Li", "Li"), "LiO": ("Li", "O"), "ZrO": ("Zr", "O"), "LaO": ("La", "O"), "OO": ("O", "O")}
f = lambda r, k: float(r[k])

def contact(r):
    return max(0.6 * (COV[a] + COV[b]) / f(r, "dmin_" + k) for k, (a, b) in PAIRS.items() if r["dmin_" + k] != "nan")

def leak(r, at):
    n_ox = sum(s in ("La", "Zr", "O") for s in at.get_chemical_symbols())
    return f(r, "ox_into_metal") / (0.05 * n_ox)

rows = [("Closest atom pair", [contact(r) for r in R], "0.6 × covalent-radius sum"),
        ("Max force, mobile atoms", [f(r, "fmax") / 10 for r in R], "10 eV/Å"),
        ("Kinetic T vs target", [abs(f(r, "T_mobile") / f(r, "T") - 1) / 0.20 for r in R], "±20 %"),
        ("Energy jump", [abs(f(r, "E_z")) / 5 for r in R], "5 robust s.d."),
        ("La/Zr/O into metal", [leak(r, a) for r, a in zip(R, frames)], "5 % of framework"),
        ("Frozen-atom move", [f(r, "frozen_moved_A") / 0.5 for r in R], "0.5 Å"),
        ("Interface-plane shift", [abs(f(r, "zif_shift_A")) / 3 for r in R], "3 Å"),
        ("Interior LLZO rms (8–15 Å)", [f(r, "rms_8_15") / 0.75 for r in R], "0.75 Å")]

INK, MUTED, MARK, LIMIT = "#1B2026", "#7B838C", "#3E6B9F", "#8A2036"
COLORS = {"Li": "#5aa0d8", "O": "#e0453f", "La": "#3c9b4c", "Zr": "#8e6bbf"}
fig = plt.figure(figsize=(7.2, 7.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.25], hspace=0.18)
ax = fig.add_subplot(gs[0])
rng = np.random.default_rng(0)
for k, (name, v, lim) in enumerate(rows):
    y = len(rows) - 1 - k
    ax.scatter(v, y + rng.uniform(-0.18, 0.18, len(v)), s=10, color=MARK, alpha=0.75, linewidths=0)
    ax.text(1.04, y, lim, va="center", fontsize=7, color=MUTED)
ax.axvline(1.0, color=LIMIT, lw=1.2); ax.text(0.98, len(rows) - 0.45, "pass limit", color=LIMIT, fontsize=7, ha="right")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.5)
ax.set_xlim(0, 1.32); ax.set_ylim(-0.6, len(rows) - 0.1); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xlabel("value / pass limit (50 snapshots)", fontsize=8); ax.tick_params(labelsize=7.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(axis="x", color="#D3D8D6", lw=0.5); ax.set_axisbelow(True)
ax.text(-0.36, 1.02, "a", transform=ax.transAxes, fontsize=11, fontweight="bold")

seen = []
for r, at in zip(R, frames):
    if r["bucket"] not in [x[0] for x in seen]:
        seen.append((r["bucket"], r, at))
seen = seen[:10]
widths = [at.cell[0, 0] for _, _, at in seen]
zs = [at.positions[:, 2] - at.positions[:, 2].min() for _, _, at in seen]
H = max(z.max() for z in zs) + 1.0
sub = gs[1].subgridspec(1, 10, wspace=0.12, width_ratios=widths)
for j, ((b, r, at), z) in enumerate(zip(seen, zs)):
    a = fig.add_subplot(sub[j]); x = at.positions[:, 0] % at.cell[0, 0]; sym = np.array(at.get_chemical_symbols())
    for s in ("Li", "O", "Zr", "La"):
        m = sym == s; a.scatter(x[m], z[m], s={"Li": 1.2, "O": 1.0, "La": 3, "Zr": 2.2}[s], c=COLORS[s], linewidths=0, label=s)
    a.set_xlim(0, at.cell[0, 0]); a.set_ylim(-0.5, H); a.set_aspect("equal", anchor="S"); a.axis("off")
    a.set_title(f"{float(r['t_ns']):.2f} ns\n{r['cell']}\n{r['T']} K", fontsize=5.8, color=INK)
    if j == 0:
        a.text(-0.9, 1.0, "b", transform=a.transAxes, fontsize=11, fontweight="bold", va="bottom")
        a.plot([-2, -2], [0, 10], color=INK, lw=1, clip_on=False); a.text(-3, 5, "10 Å", rotation=90, fontsize=6, ha="right", va="center", clip_on=False)
h, l = fig.axes[1].get_legend_handles_labels()
fig.legend([plt.Line2D([], [], ls="", marker="o", color=COLORS[s], ms=4) for s in l], l, loc="lower center", ncol=4, fontsize=7, frameon=False, bbox_to_anchor=(0.5, 0.02))
fig.savefig(os.path.join(HERE, "fig_snapshot_audit.pdf"), bbox_inches="tight")
fig.savefig(os.path.join(HERE, "fig_snapshot_audit.png"), dpi=200, bbox_inches="tight")
for name, v, lim in rows: print(f"{name:28s} max {max(v):.2f}")
