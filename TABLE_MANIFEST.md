# Table / figure -> script -> input manifest

| Paper item | Script | Inputs | Output |
|---|---|---|---|
| Table 6 (overall performance) | evaluation/reproduce_tables.py | predictions/voter_holdout/* | outputs/table_overall.csv |
| Table 7 (FPR by race) | evaluation/reproduce_tables.py | predictions/voter_holdout/* | outputs/table_fpr_by_race.csv |
| Table 8 (per-class + Brier) | evaluation/reproduce_tables.py | predictions/voter_holdout/strata_ensemble | outputs/per_class_ensemble.csv |
| Confusion matrix | evaluation/reproduce_tables.py | predictions/voter_holdout/strata_ensemble | outputs/confusion_ensemble.csv |
| Table 10 (PPP person cohort) | evaluation/reproduce_tables.py | predictions/ppp_holdout/* | outputs/table_overall.csv (ppp rows) |
| Table 13 (aggregate recovery) | evaluation/reproduce_tables.py | predictions/voter_holdout/strata_ensemble | outputs/aggregate_recovery.csv |
| Figure 1 (voter misclass by income) | evaluation/plot_figures.py | predictions/voter_holdout/* | outputs/figure1_voter.png |
| Figure 2 (PPP misclass by income) | evaluation/plot_figures.py | predictions/ppp_holdout/* | outputs/figure2_ppp.png |
| Table 9 (geolocation ablation) | reproduce_tables.py (name-only vs base) | voter_holdout/{lstm_nameonly,strata_base} | outputs/table_overall.csv |
| Table 11 (M1-M4 training geography) | evaluation/aux/results_M1_M4.json | aggregate results (separate model generation; not per-record) | — |

Note: bootstrap intervals, McNemar tests, and the disparity example use the same prediction
files; scripts for those are in evaluation/ (see reproduce_tables.py comments).
