#!/usr/bin/env python3
"""Reproduce the STRATA paper's headline tables from the frozen, de-identified
prediction files in predictions/. No model, weights, or PII required.

Outputs (written to outputs/):
  table_overall.csv        - per-model accuracy / weighted-F1 / weighted-precision /
                             macro one-vs-rest FPR / coverage  (voter subset; PPP person cohort)
  table_fpr_by_race.csv     - per-class one-vs-rest FPR by model
  confusion_ensemble.csv    - STRATA ensemble 5x5 confusion (voter subset)
  per_class_ensemble.csv    - per-class precision/recall/FNR/F1/FPR/Brier (voter subset)
  aggregate_recovery.csv    - summed-probability vs hard-label group-count recovery
Run:  python evaluation/reproduce_tables.py         (or: make reproduce)

Cohort definitions (match the paper):
  voter evaluation cohort = voter_holdout rows with true_fine_class != 'multi'  (N=981,288)
  PPP evaluation cohort   = ppp_holdout rows with person_name_cohort == True     (N=124,914)
"""
import os, glob, numpy as np, pandas as pd
from sklearn.metrics import f1_score, precision_score
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED=os.path.join(HERE,"predictions"); OUT=os.path.join(HERE,"outputs"); os.makedirs(OUT,exist_ok=True)
CLASSES=["White","Black","Hispanic","Asian","Other"]
VOTER_MODELS=["lstm_nameonly","strata_base","zrp","bifsg","bisg","argyle_barber","strata_ensemble"]
PPP_MODELS=["lstm_nameonly","strata_base","zrp","strata_ensemble"]

def load(cohort,model):
    return pd.read_parquet(os.path.join(PRED,cohort,f"{model}_predictions.parquet"))
def cohort_mask(df):
    if df.evaluation_cohort.iloc[0]=="voter_holdout": return df.true_fine_class!="multi"
    return df.person_name_cohort==True
def metrics(df):
    d=df[cohort_mask(df)].copy()
    scored=d[d.returned_prediction]                      # common-support for BISG/BIFSG
    y=scored.true_coarse_class; p=scored.predicted_class
    fpr={c: round(float(((p==c)&(y!=c)).sum()/max(1,(y!=c).sum())),4) for c in CLASSES}
    return {"n_cohort":len(d),"n_scored":len(scored),"coverage":round(len(scored)/len(d),4),
            "accuracy":round(float((p==y).mean()),4),
            "f1_weighted":round(float(f1_score(y,p,average="weighted",zero_division=0)),4),
            "precision_weighted":round(float(precision_score(y,p,average="weighted",zero_division=0)),4),
            "macro_ovr_fpr":round(float(np.mean(list(fpr.values()))),4), **{f"fpr_{c}":fpr[c] for c in CLASSES}}

# ---- Table: overall + FPR-by-race ----
rows=[]
for coh,models in [("voter_holdout",VOTER_MODELS),("ppp_holdout",PPP_MODELS)]:
    for m in models:
        r=metrics(load(coh,m)); r["cohort"]=coh; r["model"]=m; rows.append(r)
tab=pd.DataFrame(rows)
tab[["cohort","model","accuracy","f1_weighted","precision_weighted","macro_ovr_fpr","coverage","n_cohort","n_scored"]].to_csv(os.path.join(OUT,"table_overall.csv"),index=False)
tab[["cohort","model"]+[f"fpr_{c}" for c in CLASSES]].to_csv(os.path.join(OUT,"table_fpr_by_race.csv"),index=False)

# ---- Confusion + per-class (STRATA ensemble, voter subset) ----
e=load("voter_holdout","strata_ensemble"); e=e[cohort_mask(e)]
ci={c:i for i,c in enumerate(CLASSES)}
C=np.zeros((5,5),int)
for t,pp in zip(e.true_coarse_class.map(ci),e.predicted_class.map(ci)): C[t,pp]+=1
pd.DataFrame(C,index=[f"true_{c}" for c in CLASSES],columns=[f"pred_{c}" for c in CLASSES]).to_csv(os.path.join(OUT,"confusion_ensemble.csv"))
probs=e[[f"probability_{c.lower()}" for c in ["white","black","hispanic","asian","other"]]].to_numpy()
pc=[]
for i,c in enumerate(CLASSES):
    tp=C[i,i]; fp=C[:,i].sum()-tp; fn=C[i,:].sum()-tp; tn=C.sum()-tp-fp-fn
    prec=tp/max(1,tp+fp); rec=tp/max(1,tp+fn); f1=2*prec*rec/max(1e-9,prec+rec); fpr=fp/max(1,fp+tn)
    onehot=(e.true_coarse_class==c).to_numpy().astype(float); brier=float(np.mean((probs[:,i]-onehot)**2))
    pc.append({"class":c,"precision":round(prec,4),"recall":round(rec,4),"fnr":round(1-rec,4),"f1":round(f1,4),"fpr_ovr":round(fpr,4),"brier":round(brier,4)})
pd.DataFrame(pc).to_csv(os.path.join(OUT,"per_class_ensemble.csv"),index=False)

# ---- Aggregate recovery (voter subset): summed prob vs hard label vs true ----
nhat=probs.sum(0); ntrue=np.array([(e.true_coarse_class==c).sum() for c in CLASSES],float)
nhard=np.array([(e.predicted_class==c).sum() for c in CLASSES],float)
agg=pd.DataFrame({"class":CLASSES,"true":ntrue.astype(int),"summed_prob":nhat.round(1),"hard_label":nhard.astype(int),
    "prob_share_err_pp":((nhat/nhat.sum()-ntrue/ntrue.sum())*100).round(3),
    "hard_share_err_pp":((nhard/nhard.sum()-ntrue/ntrue.sum())*100).round(3)})
agg.to_csv(os.path.join(OUT,"aggregate_recovery.csv"),index=False)

print("Wrote outputs/ :")
for f in sorted(glob.glob(os.path.join(OUT,"*.csv"))): print("  ",os.path.relpath(f,HERE))
print("\nHeadline check (STRATA ensemble):")
ens=tab[(tab.cohort=='voter_holdout')&(tab.model=='strata_ensemble')].iloc[0]
print(f"  voter subset  acc={ens.accuracy}  White FPR={ens.fpr_White}  (paper: 0.8876 / 0.1783)")
pe=tab[(tab.cohort=='ppp_holdout')&(tab.model=='strata_ensemble')].iloc[0]
print(f"  PPP person    acc={pe.accuracy}  White FPR={pe.fpr_White}  (paper: 0.8845 / 0.0981)")
