# Data use and privacy statement

## Released here
- **De-identified per-record predictions** (`predictions/`): one row per held-out record per
  model, with model predicted class, class probabilities (where the method emits them),
  true coarse/fine class, `state` (two-letter), `income_decile` (1–10), a coverage flag,
  and a person-name-cohort flag.
- Evaluation, plotting, and cohort-construction code; a synthetic test set; a locked environment.

*Note:* the released prediction probabilities are GPU-generated (the paper's compute). The
CPU-only inference container reproduces class argmax and all reported metrics exactly, and
probabilities to within ~3e-2 (CPU/GPU floating point); see `REPRODUCIBILITY.md`.

## Withheld (never in this repository)
- **Personal identifiers:** names, addresses, PPP `LoanNumber`, voter-file identifiers, ZIP,
  and census tract / block-group GEOIDs. None of these appear in any file, and no released
  column is a deterministic function of them.
- The merged, geocoded, individually race-labeled **training corpus** (PII-sensitive).
- The **model weights and training code** (commercial).

## `random_row_id` construction
Each cohort's records were assigned a fresh integer `random_row_id` by a seeded random
permutation generated at export time. The mapping from real record keys to `random_row_id`
is **not published** and is not recoverable from this repository. `random_row_id` is shared
across the model files *within a cohort* only so that paired tests (e.g. McNemar) can align
the same record across models; it does not identify any real person or loan.

## Re-identification assessment
The only covariates released are `state` and a coarse `income_decile`, alongside model
outputs and race labels, over cohorts of ~10^5–10^6 records. No geographic unit finer than
state is released, no free-text, and no stable hash of any identifier. We judge row-level
re-identification risk to be negligible.

## Third-party baselines
Two comparison files are baselines, not STRATA outputs. Neither contains any third-party
source code or dataset — only de-identified probability/label outputs:
- **ZRP:** produced by running the open-source `zestai/zrp` package, which is licensed
  **Apache-2.0** (redistribution permitted). The file here is de-identified model output, not
  ZRP source code or its reference tables.
- **Argyle & Barber:** produced by our own faithful reimplementation of the published method
  (Argyle & Barber, 2024); the file is our reimplementation's de-identified output, not the
  authors' code or data.

Both are released under this repository's data license (CC-BY-4.0) as de-identified evaluation
baselines.

## Added grouping / outcome columns
- `tract_cluster_id`: an **opaque** integer that groups records sharing a census tract, with
  labels randomly permuted at export time. It carries **no mapping to any real tract GEOID**
  (the mapping is not published) and exists only to permit the tract-clustered bootstrap. No
  geography finer than state is otherwise released.
- `forgiven` (PPP only): a boolean derived from the **public** SBA field
  ForgivenessAmount/CurrentApprovalAmount ($\geq 0.99$), NA where no outcome is recorded. It is
  a public loan attribute attached to the de-identified row; it is not a personal identifier.
