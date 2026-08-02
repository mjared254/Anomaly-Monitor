#!/usr/bin/env python3

import sys, json, glob
from pathlib import Path
import pandas as pd

#Creating Path Object that represents a directory
RAW = Path.home() / "anomaly-monitor" / "data" / "raw"

#match every file that ends in .jsonl
def load(pattern="*.jsonl"):
    frames = []
    #look inside the directory represented by RAW and find every file with that pattern
    #f is a file path
    for f in sorted(RAW.glob(pattern)):
        rows = []
        #read text from f(filepath) and splitlines to make into a list for better visibility
        for line in f.read_text().splitlines():
            try:
                #converts the json text to a Python Object
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        if not rows:
            continue
        df = pd.DataFrame(rows)
        df["session"] = f.stem
        df["label"] = "anomaly" if f.stem.startswith("anomaly") else "baseline"
        frames.append(df)
    if not frames:
        sys.exitr(f"No Data Found in {RAW}")
    return pd.concat(frames, ignore_index=True)

df = load()
#Converting time 
df["dt"] = pd.to_datetime(df["ts"], unit="ns")

print(f"Events: {len(df):,}     Sessions: {df.session.nunique()}")
print(f"\nBy Label:\n{df.label.value_counts()}")
print(f"\nBy Type:\n{df.type.value_counts()}")
print(f"\ntop processes:\n{df.comm.value_counts().head(15)}")

rate = df.groupby("session").apply(
    lambda g: len(g) / max((g.ts.max() - g.ts.min()) / 1e9, 1), include_groups=False
)
print(f"\nevents/sec by session:\n{rate.round(1)}")