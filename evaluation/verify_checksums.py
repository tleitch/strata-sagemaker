#!/usr/bin/env python3
"""Verify every file listed in CHECKSUMS.md against its SHA-256. Usage: python evaluation/verify_checksums.py CHECKSUMS.md"""
import sys,hashlib,os,re
manifest=sys.argv[1] if len(sys.argv)>1 else "CHECKSUMS.md"
root=os.path.dirname(os.path.abspath(manifest)) or "."
ok=bad=0
for line in open(manifest):
    m=re.match(r"^([0-9a-f]{64})\s+(.+?)\s*$",line.strip())
    if not m: continue
    dig,path=m.group(1),m.group(2)
    fp=os.path.join(root,path)
    if not os.path.exists(fp): print("MISSING",path); bad+=1; continue
    h=hashlib.sha256(open(fp,"rb").read()).hexdigest()
    if h==dig: ok+=1
    else: print("MISMATCH",path); bad+=1
print(f"checksums: {ok} ok, {bad} bad")
sys.exit(1 if bad else 0)
