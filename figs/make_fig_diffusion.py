"""Figure 5: Arrhenius plot of the interior Li diffusion coefficient.

Reads data/diffusion_by_T_<tag>.csv and data/diffusion_arrhenius_<tag>.csv
(copied verbatim from alchemi_a100_package/results/campaign_midT_lid/kinetics/)
and writes figs/fig_diffusion.pdf.  Run:  python figs/make_fig_diffusion.py [tag]
"""
import csv, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TAG = sys.argv[1] if len(sys.argv) > 1 else "1ns"
KB = 8.617333e-5  # eV/K

NAMES = {
    "seed1_420at_Li100_LLZO110_vac1pfu": ("Li(100)/LLZO(110), 1 vac", "C0", "o"),
    "seed2_536at_LLZO100ct_vac0p5pfu": ("Li(100)/LLZO(100)-ct, 0.5 vac", "C1", "s"),
    "seed3_792at_LLZO110ct_vac1pfu": ("Li(100)/LLZO(110)-ct, 1 vac", "C2", "^"),
    "seed4_1378at_Li111_LLZO001_vac0p5pfu": ("Li(111)/LLZO(001), 0.5 vac", "C3", "D"),
    "unseen_2frames_dftfe_labelled_idx0": ("Li(100)/LLZO(100)-ct, held-out", "C4", "v"),
    "unseen_2frames_dftfe_labelled_idx1": ("Li(100)/LLZO(110)-ct, held-out", "C5", "P"),
}

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", f"diffusion_by_T_{TAG}.csv"))))
arr = {r["structure"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", f"diffusion_arrhenius_{TAG}.csv")))}

fig, ax = plt.subplots(figsize=(4.6, 3.6))
Tgrid = np.linspace(280, 850, 200)
for key, (name, col, mk) in NAMES.items():
    rs = [r for r in rows if r["structure"] == key]
    if not rs:
        continue
    T = np.array([float(r["T_K"]) for r in rs])
    D = np.array([float(r["D_int_tot_cm2s_mean"]) for r in rs])
    S = np.array([float(r["D_int_tot_cm2s_std"]) for r in rs])
    al = np.array([float(r["alpha_int_mean"]) for r in rs])
    diff = al >= 0.6
    lo = np.clip(D - S, 0.2 * D, None)
    for m, fill in ((diff, col), (~diff, "white")):
        if m.any():
            ax.errorbar(1000 / T[m], D[m], yerr=[D[m] - lo[m], S[m]], fmt=mk, color=col,
                        mfc=fill, mec=col, ms=5, capsize=2, lw=1, label=name if fill == col else None)
    a = arr.get(key)
    if a:
        Ea = float(a["Ea_D_meV"]) / 1000; D0 = float(a["D0_cm2s"])
        ax.plot(1000 / Tgrid, D0 * np.exp(-Ea / (KB * Tgrid)), color=col, lw=0.8, alpha=0.6)
# tetragonal LLZO experiment (Awaka et al. 2009): sigma(300 K) = 1.63e-6 S/cm, Ea = 0.54 eV,
# converted to D with n(Li) = 2.56e22 cm^-3 (Nernst-Einstein, Haven ratio 1)
D300 = 1.03e-11
ax.plot(1000 / Tgrid, D300 * np.exp(-0.54 / KB * (1 / Tgrid - 1 / 300)), "k--", lw=1.2,
        label="t-LLZO expt. (Awaka 2009)")
ax.set_yscale("log")
ax.set_xlabel("1000 / T (K$^{-1}$)")
ax.set_ylabel("$D_{\\mathrm{Li}}$, electrolyte interior (cm$^2$/s)")
ax.set_xlim(1.15, 3.45)
sec = ax.secondary_xaxis("top", functions=(lambda x: 1000 / np.maximum(x, 1e-9), lambda T: 1000 / np.maximum(T, 1e-9)))
sec.set_xticks([800, 700, 600, 500, 400, 300]); sec.set_xlabel("T (K)")
ax.legend(fontsize=6.5, frameon=False, loc="lower left")
ax.text(0.98, 0.97, "filled: diffusive ($\\alpha\\geq0.6$)\nopen: caged, upper bound", transform=ax.transAxes,
        ha="right", va="top", fontsize=6.5)
fig.tight_layout()
out = os.path.join(HERE, "fig_diffusion.pdf")
fig.savefig(out); fig.savefig(out.replace(".pdf", ".png"), dpi=200)
print("wrote", out)
