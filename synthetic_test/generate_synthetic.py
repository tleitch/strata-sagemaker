#!/usr/bin/env python3
"""Generate a fully synthetic name+address test set (no real people) for exercising the
STRATA inference path. Deterministic (seeded). Produces synthetic_records.csv with an
intended coarse class per row; actual scoring is done through the SageMaker endpoint /
AWS Marketplace artifact (contact terry@aequum.ai for no-cost review access), and the
returned probabilities are compared against expected_outputs.json conventions.

These records are constructed from synthetic name fragments and placeholder addresses.
They are NOT drawn from any real individual, voter file, or loan record.
"""
import csv, json, os, random
random.seed(20260714)
HERE=os.path.dirname(os.path.abspath(__file__))
# synthetic, non-real name fragments grouped only to exercise the model's input space
FIRST=["Alex","Jordan","Taylor","Morgan","Riley","Casey","Sam","Jamie","Chris","Pat",
       "Devon","Sydney","Avery","Quinn","Reese","Skyler","Drew","Harper","Rowan","Emerson"]
LAST=["Carter","Nguyen","Garcia","Okafor","Kim","Rossi","Patel","Johnson","Lopez","Cohen",
      "Yamamoto","Ali","Novak","Santos","Freeman","Walsh","Mbeki","Delgado","Park","Abara"]
STREETS=["Main St","Oak Ave","Elm Rd","2nd St","Park Blvd","Cedar Ln","Maple Dr","Lake Way"]
STATES=["FL","GA","NC","TX","CA","NY","IL","OH","AZ","WA"]
CLASSES=["White","Black","Hispanic","Asian","Other"]
rows=[]
for i in range(500):
    rows.append({
        "synthetic_id": i,
        "first_name": random.choice(FIRST),
        "last_name": random.choice(LAST),
        "street_address": f"{random.randint(1,9999)} {random.choice(STREETS)}",
        "city": "Testville",
        "state": random.choice(STATES),
        "zip": f"{random.randint(10000,99999)}",
        "intended_class": random.choice(CLASSES),   # label by construction; for smoke-testing only
    })
with open(os.path.join(HERE,"synthetic_records.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump({
    "description":"Expected-output conventions for scoring synthetic_records.csv via the STRATA endpoint.",
    "n_records":len(rows),
    "endpoint_output_schema":{"predicted_class":"str in {White,Black,Hispanic,Asian,Other}",
        "probability_white":"float","probability_black":"float","probability_hispanic":"float",
        "probability_asian":"float","probability_other":"float"},
    "rounding":"probabilities reported to 4 decimals; class = argmax",
    "note":"These synthetic records exercise the input/inference path only; they are not a "
           "held-out benchmark. Metric-level reproduction of the paper uses predictions/ (see REPRODUCIBILITY.md).",
}, open(os.path.join(HERE,"expected_outputs.json"),"w"), indent=2)
print(f"wrote synthetic_records.csv ({len(rows)} rows) and expected_outputs.json")
