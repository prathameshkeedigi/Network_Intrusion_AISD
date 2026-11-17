"""Generate an HTML EDA report with ydata-profiling. Run with the isolated edaenv python.
Loads the 4 recorded rounds and profiles the features + label (timestamps dropped: huge cardinality)."""
import glob, os
import pandas as pd
from ydata_profiling import ProfileReport

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results", "eda_report.html")

df = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(HERE, "data/flows/round*.csv")))],
               ignore_index=True)
# drop the two raw timestamps (per-flow, near-unique: noise in a profile report)
df = df.drop(columns=[c for c in ["bidirectional_first_seen_ms", "bidirectional_last_seen_ms"] if c in df.columns])
print(f"Profiling {len(df)} flows x {df.shape[1]} columns ...")

profile = ProfileReport(
    df, title="CyberSentinel AI v2 — EDA Report (10,676 flows, rounds 3-6)",
    explorative=True, correlations={"auto": {"calculate": True}},
    dataset={"description": "Labelled network flows from the private labnet lab. "
             "Attacker 10.10.10.1, innocent user 10.10.10.3, victim 10.10.10.2. "
             "66 flow features; label in {normal, scan, bruteforce, synflood}."})
profile.to_file(OUT)
print("Saved", OUT)
