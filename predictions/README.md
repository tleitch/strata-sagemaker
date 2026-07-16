# Prediction file schema

Every `*_predictions.parquet` under `voter_holdout/` and `ppp_holdout/` has one row per
held-out record and these columns:

| Column | Type | Notes |
|---|---|---|
| `random_row_id` | int64 | Fresh seeded identifier; shared across models *within a cohort* for paired tests. NOT derived from any real id/name/address (see `DATA_USE_STATEMENT.md`). |
| `evaluation_cohort` | str | `voter_holdout` or `ppp_holdout`. |
| `true_coarse_class` | str | White / Black / Hispanic / Asian / Other (self-reported). |
| `true_fine_class` | str | Source provenance label (`white`,`black`,`hisp`,`asian`,`nhpi`,`aian`,`other`,`multi`,`asian_pi`,`other_multi`). Voter evaluation cohort excludes `multi`. |
| `model_name` | str | `strata_ensemble`, `strata_base`, `lstm_nameonly`, `bisg`, `bifsg`, `zrp`, `argyle_barber`. |
| `model_version` | str | e.g. `M8-bgtract-oof-v1` (STRATA). |
| `predicted_class` | str | Argmax prediction; null where `returned_prediction == False`. |
| `probability_white/black/hispanic/asian/other` | float | Class probabilities where the method emits them (STRATA ensemble both cohorts; BISG voter). Null (NaN) otherwise. |
| `returned_prediction` | bool | False when the method returned no prediction (BISG/BIFSG out-of-reference-list). |
| `state` | str | Two-letter code. |
| `income_decile` | Int64 | Census-tract income decile 1–10 (within cohort). |
| `person_name_cohort` | bool | PPP only: True for the two-stage person-name cohort (N=124,914). Always False/NA for voter. |
| `tract_cluster_id` | int64 | **Opaque** cluster key: records sharing a census tract share an id, but the ids are randomly relabeled and carry **no mapping to any real GEOID**. Enables the tract-clustered bootstrap (`compute_significance.py`). |
| `forgiven` | boolean | PPP only: True if PPP loan forgiveness ratio (ForgivenessAmount/CurrentApprovalAmount) $\geq 0.99$; NA where no forgiveness outcome is recorded (public SBA field). Used by `compute_disparity.py`. NA for voter. |

**Cohorts.** Voter evaluation cohort = `true_fine_class != "multi"` (N=981,288). PPP
evaluation cohort = `person_name_cohort == True` (N=124,914). BISG/BIFSG metrics use
`returned_prediction == True` (their scored subset).

Counts: voter files 986,801 rows each; PPP files 125,081 rows each. `make reproduce`
consumes these to regenerate the paper's tables.
