# PPP cohort construction

Documents how the national PPP person-name evaluation cohort (N=111,062) was built from the
public SBA PPP FOIA loan files. The raw SBA CSVs are publicly downloadable from the U.S.
Small Business Administration; we do not redistribute them here.

Stages (see filter_ppp_cohort.py):
1. **BusinessType filter (Stage 1):** BusinessType in {Sole Proprietorship, Self-Employed
   Individuals, Independent Contractors, Single Member LLC}.
2. **Person-name heuristic (Stage 2):** BorrowerName is exactly two alphabetic tokens with no
   business keywords. (In the held-out cohort this yields Sole Proprietorship + Self-Employed
   only; no LLC/Independent-Contractor record survives Stage 2.)
3. **Geocoding:** address -> census tract via an offline TIGER/Line resolver (geocode_ppp.py,
   requires TIGER/Line shapefiles). Only tract-resolved records can be scored.
4. Of 125,081 tract-resolved held-out PPP records, 111,062 (88.8%) pass Stages 1-2.

score_ppp_endpoint.py documents hitting the SageMaker inference endpoint (requires the
commercial/academic artifact; contact terry@aequum.ai for no-cost review access).
