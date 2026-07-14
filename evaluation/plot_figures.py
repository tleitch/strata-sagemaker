#!/usr/bin/env python3
"""Reproduce Figures 1 (voter) and 2 (PPP person cohort): per-class misclassification
rate vs census-tract income decile, with 95% bootstrap CI bands, from predictions/.
Writes outputs/figure1_voter.png and outputs/figure2_ppp.png.
"""
import os,numpy as np,pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED=os.path.join(HERE,"predictions"); OUT=os.path.join(HERE,"outputs"); os.makedirs(OUT,exist_ok=True)
CLASSES=["White","Black","Hispanic","Asian"]
def load(coh,m): return pd.read_parquet(os.path.join(PRED,coh,f"{m}_predictions.parquet"))
def series(coh,m,mask_fn,cls,deciles):
    d=load(coh,m); d=d[mask_fn(d)]; d=d[d.returned_prediction]
    d=d[d.true_coarse_class==cls]
    rng=np.random.RandomState(42); med=[];lo=[];hi=[]
    for dec in deciles:
        g=d[d.income_decile==dec]; n=len(g)
        if n<30: med.append(np.nan);lo.append(np.nan);hi.append(np.nan); continue
        mis=(g.predicted_class!=cls).to_numpy().astype(float)
        med.append(mis.mean())
        bs=np.array([mis[rng.randint(0,n,n)].mean() for _ in range(500)])
        lo.append(np.percentile(bs,2.5)); hi.append(np.percentile(bs,97.5))
    return np.array(med),np.array(lo),np.array(hi)

def figure(coh,models,disp,styles,mask_fn,fname,suptitle):
    deciles=sorted(load(coh,models[0]).income_decile.dropna().unique())
    fig,axes=plt.subplots(2,2,figsize=(12,10)); fig.suptitle(suptitle,fontsize=13)
    for ax,cls in zip(axes.ravel(),CLASSES):
        for m in models:
            med,lo,hi=series(coh,m,mask_fn,cls,deciles); x=np.array(deciles); ok=~np.isnan(med)
            col,ls=styles[m]; ax.plot(x[ok],med[ok],ls,color=col,label=disp[m],lw=1.8); ax.fill_between(x[ok],lo[ok],hi[ok],color=col,alpha=0.18,lw=0)
        ax.set_title(f"Misclassification rate by income decile: {cls} (true class)",fontsize=11)
        ax.set_xlabel("Census-tract income decile (1--10)"); ax.set_ylabel("Misclassification rate")
        ax.set_ylim(0,1); ax.grid(True,ls=":",alpha=.5); ax.legend(fontsize=9)
    plt.tight_layout(rect=[0,0,1,.98]); plt.savefig(os.path.join(OUT,fname),dpi=150,bbox_inches="tight"); plt.close()
    print("  wrote outputs/"+fname)

vmask=lambda d: d.true_fine_class!="multi"
pmask=lambda d: d.person_name_cohort==True
vmodels=["lstm_nameonly","strata_base","bisg","bifsg","zrp","strata_ensemble"]
vdisp={"lstm_nameonly":"Name-only LSTM","strata_base":"STRATA base","bisg":"BISG","bifsg":"BIFSG","zrp":"ZRP","strata_ensemble":"STRATA ensemble"}
vsty={"lstm_nameonly":("#1f77b4","-"),"strata_base":("#ff7f0e","--"),"bisg":("#2ca02c","-."),"bifsg":("#d62728",":"),"zrp":("#9467bd","-"),"strata_ensemble":("#8c564b","--")}
pmodels=["lstm_nameonly","strata_base","strata_ensemble","zrp"]
pdisp={"lstm_nameonly":"Name-only LSTM","strata_base":"STRATA base","strata_ensemble":"STRATA ensemble","zrp":"ZRP"}
psty={"lstm_nameonly":("#1f77b4","-"),"strata_base":("#ff7f0e","--"),"strata_ensemble":("#8c564b","--"),"zrp":("#9467bd","-")}
print("Reproducing figures:")
figure("voter_holdout",vmodels,vdisp,vsty,vmask,"figure1_voter.png","Voter holdout: misclassification by tract-income decile (95% bootstrap CI)")
figure("ppp_holdout",pmodels,pdisp,psty,pmask,"figure2_ppp.png","PPP person-name cohort: misclassification by tract-income decile (95% bootstrap CI)")
