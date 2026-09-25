"""Supplementary Figure S1: interface chemistry at 800 K after about 3 ns.

(a) fraction of Zr with fewer than six O neighbours (within 2.6 A) at the
contact (+-3 A band about the interface plane) and in the interior; (b) interior
hop rate (displacement > 2 A within 2 ps) per Li per ns with the cooperative
share; (c) framework atoms more than 2 A above the interface plane at the end
of the run.  Values are means over five replicas, transcribed from
data/chemistry_report_3ns.md (alchemi_a100_package/results/campaign_midT_lid/
chemistry/report.md).  Run:  python figs/make_fig_chemistry.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SHORT = ["(110)\n1 vac", "(100)-ct\n0.5 vac", "(110)-ct\n1 vac", "(001)\n0.5 vac", "(100)-ct\nheld-out", "(110)-ct\nheld-out"]
COLS = ["C0", "C1", "C2", "C3", "C4", "C5"]
ucZr_if = [0, 55, 95, 37, 56, 0]        # % undercoordinated Zr, +-3 A band, 800 K
ucZr_int = [1, 2, 1, 2, 1, 0]           # % undercoordinated Zr, interior, 800 K
O_above = [0.6, 0.2, 1.2, 1.0, 0.0, 3.2]  # O atoms > 2 A above the plane at the end
hops = [5.7, 15.7, 12.1, 41.1, 4.2, 10.7]  # interior hops per Li per ns, 800 K
coop = [23, 3, 7, 18, 26, 15]           # % of hops with a neighbour hopping in the same window
x = np.arange(6)

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.5))
ax = axs[0]
ax.bar(x - 0.2, ucZr_if, 0.4, color="#8A2036", label="contact ($\\pm$3 Å)")
ax.bar(x + 0.2, ucZr_int, 0.4, color="#3E6B9F", label="interior")
ax.set_ylabel("Zr with < 6 O neighbours (%)", fontsize=7); ax.legend(fontsize=6, frameon=False)
ax.text(-0.25, 1.04, "a", transform=ax.transAxes, fontsize=10, fontweight="bold")
ax = axs[1]
ax.bar(x, hops, color=COLS)
for i, c in enumerate(coop):
    ax.text(i, hops[i] + 0.8, f"{c}%", ha="center", fontsize=6)
ax.set_ylabel("interior hops per Li per ns", fontsize=7); ax.set_ylim(0, 48)
ax.text(0.98, 0.97, "labels: cooperative share", transform=ax.transAxes, ha="right", va="top", fontsize=6)
ax.text(-0.25, 1.04, "b", transform=ax.transAxes, fontsize=10, fontweight="bold")
ax = axs[2]
ax.bar(x - 0.2, O_above, 0.4, color="#D44", label="O")
ax.bar(x + 0.2, [0] * 6, 0.4, color="#7B4", label="Zr, La (zero)")
ax.set_ylabel("framework atoms > 2 Å above plane", fontsize=7); ax.set_ylim(0, 5); ax.legend(fontsize=6, frameon=False)
ax.text(-0.25, 1.04, "c", transform=ax.transAxes, fontsize=10, fontweight="bold")
for ax in axs:
    ax.set_xticks(x); ax.set_xticklabels([s.replace("\n", " ") for s in SHORT], fontsize=5.2, rotation=30, ha="right"); ax.tick_params(axis="y", labelsize=6.5); ax.grid(axis="y", alpha=.25, lw=.4)
fig.tight_layout()
out = os.path.join(HERE, "fig_chemistry.pdf")
fig.savefig(out); fig.savefig(out.replace(".pdf", ".png"), dpi=220)
print("wrote", out)
