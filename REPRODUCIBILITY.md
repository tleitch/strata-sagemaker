# Reproducibility

| Level | What you can do | Supported |
|---|---|---|
| **Metric verification** | Recompute every reported number (Tables, confusion matrix, per-class metrics, bootstrap intervals, McNemar tests, aggregate recovery, disparity) from the frozen predictions in `predictions/` | **Yes — fully public** (this repo) |
| **Inference reproduction** | Run the paper's exact model on the public PPP benchmark and on synthetic records | **Yes — no-cost reviewer access** via the SageMaker endpoint (contact terry@aequum.ai) or the AWS Marketplace listing |
| **Training reproduction** | Retrain STRATA from source data and code | **No** — proprietary training implementation and weights; the merged race-labeled voter corpus is not redistributed |

## Provenance of the frozen predictions
All voter- and PPP-holdout ensemble numbers derive from a single frozen prediction set
produced by the locked M8-bgtract artifacts: the full-data character BiLSTM and the five
**out-of-fold**-refit XGBoost post-filter boosters. The source array is archived as
`m8_preds_oof.npz` (SHA-256/MD5 recorded in `CHECKSUMS.md`); the parquets in `predictions/`
are its de-identified projection (see `DATA_USE_STATEMENT.md`).

The historical geographic-transfer models (M1–M4; Table "training geography" in the paper)
are a **separate, earlier model generation** trained with an in-sample stacker on a distinct
PPP extract; their per-record predictions are not part of this release, and their aggregate
results are reported from their frozen `results.json` (included under `evaluation/aux/`).

## Cohort definitions used by the scripts
- **Voter evaluation cohort** (N = 981,288): `voter_holdout` rows with `true_fine_class != "multi"`.
- **PPP evaluation cohort** (N = 111,062): `ppp_holdout` rows with `person_name_cohort == True`.
- BISG/BIFSG metrics are computed over their **scored subset** (`returned_prediction == True`);
  pairwise tests involving them use common support.

Running `make reproduce` regenerates the headline values, e.g. STRATA ensemble voter-subset
accuracy 0.8876 / White FPR 0.1783 and PPP person-cohort 0.8846 / 0.0915.

## Compute environment (GPU vs CPU)
The frozen prediction files in this repository were generated on **GPU** (the paper's compute)
and are the exact source of every reported table, figure, CI, and statistical test. The deployed
inference container is **CPU-only** (a deliberate network-isolation choice). CPU-vs-GPU
floating-point differences in the character BiLSTM propagate through the XGBoost post-filter and
produce small per-class probability differences (median 0, p90 ≈ 8e-5, max ≈ 3e-2 on a thin
tail). These do **not** change any reported result: class argmax agrees on 1,111,843 / 1,111,882
records (39 differ, 0.0035%); all metric tables are argmax-based and identical; per-class Brier
is identical to four decimals; the Section-4.9 aggregate share errors differ by ≤0.002 pp; and
the probability-weighted disparity is identical at the reported precision. The only reported
figure sensitive to this is the PPP-cohort White FPR (0.0915 GPU vs 0.0914 CPU), a last-digit
rounding-boundary shift. In short: **metric-level reproduction from the frozen files here is
exact; functional reproduction via the CPU inference container reproduces class argmax and all
reported metrics, and class probabilities to within ~3e-2 (CPU/GPU floating point).**
