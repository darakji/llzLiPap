# Complete context for editing `npj_v0_template.tex`

Single-file handoff. If you are an agent picking up this manuscript, read this
top to bottom before touching the `.tex`. Everything you need to make correct
edits is here; the three companion documents are `SI_notes.md` (in this repo,
material deliberately cut from the paper) and
`/scratch/users/phanim/mehuldarak/it5_final/MASTER_SUMMARY.md` (~2000 lines,
the project's full audit trail and the provenance of every number below).

Written 2026-09-25. Manuscript at commit `f53e109`.

---

## 1. What this paper is

**Target venue:** npj Computational Materials, Article type.

**The narrative, decided and not open for reinterpretation:**

> Latent-space-driven active learning with DFT-FE for solid-state battery
> interfaces — application to the Li-metal/LLZO interface.

This is a **method paper with two components**, demonstrated on one system. It
is *not* a "here is our Li/LLZO potential" paper. The two components are:

1. **Open-boundary reference labels at deployment scale.** DFT-FE (real-space
   finite-element Kohn–Sham) supports mixed boundary conditions, so slabs are
   periodic in x,y and genuinely **open in z**. Plane-wave DFT cannot do this:
   it needs a periodic sandwich or a dipole-corrected slab, neither of which is
   a free surface. Training cells are 420–1378 atoms — the same size as the
   production MD, so there is no cell-size extrapolation to make.
2. **Latent-space coverage-driven acquisition.** Candidates from MLIP-driven MD
   are embedded in the pretrained MACE model's own latent space; farthest-point
   sampling seeded on the already-labelled set picks what most reduces
   worst-case coverage distance. Stopping is by pool coverage, not by quota.

Each component has an internal validation, and these are the paper's real
results — more important than the aggregate error number:

- **Error localisation validates component 1.** Residual force error sits at
  **2.05×** the frame mean on the outermost vacuum-facing LLZO layer — exactly
  the environment a periodic training cell cannot contain. A conventionally
  trained potential would be weakest where its own validation set is blind.
- **r = 0.85 validates component 2.** Latent-space uncertainty computed *before
  labelling* predicts the DFT force error subsequently measured on those
  structures. This answers the standing objection that diversity-based
  acquisition selects on geometric novelty rather than model deficiency.

**Do not** restructure toward "DFT-FE is the hero" (an earlier framing, now
superseded) or toward "active learning only" (the Overleaf title, superseded).
Both were considered; the current title carries all three elements
deliberately.

---

## 2. Repo, branches, build

**Working clone:** `/scratch/users/phanim/mehuldarak/paper`

| remote | URL | default branch |
|---|---|---|
| `origin` | `github.com/matrixlabiisc/mdMatrixLLZOPaper` | `master` |
| `privMeh` | `github.com/darakji/llzLiPap` | `main` |

Work happens on **`main`**, and `main` is pushed to **both** remotes. Keep
doing that — they are currently identical.

⚠️ Two traps:
- `origin/master` is the GitHub default branch but is **stale** (still at the
  original v0 template, `e1d453b`). Unresolved; do not "fix" it by merging
  without asking.
- Local `main` is configured to track **`privMeh`**, not `origin`
  (`branch.main.remote = privMeh`). A bare `git push` goes to the *private*
  repo. Always push explicitly: `git push origin main` and `git push privMeh main`.

**Overleaf:** branch `privMeh/overleaf-2026-09-24-1735` was merged into `main`
at `e95c220` (it supplied the real author list). If Overleaf syncing continues,
that branch will re-diverge from `e1d453b` unless the merge is pulled back into
Overleaf.

**Building the PDF.** `tectonic` is at
`/scratch/users/phanim/mehuldarak/miniconda3/envs/tex/bin/tectonic`.

```bash
# never run on the login node -- take an allocation first
srun --partition=short --account=research --qos=normal --gres=gpu:1 \
     --cpus-per-task=4 --mem=32G --time=1:00:00 --job-name=tex sleep infinity &
JID=$(squeue -u $USER -h -n tex -o "%i")
srun --jobid=$JID --overlap -n1 bash -lc \
  'export PATH=/scratch/users/phanim/mehuldarak/miniconda3/envs/tex/bin:$PATH
   cd <workdir> && tectonic npj_v0_template.tex'
scancel $JID
```

`ssh cn2` does **not** work (no SSH keypair in the home dir). Use
`srun --jobid=<id> --overlap` to run on an allocated node. `/tmp` is node-local
and not shared, so stage files under `/scratch`, not `/tmp`.

**Do not run anything on the login node.** Standing instruction from the user.

**GPU/conda:** `source /scratch/users/phanim/mehuldarak/miniconda3/etc/profile.d/conda.sh`
then `conda activate mace_cueq_env`. Note that env does **not** actually have
`cuequivariance` installed despite the name, so `enable_cueq=True` raises
`RuntimeError: Unexpected key(s) ... symmetric_contractions.weight`. Load the
model without it.

---

## 3. Current state of the manuscript

Main text ≈ **2,930 words** against the npj limit of **5,000**, so there is
~2,000 words of headroom — deliberately reserved for the diffusion results.
Compiles clean under tectonic.

| section | state |
|---|---|
| Title / authors / affiliations | Done. Corresponding author still unmarked (TODO, probably Prof. Motamarri) |
| Abstract | Done except closing sentence, which waits on diffusion |
| Introduction | Done |
| Results — Open-boundary reference data | Done |
| Results — Active-learning campaign | Done |
| Results — Accuracy | Done, Table 1 populated |
| Results — Residual error at the free surface | Done |
| Results — Acquisition signal predicts DFT error | Done |
| Results — Domain of validity | Done |
| **Results — Diffusion-coefficient validation** | **STUB. This is the job.** |
| Discussion | Done, incl. "Transfer to other systems" |
| Methods — all subsections | Done except interface-construction detail and diffusion protocol |
| References | 10 entries, 5 are `[TODO]` placeholders |
| Figure legends | 5 figures defined; 3 need building, 1 waits on diffusion |

**Display-item budget is FULL: 5 figures + 1 table = 6, and npj allows 6
combined.** Adding a figure means removing one. Do not silently exceed this.

---

## 4. The job: filling in the diffusion validation

Three places must be edited together, and they must agree:

1. **`\subsection{Diffusion-coefficient validation}`** (line ~333) — replace
   the whole `[TODO ...]` block with real prose.
2. **`\paragraph{Figure 5.}`** in Figure Legends (line ~666) — replace the
   `[TODO]`; label is already `\label{fig:msd}` and is referenced from the
   Results stub, so keep the label.
3. **Abstract closing sentence** (line ~114) — one sentence, and it must not
   overclaim relative to what the statistics support.

Also finish `\subsection{Diffusion analysis}` in Methods (line ~541): fitting
window, number of independent seeds, temperature set, Arrhenius extrapolation.

### What is currently in the stub, and why it is not a result

Single-trajectory, no error bars:

| region | this work (1 seed) | literature-extrapolated |
|---|---|---|
| LLZO | ~9–11 × 10⁻⁷ cm²/s | ~2.3 × 10⁻⁶ cm²/s |
| Li metal | ~4.1 × 10⁻⁴ cm²/s | ~6 × 10⁻⁴ – 1.2 × 10⁻³ cm²/s |

Agreement within 2–3× for both regions. **These numbers are in the draft
explicitly marked as not-a-result.** They must be replaced by multi-seed values
with genuine error bars, not merely re-stated. If the multi-seed runs disagree
with the single-seed numbers, report the multi-seed values — do not reconcile.

### Non-negotiable analysis conventions

These are established project conventions. Deviating from them silently will
produce wrong numbers that look plausible.

- **Unwrap before any MSD.** Trajectories are stored wrapped in x,y
  (`s5_MD.py:204` and the package's `03_md_ase_reference.py:66` both call
  `atoms.wrap(pbc=[True,True,False])`). Wrapped MSD saturates near
  `L²/6 ≈ 21 Å²` per dimension in the smallest cells — reached within tens of
  ps at 1100 K.
- **Unwrap in fractional coordinates, not with a diagonal box.** One of the MD
  seeds has **γ = 111.54°**. `diffusion_coeff.py` uses
  `box_xy = [cell[0,0], cell[1,1]]`, which is wrong for that cell and injects
  spurious ~4 Å displacements. Correct form:
  ```python
  frac  = pos_xy @ np.linalg.inv(cell_xy)
  dfrac = np.diff(frac, axis=0); dfrac -= np.round(dfrac)
  disp  = dfrac @ cell_xy
  ```
  Unwrapping is unambiguous at the 100 fs snapshot interval (RMS Li
  displacement ≈ 0.2 Å ≪ half-cell 5.6 Å).
- **Do not apply a centre-of-mass drift correction.** The bottom LLZO is frozen
  (`FixAtoms`), so the frame is already pinned. Li is 55–70 % of the atoms, so
  subtracting an all-atom COM removes part of the real Li flux.
- **Exclude z from the fit.** It is confined by slab thickness, not freely
  diffusing. `D_2D = slope/4`. Use z only for region assignment.
- **Assign regions relative to the measured interface plane per frame**, i.e.
  `max(z)` over La/Zr/O, not a fixed height. `diffusion_coeff.py` hardcodes
  `BOUNDARY_Z = 36.0`, correct for exactly one structure; the seeds have z
  ranges spanning 6.8–62.7 Å and vacuum 12.7–36 Å, so a constant is wrong for
  most of them.
- **Exclude atoms frozen by the active-region constraint** from the mobile
  population.
- **Exclude region-crossers** from a lag window, for both regions.
- Use **multiple time origins**.

**Caveat worth stating in the paper:** Langevin friction is 10⁻³ fs⁻¹ = 1 ps⁻¹,
which is on the strong side for transport and will suppress D somewhat relative
to NVE. Fine for comparing structures under identical settings; must be
declared if an absolute D is quoted.

**Existing script:** `it5_final/snapshot_analysis_LLZO100/diffusion_coeff.py`.
It gets multi-origin averaging, crosser exclusion and z-exclusion right, and
gets the two things above (diagonal unwrap, hardcoded boundary) wrong. Fix
rather than rewrite from scratch.

---

## 5. Every number in the manuscript, with provenance

Do not change any of these without checking `MASTER_SUMMARY.md`. They have been
cross-checked and several are the corrected version of an earlier wrong number.

### Dataset
- **108** training structures, **33** held-out (in-domain). All are independent
  DFT-FE single-point calculations.
- **420–1378 atoms**; in-plane cell vectors **11.3–26.4 Å**; z extent
  **52–80 Å** (finite-element domain padding, *not* image separation).
- `pbc = [True, True, False]` on every frame, verified.
- Candidate pool in the final round: **62,029** frames.
- Seed-only coverage before the final round: **98.999 %**; **31** structures
  closed it.

### Accuracy (Table 1, 33-structure in-domain set)
Source: `it6_final/epoch_sweep/test35_indomain_33_comparison.csv`.
Component-wise force RMSE / MAE in meV/Å.

| model | RMSE mean | RMSE max | MAE mean | MAE max |
|---|---|---|---|---|
| universal | 121.2 | 201.9 | 69.9 | 114.4 |
| it0 | 188.1 | 330.4 | 100.8 | 168.8 |
| it1 | 117.2 | 167.8 | 68.8 | 99.0 |
| it2 | 94.6 | 163.7 | 57.7 | 100.5 |
| it3 | 90.5 | 158.2 | 55.6 | 99.0 |
| it4 | 83.7 | 128.9 | 51.5 | 81.9 |
| it5 | 77.2 | 112.9 | 47.5 | 72.1 |
| **it6** | **72.4** | **99.9** | **45.1** | **59.0** |

- Tail vs mean across the campaign: worst per-structure RMSE **−70 %**,
  across-structure std **−82 %**, mean **−62 %**.
- it5→it6 paired Wilcoxon: **77.2 → 72.4 meV/Å, p = 0.008**, better on **24/33**.
- Energy: flat at **~4 meV/atom** since it2; it5 3.80 vs it6 4.14, **p = 0.50 (ns)**.

### Error localisation
- Zr+La are **15.4 %** of atoms, hold **77.8 %** of worst-percentile squared error.
- Mean component-wise |ΔF|: Zr **102.3**, La **83.4**, O **58.3**, Li **25.1** meV/Å.
- Li is **47.8 %** of atoms.
- Outermost vacuum-facing LLZO layer: **2.05×** frame mean, range **0.98–3.79×**.
- Per-atom source array: `it5_final/it5_per_atom_raw.npz`.

### Acquisition validation
- Pre-round posterior variance vs realised DFT error: **r = +0.847 force**,
  **+0.777 energy**, p ≤ 2.3 × 10⁻⁸.
- Leave-one-out range **[+0.82, +0.87]**; bootstrap 95 % CI **[+0.69, +0.93]**.
- Restricting to the 31 FPS picks alone: +0.839 / +0.784 (not a two-cluster artifact).
- Size confound: r(n_atoms, error) = −0.03; partial correlation unchanged at +0.850.
- Selected set exceeded **all 1000** random 31-subsets.
- Spearman(PV, FPS criterion) over the pool: **+0.10 to +0.16** only; top-31 overlap **10–11/31**.
- Scripts: `it6_final/uq_fps_validation/`.

### Domain of validity
- Training set: **0** structures above 1 vacancy/f.u. (12 at 0.5, 19 at 1, 77 undoped).
- Held-out 2 vac/f.u. probe: **252.6 meV/Å** (it6) vs **72.4** in-domain. it5 gives 266.3.

### Label quality
- Neumann vs zero-Dirichlet electrostatic BC: ΔE = O(10⁻⁶) Ha, max ΔF ≈ **2.6 meV/Å**.
- DFT-FE label noise from an accidental duplicate: **0.06 meV/atom**, **0.12 meV/Å**.
- Leak detection: two contaminated frames agreed with training frames to
  **6.5 × 10⁻⁶** and **1.8 × 10⁻⁶** meV/atom; removed.

### Training hyperparameters (identical every iteration)
Foundation `mace-omat-0-medium`; LoRA rank 5, α = 1; w_E = 1.0, w_F = 5.0;
batch 8; lr 5e-3 with ReduceLROnPlateau (factor 0.8, patience 50); 1500 epochs,
SWA from 1000 at lr 1e-4; seed 42; **float32**; checkpoint by best validation loss.
E0 (eV): Li −190.7590256408, O −442.9888796243, Zr −1380.1817128081,
La −958.0774205521.
Every iteration fine-tunes **the foundation model**, never the previous iteration.

### DFT-FE settings
PBE; SPMS norm-conserving pseudopotentials; FE polynomial order 7; mesh size
parameter 1.2 Å; atom-centred refinement radius 8.0 Å; Fermi–Dirac smearing at
500 K; SCF tolerance 5 × 10⁻⁵ Ha; Anderson mixing; zero Dirichlet in z for both
wavefunctions and electrostatic potential; no relaxation. Run on OLCF Frontier,
64 nodes, 4 × MI250X per node, one MPI task per GPU.

### MD protocol
Langevin, **1100 K**, friction **10⁻³ fs⁻¹**, timestep **1 fs**, **50 ps**
(50,000 steps), snapshot every **100 steps**. Frozen region: oxide atoms deeper
than `max(0.85·t, 6 Å)` below the LLZO top surface. Physicality filter:
min pairwise distance > 1.2 Å (0 of 62,029 rejected).

---

## 6. What must NOT go into the paper

The draft was once ~4,370 words and read as a lab notebook. It was cut to
~2,700 (now ~2,930) on the user's explicit instruction. **Do not reintroduce
any of the following.** All of it is preserved with full numbers in
`SI_notes.md`.

- The per-round training-set ledger (16→28→33→38→47→77→108). Say "six
  iterations, 16 → 108".
- Any paragraph explaining why it0 is worse than the foundation model. One
  clause exists; that is the whole budget.
- The **timetest7** 7-snapshot set. It is 7 correlated frames from a single
  trajectory — not an independent test set — and it was being reported as
  evidence against our own result.
- The float32 energy-noise analysis. One clause in Methods/Evaluation; no more.
- The epoch-sweep training-length control (1500/2000/2500 epochs). Internal check.
- The PV-vs-FPS head-to-head, Williams' tests, the standardisation finding, the
  biased-arena caveat. The paper needs **one sentence**: the signal predicts
  real DFT error. The rest belongs to the separate methods paper.
- The vac2pfu blow-up provenance (6/12 exceeded 3000 K etc.). Two sentences of
  scope only.
- MD unwrapping mechanics in the main text. Methods clause only — the details
  live in Section 4 above and in the code.

**Editorial test when adding anything:** does this change what a reader
believes about the two claims in Section 1? If not, it goes in SI.

---

## 7. npj Computational Materials house style

Encoded in the `.tex` preamble comments; checked against the Guide to Authors
2026-08-28.

- Unstructured abstract, **≤ 250 words**.
- Main text **5,000 words**, excluding abstract/references/figures/tables.
- **Max 6 tables + figures combined.** Currently at exactly 6.
- References **≤ ~50**, numerical superscript citations only (`natbib` with
  `[super,comma,sort&compress]`). Not author–year.
- Mandatory section order: Title → Abstract+keywords → Introduction → Results →
  Discussion → Methods → Acknowledgements → Competing Interests → Contributions
  → Funding → References → Figure Legends → Tables → Figures. **Do not reorder.**
- Code availability **before** Data availability, both at the end of Methods.
- Title ≤ 150 chars (current: 117). Running title ≤ 50 letters+spaces.
- Before submission: generate `.bbl` via BibTeX and paste its content in place
  of the `thebibliography` block; line numbers (`lineno`) stay until acceptance;
  tables and figures upload as separate files.

---

## 8. Known open items

Beyond the diffusion work:

- **5 reference placeholders**: OMat24/mace-omat-0-medium, DFT-FE methodology
  (Motamarri et al.), Das 2022, SPMS pseudopotentials, plus prior Li/LLZO DFT
  literature (Iwasaki et al.; Burov et al. 2024).
- **3 figures to build**: Fig 1 (system + BC schematic), Fig 3 (error vs
  distance from free surface — build from `it5_per_atom_raw.npz`), Fig 5 (MSD).
  Fig 2 (latent space) can be adapted from `paper/poster/make_figs.py`, which
  already generates `fig_latent.pdf` from the real 62k pool.
- **Corresponding author** not marked.
- **Acknowledgements / Funding / Contributions** need real content.
- **Interface-construction Methods detail** (lattice matching, gap
  optimisation) is a TODO; source material is in the BS thesis, §"Lattice
  Matching and Supercell Construction" and §"Interface Construction and Gap
  Optimization" — `github.com/darakji/BSThesis`, `main.tex`. **Treat the thesis
  as reference for formalism only, not as ground truth** — the project has
  moved on substantially (thesis says 26 labelled structures, 5000-step MD,
  snapshot every 25 steps; current values are 108, 50 ps, every 100 steps).
- **Unresolved data discrepancy**: `kfold_it3_final/embeddings/fps_coverage/fps_summary.json`
  records 5 picks for it3→it4 where the reviewed series needs +9 to reach 108.
  The poster used +9. Settle before that series is published anywhere.
- **Two genuinely missing experiments**, both flagged in `MASTER_SUMMARY.md` §13
  and in `SI_notes.md`: z-padding convergence (will be asked for by a referee),
  and a periodic-sandwich vs open-z comparison of a physical observable — the
  latter is the highest-value missing result in the project.
- **Scope risk created by the current framing**: one interface family
  demonstrates the pipeline but does not establish that the accuracy or the
  iteration count generalises. The Discussion states this explicitly; a second
  system would close it.

---

## 9. Glossary

| term | meaning |
|---|---|
| **universal** | the unmodified `mace-omat-0-medium` foundation model |
| **it0 … it6** | active-learning iterations; it6 is the production model |
| **clean 29** | the 32-frame legacy evaluation set minus 3 contaminated entries |
| **test35 / 33-set** | 29 clean + 6 holdout = 35; minus the 2 out-of-domain vacancy frames = the 33 reported |
| **idx30, idx34** | the two 2 vac/f.u. frames in test35; both out of domain, both must be excluded together |
| **timetest7** | 7 snapshots from one 1 ns trajectory; weak set, excluded from the paper |
| **vac0p5pfu / vac1pfu / vac2pfu** | vacancy tiers, 0.5 / 1 / 2 per formula unit. 2 pfu is out of domain |
| **FPS** | farthest-point sampling in latent space |
| **PV** | Gaussian-process posterior variance in latent feature space |
| **d99 / coverage radius ρ** | ρ = max_k δ_k, worst-case distance from any pool point to its nearest labelled neighbour |
| **SWA / Stage Two** | stochastic weight averaging phase of MACE training |
| **open-z** | `pbc = [True, True, False]`; the project's defining constraint |

---

## 10. Key file locations

All under `/scratch/users/phanim/mehuldarak/`. **`/storage` no longer exists** —
older paths in `MASTER_SUMMARY.md` say `/storage`; substitute `/scratch`.

| what | path |
|---|---|
| project audit trail | `it5_final/MASTER_SUMMARY.md` |
| training set (108) | `it6_final/it6_train_108.extxyz` |
| test set (35) | `it6_final/it6_test_35.extxyz` |
| production model | `alchemi_a100_package/model/mace_it6_final_full_stagetwo.model` |
| per-iteration metrics | `it6_final/epoch_sweep/test35_{indomain_33,excl_idx34,incl_all35}_comparison.csv` |
| per-frame metrics | `it6_final/epoch_sweep/test35_per_frame_epochsweep.csv` |
| per-atom errors (for Fig 3) | `it5_final/it5_per_atom_raw.npz` |
| UQ validation scripts | `it6_final/uq_fps_validation/` |
| FPS coverage outputs | `it5_final/latent_extraction/fps_summary.json`, `fps_coverage_curve.csv` |
| MD driver (canonical) | `it5_final/md_all36_50ps/s5_MD.py` |
| diffusion analysis (has 2 bugs, see §4) | `it5_final/snapshot_analysis_LLZO100/diffusion_coeff.py` |
| figure generation to adapt | `paper/poster/make_figs.py` |
| MD convention constants | `alchemi_a100_package/scripts/common.py` |

---

## 11. Working agreements

From the user, standing:

- **Never run compute on the login node.** Take an `srun` allocation.
- **Do not delete or modify existing files without asking.** Creating new files
  is fine.
- Report what actually happened. If a test fails or a step was skipped, say so.
- The user pushes back hard on over-documentation in the paper and on
  unverified claims. When in doubt about whether something belongs in the main
  text, it does not — put it in `SI_notes.md`.
