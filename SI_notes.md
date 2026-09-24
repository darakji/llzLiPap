# Material cut from the main text

Everything below was written into the manuscript draft and then removed to keep
the main text on the argument. None of it is wrong; it is the wrong length for
a paper. Numbers are kept here verbatim so the SI (or the separate methods
paper) can be assembled without re-deriving anything.

Provenance for every number: `it5_final/MASTER_SUMMARY.md`.

## Destined for Supplementary Information

**Per-round training-set growth.** 16 → 28 (+12) → 33 (+5) → 38 (+5) → 47 (+9)
→ 77 (+30) → 108 (+31) across it0–it6. Main text states only "six iterations,
16 → 108". Note: `kfold_it3_final/embeddings/fps_coverage/fps_summary.json`
records 5 picks for the it3→it4 round where the reviewed series needs +9; this
discrepancy is unresolved and should be settled before the series is published
in any form.

**Full per-iteration metrics on all three evaluation scopes.** The main text
reports one table on the 33-structure in-domain set. Also on disk, for all of
universal/it0–it6 plus the two epoch-sweep variants:
`it6_final/epoch_sweep/test35_indomain_33_comparison.csv`,
`test35_excl_idx34_comparison.csv`, `test35_incl_all35_comparison.csv`,
`timetest7_all7_comparison.csv`, plus per-frame CSVs for each.

**The 7-snapshot temporal confirmation set (timetest7).** Snapshots at
0/50/100/200/400/800/1000 ps from a single 1 ns trajectory of one interface.
On it, it6 (80.0 meV/Å RMSE, 49.5 MAE) is tied with it4 (76.0, 46.9) rather
than better. Cut because 7 correlated frames from one trajectory is not an
independent test set — it probes temporal, not configurational, diversity. If
included in SI, present it as what it is and do not treat the tie as evidence
against the it4→it6 gain.

**Domain-of-validity provenance.** The 2 vac/f.u. tier was excluded at pool
construction, not post hoc: 6 of its 12 structures exceeded 3000 K within
81–248 MD steps (`it5_final/md_all36_50ps/BLOWUP_LOG.md`). Two such structures
entered the held-out set through the independent holdout construction and are
retained as an extrapolation probe. it5 gives 266.3 meV/Å on them, it6 252.6,
against 72.4 in domain. Main text keeps only the scope statement and the
252.6/72.4 contrast.

**Training-length control (epoch sweep).** The final iteration retrained at
2000 epochs (SWA from 1200) and 2500 (SWA from 1600) against the production
1500/1000, all else identical. Force error unchanged: 72.04 / 72.00 / 71.84
meV/Å RMSE and 44.89 / 44.87 / 44.78 MAE. Both longer runs froze the same
pre-SWA checkpoint (epoch 453); best post-SWA checkpoints at 1226 and 1896,
after which validation plateaus then drifts upward. Establishes the model is
data-limited, not optimisation-limited. Cut as an internal control.

**float32 energy-metric floor.** Absolute total energies are ~2.3e5 eV, where
the float32 ULP is 1.6e-2 eV, so |E_pred − E_ref| loses several digits to
cancellation. Repeating an identical evaluation of an identical model on
identical data returns 4.376 / 4.280 / 4.369 meV/atom on successive runs while
force RMSE reproduces bit-for-bit. Differences in reported energy error below
~0.1 meV/atom are not resolvable. Main text keeps one clause in Methods.
Independently corroborated: a rigid z-translation that leaves MACE descriptors
bit-identical (cosine similarity 1.00000000 on 13 structures) still shifts
total energy by up to 3.1 meV/atom, every shift an exact multiple of the
float32 ULP.

**MD-analysis conventions.** Trajectories are stored wrapped in x,y, so
coordinates must be unwrapped before any MSD. Unwrapping must be done in
fractional coordinates — one of the MD seeds has γ = 111.54°, and a
diagonal-only minimum-image convention injects spurious ~4 Å displacements on
it. Unwrapping is unambiguous at the 100 fs snapshot interval (RMS Li
displacement ~0.2 Å vs half-cell 5.6 Å). Without it, MSD saturates near L²/6 ≈
21 Å² per dimension in the smallest cells, reached within tens of ps at 1100 K.
No centre-of-mass drift correction should be applied: the frozen substrate
already fixes the reference frame, and Li is 55–70% of the atoms, so
subtracting an all-atom COM would remove part of the genuine Li flux.

**Centering.** `fix_slab.py --mode unwrap --vac 20` is descriptor-neutral
(cosine 1.00000000) and changes forces by ≤0.13 meV/Å under a controlled pure
translation — safe, but physically inert for MD given open-z. The CIF
round-trip it performs perturbs positions by 1–3 mÅ and changes forces by up to
6.4 meV/Å, ~50× more than the translation itself; if centering is applied
before MD it should be done in memory, not via file round-trip.

## Destined for the separate methods paper

Scoped in MASTER_SUMMARY §13 as "how active-learning campaigns fool
themselves". The main text keeps only the one-line result that latent
uncertainty predicts realised DFT error at r = 0.85.

- **PV vs FPS head-to-head.** PV +0.847 force / +0.777 energy against FPS's
  literal criterion at +0.724 / +0.611. Not significant for forces (Williams
  p = 0.066). Most of the margin is preprocessing, not criterion: PV run in
  FPS's own L2+PCA space drops to +0.683, indistinguishable from plain
  min-distance (p = 0.65). The one clean finding is that per-feature
  standardisation improves energy-error prediction (+0.611 → +0.716,
  p = 0.010), independent of criterion.
- **Biased-arena caveat.** All 35 ground-truth points are FPS's own picks plus
  4 random frames, so the comparison can only measure how well each criterion
  ranks difficulty *within the region FPS chose*, never what PV would have
  selected instead. This is why no "PV beats FPS" claim is made anywhere.
- **Near-independent pool rankings.** Spearman(PV, FPS criterion) = +0.10 to
  +0.16 over 62,029 frames; top-31-by-PV overlaps FPS's 31 by 10–11. They agree
  only in the extreme tail (median FPS pick at the 99.5th PV percentile, but 10
  of 31 below the 90th, min 24.9th).
- **Round-1/2 static correlation correction.** The apparent PV-vs-energy
  correlation on the held-out set was carried entirely by one out-of-domain
  structure; excluding both 2 vac/f.u. frames flips it — force becomes the real
  signal (r ≈ +0.46–0.49, p ≈ 0.004–0.007) and energy vanishes (p ≈ 0.7–0.9).
- **Leak detection.** Provenance contamination survived coordinate hashing and
  was only caught by model prediction: two held-out frames matched training
  frames to 6.5e-06 and 1.8e-06 meV/atom, differing only in real-space domain
  padding. Mean-pooled latents have no discriminative power for large slabs.
- **Cost-efficiency and stopping.** Round-to-round ΔCS per DFT-atom, and the
  coverage arithmetic that argues the pool is exhausted.

## Genuinely open, not merely cut

- **z-padding convergence.** Padding spans 14.8–36.0 Å in training and
  12.7–20.2 Å in held-out data. A convergence study (15/20/25/30 Å on one
  structure, energy + forces) has not been run and will be asked for.
- **Periodic-sandwich vs open-z comparison.** Building the same interface both
  ways and comparing a physical observable is the highest-value missing
  experiment; if the two differ, that result is the headline.

## Diffusion campaign: full numbers and pending sanity checks (added 2026-09-25)

**Where the numbers live.** `data/diffusion_by_T_1ns.csv` and
`data/diffusion_arrhenius_1ns.csv` are verbatim copies of
`alchemi_a100_package/results/campaign_midT_lid/kinetics/{by_T,arrhenius}.csv`
on PARAM Rudra (home `/home/nsmext/phanim.iisc`). Per-system values (120 rows)
are in `kinetics/systems.csv` there; the structural/chemical companion analysis
(undercoordinated Zr/La at each termination, Li uptake from the metal, density
profiles, z-resolved D, hop rates, RDFs) is in
`results/campaign_midT_lid/chemistry/report.md`. `figs/make_fig_diffusion.py`
rebuilds Fig. 5 from the CSVs; pass the tag of a newer copy (e.g. `5ns`) when
the extension chunks finish.

**Interior D at 800 K, 1 ns, mean over 5 replicas (cm2/s; alpha; N_eff):**
Li(100)/LLZO(110) 1 vac 2.5e-7 (0.74, 17); LLZO(100)-ct 0.5 vac 1.6e-7 (0.66,
16); LLZO(110)-ct 1 vac 2.4e-7 (0.74, 38); Li(111)/LLZO(001) 0.5 vac 1.1e-6
(0.87, 216); held-out LLZO(100)-ct 2.0e-7 (0.71, 19); held-out LLZO(110)-ct
4.3e-7 (0.81, 63). Arrhenius Ea (meV): 358+-60, 682+-105, 415+-42, 445+-33,
403+-90, 588+-46. Nernst-Einstein sigma(300 K) in S/cm: 6.7e-6, 1.6e-9, 1.6e-6,
3.6e-6, 1.7e-6, 4.6e-8. Tetragonal LLZO experiment (Awaka 2009): 1.6e-6 S/cm,
540 meV. Interface-exchange Ea (crossings, no residence filter): 251, 226, 188,
316, 391, 298 meV.

**Why 500-800 K and not 300 K.** At 300-450 K with 0.5 ns the interior Li
never left its cage (alpha ~ 0.1); the room-temperature number is only
reachable by Arrhenius extrapolation. The Li-metal slab is liquid-like at
>= 450 K with a free top surface under every thermostat tried (Nose-Hoover,
Langevin at 1 and 0.1 /ps); freezing the outermost 15 % (>= 4 A) of the slab as
a bulk-electrode boundary keeps it solid at 300 K and is the production setup.

**Foundation-model control (preliminary, not in the paper).** Jobs 76643
(mace-omat-0-medium) and 76644 (it6), seed1/seed3/seed4 at 800 K, lid, NH,
2 fs, one replica, both cut at the 1 h debug limit after 28 / 38 ps. Interior
Li MSD over that window: omat 1.6 / 4.0 / 1.6 A2 vs fine-tune 0.4 / 5.4 /
1.4 A2 (D ~1.6e-6 / 3.9e-6 / 1.6e-6 vs 2.8e-7 / 3.3e-6 / 8.6e-7 cm2/s). Same
order of magnitude, both slow; too short and too few to claim that the
transport regime is model-independent. A sentence to that effect was in the
Results draft and was cut on review. To support it: rerun omat on all six
cells at 700 and 800 K, 3 replicas, >= 500 ps.

**Exchange barrier threshold.** The 190-390 meV in the paper is the
t_res = 0 column (every crossing of the +-1.5 A band). With t_res = 200 ps the
same cells give 154 / 91 / 59 / 129 / 244 / 158 meV. Both are now stated in
the text; the residence criterion is a free parameter and the 5 ns data
should show whether the filtered value converges (Burov used residence-time
filtering on 40 ns trajectories).

**t_total_ps in the CSVs is per replica** (0.95-1.11 ns; the 500 K systems
ran on lighter ranks and got more steps in the same wall time).

**Sanity checks still owed on the diffusion numbers (not yet done):**
1. DFT-FE single points on 12 production frames (one 800 K mid-hop and one
   500 K random frame per interface, `chemistry/dftfe_subset12/`): force error
   of the fine-tune vs the foundation model under production conditions.
2. NEB barrier of an interior Li vacancy hop, fine-tune vs DFT-FE.
3. Convergence in run length: 1 ns vs 5 ns (extension chunks running); alpha
   must approach 1 at 700-800 K and the Arrhenius slope must stop moving.
4. Thermostat independence of D at the production temperatures (an NVE
   segment from a thermalised state); the NH-vs-Langevin test so far is at
   300-450 K only.
5. Sensitivity to the frozen-lid thickness (0.15 vs 0.30 of the slab) and to
   the interior-region margins (8 A below the plane, 4 A above the wall).
6. Slab-thickness / finite-size sensitivity of the interior D.
7. Li-sublattice ordering of the seeds (site-occupancy check that the
   starting cells are the ordered tetragonal arrangement, as claimed).
8. z-padding convergence and the periodic-sandwich comparison (above).
