# strata-sagemaker — evaluation artifact for STRATA

Public evaluation artifact for **"STRATA: A Name-and-Geography Race Inference Model
for Fair Lending and Housing Equity Applications"** (Chalavadi, Leitch, and Pastor).

This repository lets anyone **recompute every table, figure, confidence interval, and
statistical test in the paper from frozen, de-identified prediction files** — without
the training code, model weights, or any personally identifiable data.

## One-command reproduction
```bash
pip install -r requirements.txt      # or: conda env create -f environment.yml
make reproduce                       # regenerates all tables/figures into outputs/
```
`make reproduce` runs the scripts in `evaluation/` against `predictions/` and writes
CSV/figure outputs to `outputs/`. `make verify` checks every file against `CHECKSUMS.md`.

## What is and is not here
- **Included:** de-identified per-record predictions for every reported model and
  ablation (`predictions/`), the evaluation and plotting code (`evaluation/`), the PPP
  cohort-construction scripts (`ppp_pipeline/`), a synthetic test set (`synthetic_test/`),
  a locked environment, and `CHECKSUMS.md`.
- **Not included (by design):** the proprietary training implementation and model weights
  (commercial); and the merged, individually race-labeled, geocoded voter corpus (PII).
  **No names, addresses, loan identifiers, voter-file identifiers, or stable hashes derived
  from them are present in this repository.** See `DATA_USE_STATEMENT.md`.

## Reproducibility tiers
See `REPRODUCIBILITY.md`. In short: metric verification is fully public here; running the
paper's exact model on new/synthetic records is available at no cost to reviewers via a
SageMaker endpoint; retraining from source is not supported.

## Inference access
- Commercial deployment: **AWS Marketplace listing "aequumAI STRATA"** (Amazon SageMaker AI
  real-time endpoint or Batch Transform), under the aequumAI STRATA EULA v3.0.
- **No-cost review / academic use:** governed by the Academic Use Addendum v1.0
  (Academic Tier). Contact **terry@aequum.ai** for no-cost review access.

## Licensing
- Code (`evaluation/`, `ppp_pipeline/`, `synthetic_test/`): **Apache-2.0**.
- Released artifacts (prediction files, docs): **CC BY 4.0**.
- **Third-party note:** the ZRP and Argyle \& Barber prediction files are derived from those
  methods' outputs and are subject to their respective source licenses; verify redistribution
  terms before relying on those two files.

## Citation
Chalavadi, S., Leitch, T., and Pastor, A. STRATA: A Name-and-Geography Race Inference Model
for Fair Lending and Housing Equity Applications. arXiv:2504.21259.
