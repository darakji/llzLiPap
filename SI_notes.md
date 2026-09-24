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
