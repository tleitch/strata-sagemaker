# Synthetic test set
`generate_synthetic.py` deterministically builds `synthetic_records.csv` — 500 fully
synthetic name+address records (no real individuals) — plus `expected_outputs.json`.
Use it to exercise the STRATA inference path via the SageMaker endpoint / AWS Marketplace
artifact (contact terry@aequum.ai for no-cost review access). Metric-level reproduction of
the paper's tables uses `predictions/` and `make reproduce`, not this set.
