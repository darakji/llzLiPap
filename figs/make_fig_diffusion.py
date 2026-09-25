"""Figure 5: (a) interior-Li mean-squared displacement, (b) Arrhenius plot of D.

Reads data/diffusion_by_T_<tag>.csv, data/diffusion_arrhenius_<tag>.csv and
data/msd_curves_<tag>_rep0.npz (copied verbatim from
alchemi_a100_package/results/campaign_midT_lid/{kinetics,msd_curves}/) and
writes figs/fig_diffusion.pdf/png.  Run:  python figs/make_fig_diffusion.py [tag]
"""
import csv, sys, os, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TAG = sys.argv[1] if len(sys.argv) > 1 else "3ns"
KB = 8.617333e-5  # eV/K

NAMES = {
    "seed1_420at_Li100_LLZO110_vac1pfu": ("Li(100)/LLZO(110), 1 vac", "C0", "o"),
    "seed2_536at_LLZO100ct_vac0p5pfu": ("Li(100)/LLZO(100)-ct, 0.5 vac", "C1", "s"),
    "seed3_792at_LLZO110ct_vac1pfu": ("Li(100)/LLZO(110)-ct, 1 vac", "C2", "^"),
    "seed4_1378at_Li111_LLZO001_vac0p5pfu": ("Li(111)/LLZO(001), 0.5 vac", "C3", "D"),
    "unseen_2frames_dftfe_labelled_idx0": ("Li(100)/LLZO(100)-ct, held-out", "C4", "v"),
    "unseen_2frames_dftfe_labelled_idx1": ("Li(100)/LLZO(110)-ct, held-out", "C5", "P"),
}
TCOL = {500: "#3E6B9F", 600: "#2E8B57", 700: "#D08A00", 800: "#8A2036"}

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", f"diffusion_by_T_{TAG}.csv"))))
arr = {r["structure"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", f"diffusion_arrhenius_{TAG}.csv")))}
msd_path = os.path.join(ROOT, "data", f"msd_curves_{TAG}_rep0.npz")
msd = np.load(msd_path) if os.path.exists(msd_path) else None

fig = plt.figure(figsize=(7.2, 3.4))
gs = gridspec.GridSpec(1, 2, width_ratios=[1.15, 1], wspace=0.28)

# ---- (a) MSD, six small panels sharing axes, uniform 2 ps frame spacing as lag axis
if msd is not None:
    gsa = gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=gs[0], wspace=0.08, hspace=0.55)
    axs = [fig.add_subplot(gsa[i // 3, i % 3]) for i in range(6)]
    curves = {}
    for k in msd.files:
        if not k.endswith("__lags"):
            continue
        label = k[:-6]
        m = re.match(r"(.+?)_f(\d+)_r(\d+)(?:_T(\d+)K)?$", label)
        curves.setdefault(m.group(1), {})[int(m.group(4))] = msd[label + "__msd"]
    for ax, (key, (name, col, mk)) in zip(axs, NAMES.items()):
        for T in (500, 600, 700, 800):
            y = curves.get(key, {}).get(T)
            if y is None:
                continue
            lag = np.arange(len(y)) * 2.0
            ok = (lag > 0) & (lag <= 1500)
            ax.loglog(lag[ok], y[ok], color=TCOL[T], lw=1.1, label=f"{T} K")
        ax.axvspan(10, 300, color="0.88", lw=0, zorder=0)
        xx = np.array([10, 1000]); ax.loglog(xx, 9 * xx / 100, "k:", lw=0.7)
        ax.set_xlim(2, 1600); ax.set_ylim(0.15, 200)
        ax.set_title(name.replace(", ", "\n"), fontsize=5.4, pad=1.5)
        ax.tick_params(labelsize=6, length=2, pad=1)
        ax.set_yticks([1, 10, 100]); ax.set_xticks([10, 100, 1000])
    for i, ax in enumerate(axs):
        if i % 3: ax.set_yticklabels([])
        if i < 3: ax.set_xticklabels([])
    axs[0].legend(fontsize=5, frameon=False, loc="upper left", handlelength=1.2, borderpad=0.2)
    axs[3].set_ylabel("MSD, interior Li (Å$^2$)", fontsize=7); axs[3].yaxis.set_label_coords(-0.3, 1.05)
    axs[4].set_xlabel("lag $\\tau$ (ps)", fontsize=7)
    axs[0].text(-0.42, 1.18, "a", transform=axs[0].transAxes, fontsize=10, fontweight="bold")
    axb = fig.add_subplot(gs[1])
else:
    axb = fig.add_subplot(111)

# ---- (b) Arrhenius
ax = axb
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
                        mfc=fill, mec=col, ms=4.5, capsize=2, lw=1, label=name if fill == col else None)
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
ax.set_xlabel("1000 / T (K$^{-1}$)", fontsize=8)
ax.set_ylabel("$D_{\\mathrm{Li}}$, electrolyte interior (cm$^2$/s)", fontsize=8)
ax.set_xlim(1.15, 3.45); ax.tick_params(labelsize=7)
sec = ax.secondary_xaxis("top", functions=(lambda x: 1000 / np.maximum(x, 1e-9), lambda T: 1000 / np.maximum(T, 1e-9)))
sec.set_xticks([800, 700, 600, 500, 400, 300]); sec.set_xlabel("T (K)", fontsize=8); sec.tick_params(labelsize=7)
ax.legend(fontsize=5.6, frameon=False, loc="lower left")
ax.text(0.98, 0.97, "filled: diffusive ($\\alpha\\geq0.6$)\nopen: caged, upper bound", transform=ax.transAxes,
        ha="right", va="top", fontsize=6)
if msd is not None:
    ax.text(-0.22, 1.05, "b", transform=ax.transAxes, fontsize=10, fontweight="bold")
fig.subplots_adjust(left=0.09, right=0.99, top=0.86, bottom=0.14)
out = os.path.join(HERE, "fig_diffusion.pdf")
fig.savefig(out); fig.savefig(out.replace(".pdf", ".png"), dpi=220)
print("wrote", out)
