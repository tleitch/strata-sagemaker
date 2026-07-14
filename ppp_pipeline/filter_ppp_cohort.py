#!/usr/bin/env python3
"""Two-stage PPP person-name filter (documentation of the cohort construction).
Input: raw SBA PPP FOIA CSVs (public; not redistributed here). Output: LoanNumbers of the
person-name cohort. See ppp_pipeline/README.md."""
import re, sys, pandas as pd, glob
BUSINESS_TYPES={"Sole Proprietorship","Self-Employed Individuals","Independent Contractors","Single Member LLC"}
BIZ_KEYWORDS=("LLC","INC","CORP","CO","LTD","LP","LLP","TRUST","FOUNDATION","CHURCH","ASSOC","COMPANY","SERVICES","ENTERPRISE","GROUP")
def is_person_name(name):
    toks=str(name).split()
    if len(toks)!=2: return False
    if not all(t.isalpha() for t in toks): return False
    up=str(name).upper()
    return not any(k in up.split() for k in BIZ_KEYWORDS)
def main(csv_glob):
    keep=[]
    for f in glob.glob(csv_glob):
        df=pd.read_csv(f,usecols=["LoanNumber","BorrowerName","BusinessType"],dtype=str)
        df=df[df.BusinessType.isin(BUSINESS_TYPES) & df.BorrowerName.notna()]
        df=df[df.BorrowerName.map(is_person_name)]
        keep.append(df[["LoanNumber"]])
    out=pd.concat(keep).drop_duplicates(); out.to_csv("ppp_person_cohort_loannumbers.csv",index=False)
    print("person-name cohort size:",len(out))
if __name__=="__main__": main(sys.argv[1] if len(sys.argv)>1 else "*.csv")
