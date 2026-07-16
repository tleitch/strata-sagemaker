# STRATA (M8-BGT) — AWS Marketplace sample

Sample notebook and input for the AWS Marketplace SageMaker model package
**STRATA: Race/Ethnicity Probability + Uncertainty (US, name+address)**.

- `M8-BGT_sample_notebook.ipynb` — subscribe → deploy (real-time endpoint or
  Batch Transform) → invoke → interpret output (`pred_race`, `p_*`, `iu`,
  `model_used`, anonymous `cohort_tract`/`cohort_zcta`).
- `sample_input.csv` — example input (`fname,mname,lname,housenumber,street,city,state,zip`).

Aggregate, population-level use only. See the product EULA.
