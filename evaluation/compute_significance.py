#!/usr/bin/env python3
"""Section 4.4 significance from predictions/: McNemar (ensemble vs BISG/BIFSG/A&B on
common support), IID bootstrap and tract-clustered bootstrap CIs for ensemble accuracy
and White FPR, and the ZRP White-FPR-difference bootstrap. Writes outputs/significance.json.
Voter evaluation cohort = true_fine_class != 'multi'."""
import os,json,numpy as np,pandas as pd
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PRED=os.path.join(HERE,"predictions"); OUT=os.path.join(HERE,"outputs"); os.makedirs(OUT,exist_ok=True)
def load(m): d=pd.read_parquet(os.path.join(PRED,"voter_holdout",f"{m}_predictions.parquet")); return d[d.true_fine_class!="multi"]
ens=load("strata_ensemble").set_index("random_row_id").sort_index()
res={}
def mcnemar(base):
    b=load(base).set_index("random_row_id"); b=b[b.returned_prediction]
    common=ens.index.intersection(b.index)
    e=ens.loc[common]; bb=b.loc[common]
    ec=(e.predicted_class==e.true_coarse_class).values; bc=(bb.predicted_class==bb.true_coarse_class).values
    n01=int((ec&~bc).sum()); n10=int((~ec&bc).sum()); chi=(abs(n01-n10)-1)**2/max(1,n01+n10)
    return {"n_common":int(len(common)),"ens_right_base_wrong":n01,"ens_wrong_base_right":n10,"chi2":round(float(chi),1)}
res["mcnemar"]={b:mcnemar(b) for b in ["bisg","bifsg","argyle_barber"]}
# bootstrap helpers on ensemble
y=ens.true_coarse_class.values; p=ens.predicted_class.values; cl=ens.tract_cluster_id.values
def stat(idx):
    yy=y[idx]; pp=p[idx]; nonw=yy!="White"
    return (pp==yy).mean(), ((pp=="White")&nonw).sum()/nonw.sum()
rng=np.random.RandomState(42); n=len(y)
accs=np.empty(1000); wf=np.empty(1000)
for i in range(1000):
    ix=rng.randint(0,n,n); accs[i],wf[i]=stat(ix)
res["bootstrap_iid"]={"acc":round(float(accs.mean()),4),"acc_ci":[round(float(np.percentile(accs,2.5)),4),round(float(np.percentile(accs,97.5)),4)],
    "white_fpr":round(float(wf.mean()),4),"white_fpr_ci":[round(float(np.percentile(wf,2.5)),4),round(float(np.percentile(wf,97.5)),4)]}
# clustered by tract_cluster_id
uniq,inv=np.unique(cl,return_inverse=True); order=np.argsort(inv); sinv=inv[order]
bounds=np.searchsorted(sinv,np.arange(len(uniq)+1)); groups=[order[bounds[i]:bounds[i+1]] for i in range(len(uniq))]
ca=np.empty(500); cw=np.empty(500); nt=len(uniq)
for i in range(500):
    pick=rng.randint(0,nt,nt); idx=np.concatenate([groups[g] for g in pick]); ca[i],cw[i]=stat(idx)
res["bootstrap_tract_clustered"]={"n_tracts":int(nt),"acc":round(float(ca.mean()),4),"acc_ci":[round(float(np.percentile(ca,2.5)),4),round(float(np.percentile(ca,97.5)),4)],
    "white_fpr":round(float(cw.mean()),4),"white_fpr_ci":[round(float(np.percentile(cw,2.5)),4),round(float(np.percentile(cw,97.5)),4)]}
# ZRP White-FPR difference bootstrap (common support)
z=load("zrp").set_index("random_row_id"); z=z[z.returned_prediction]
common=ens.index.intersection(z.index); e=ens.loc[common]; zz=z.loc[common]
ey=e.true_coarse_class.values; ep=(e.predicted_class=="White").values; zp=(zz.predicted_class=="White").values; nonw=ey!="White"; m=len(common)
diffs=np.empty(1000)
for i in range(1000):
    ix=rng.randint(0,m,m); nw=nonw[ix]; d=nw.sum(); diffs[i]=(zp[ix]&nw).sum()/d-(ep[ix]&nw).sum()/d
res["zrp_white_fpr_diff_pp"]={"mean":round(float(diffs.mean()*100),2),"ci":[round(float(np.percentile(diffs,2.5)*100),2),round(float(np.percentile(diffs,97.5)*100),2)],"n_common":int(m)}
json.dump(res,open(os.path.join(OUT,"significance.json"),"w"),indent=2)
print(json.dumps(res,indent=2))
