#!/usr/bin/env python3
"""Section 4.9 illustrative downstream disparity from predictions/: White-minus-Black PPP
loan-forgiveness-rate gap estimated from self-reported race, STRATA hard labels, STRATA
summed probabilities, and BISG hard labels, on the person-name cohort with a forgiveness
outcome. 1000-resample bootstrap CIs. Writes outputs/disparity.json.

Probability-weighted group mean: mu_c = sum_i p_ic y_i / sum_i p_ic ; gap = mu_White - mu_Black.
NOTE: near-ceiling outcome (~99.6% forgiven); illustrative, not a definitive validation."""
import os,json,numpy as np,pandas as pd
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PRED=os.path.join(HERE,"predictions"); OUT=os.path.join(HERE,"outputs"); os.makedirs(OUT,exist_ok=True)
def load(m): d=pd.read_parquet(os.path.join(PRED,"ppp_holdout",f"{m}_predictions.parquet")); return d[d.person_name_cohort==True].set_index("random_row_id").sort_index()
ens=load("strata_ensemble"); bisg=load("bisg")
ok=ens.forgiven.notna().values; forg=ens.forgiven.fillna(False).astype(float).values
true=ens.true_coarse_class.values; ehard=ens.predicted_class.values
Pw=ens.probability_white.values; Pb=ens.probability_black.values
bhard=bisg.reindex(ens.index).predicted_class.values
def rate(mask): mm=mask&ok; return float(forg[mm].mean()) if mm.sum() else np.nan
def hard(pred): return rate(pred=="White")-rate(pred=="Black")
def prob():
    w=np.nan_to_num(Pw)*ok; b=np.nan_to_num(Pb)*ok
    return float(np.nansum(w*forg)/np.nansum(w)-np.nansum(b*forg)/np.nansum(b))
d={"n_with_outcome":int(ok.sum()),"forgiveness_base_rate":round(float(forg[ok].mean()),4),
   "true":round((rate(true=="White")-rate(true=="Black"))*100,3),
   "strata_prob":round(prob()*100,3),"strata_hard":round(hard(ehard)*100,3),
   "bisg_hard":round(hard(pd.Series(bhard).fillna("_none").values)*100,3)}
rng=np.random.RandomState(42); N=len(ens); bt={k:[] for k in ["true","strata_prob","strata_hard","bisg_hard"]}
for _ in range(1000):
    ix=rng.randint(0,N,N); o=ok[ix]; f=forg[ix]; tr=true[ix]; eh=ehard[ix]; bh=pd.Series(bhard[ix]).fillna("_none").values; pw=np.nan_to_num(Pw[ix])*o; pb=np.nan_to_num(Pb[ix])*o
    def r(mask): mm=mask&o; return f[mm].mean() if mm.sum() else np.nan
    bt["true"].append(r(tr=="White")-r(tr=="Black")); bt["strata_hard"].append(r(eh=="White")-r(eh=="Black"))
    bt["bisg_hard"].append(r(bh=="White")-r(bh=="Black")); bt["strata_prob"].append(np.nansum(pw*f)/np.nansum(pw)-np.nansum(pb*f)/np.nansum(pb))
for k in bt: a=np.array(bt[k])*100; d[k+"_ci"]=[round(float(np.nanpercentile(a,2.5)),3),round(float(np.nanpercentile(a,97.5)),3)]
json.dump(d,open(os.path.join(OUT,"disparity.json"),"w"),indent=2); print(json.dumps(d,indent=2))
