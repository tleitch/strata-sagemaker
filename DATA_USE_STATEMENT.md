# Data use and privacy statement

## Released here
- **De-identified per-record predictions** (`predictions/`): one row per held-out record per
  model, with model predicted class, class probabilities (where the method emits them),
  true coarse/fine class, `state` (two-letter), `income_decile` (1–10), a coverage flag,
  and a person-name-cohort flag.
- Evaluation, plotting, and cohort-construction code; a synthetic test set; a locked environment.

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

## Third-party outputs
The ZRP and Argyle \& Barber prediction files are derived from those methods' outputs and
are redistributed here only as evaluation inputs; they remain subject to the respective
source licenses.

## Added grouping / outcome columns
- `tract_cluster_id`: an **opaque** integer that groups records sharing a census tract, with
  labels randomly permuted at export time. It carries **no mapping to any real tract GEOID**
  (the mapping is not published) and exists only to permit the tract-clustered bootstrap. No
  geography finer than state is otherwise released.
- `forgiven` (PPP only): a boolean derived from the **public** SBA field
  ForgivenessAmount/CurrentApprovalAmount ($\geq 0.99$), NA where no outcome is recorded. It is
  a public loan attribute attached to the de-identified row; it is not a personal identifier.
