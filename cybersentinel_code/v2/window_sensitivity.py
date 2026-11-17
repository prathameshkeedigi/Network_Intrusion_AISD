"""Window-size sensitivity test. Run INSIDE Mint: ~/nids-env/bin/python window_sensitivity.py
Re-reads the saved pcaps with different flow idle_timeouts and reports flows + macro-F1,
so the choice of 5 s is backed by numbers (answers sir's window-size remark).
round5.pcap was overwritten, so this uses rounds 3,4 (train) and 6 (test). Behaviour window fixed at 10 s."""
import os
import numpy as np
import pandas as pd
from nfstream import NFStreamer
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
import dataset as ds
import features_v2 as fv
from plugins import EndOnRstFin

D = os.path.expanduser("~/cybersentinel/data")
ROUNDS = {3: "train", 4: "train", 6: "test"}
IDLES = [2, 5, 10, 30]
classes = ["bruteforce", "normal", "scan", "synflood"]
enc = {c: i for i, c in enumerate(classes)}


def build(idle):
    parts = []
    for n, role in ROUNDS.items():
        log = pd.read_csv(f"{D}/logs/v2_round{n}_attack_log.csv")
        fl = NFStreamer(source=f"{D}/pcap/round{n}.pcap", statistical_analysis=True,
                        idle_timeout=idle, active_timeout=30, n_dissections=0, udps=EndOnRstFin()).to_pandas()
        fl = fl[fl.src_ip.str.startswith("10.10.10.")].reset_index(drop=True)
        t = ds.make_table(fl, log, round_no=n)
        t["role"] = role
        parts.append(t)
    return pd.concat(parts, ignore_index=True)


print(f"{'idle_s':>6} {'flows':>7} {'train':>6} {'test':>6} {'macroF1':>8}")
for idle in IDLES:
    df = build(idle)
    tr, te = df[df.role == "train"], df[df.role == "test"]
    m = XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1, tree_method="hist", n_jobs=1, verbosity=0)
    m.fit(tr[fv.FEATURES].to_numpy(float), np.array([enc[c] for c in tr.label]))
    pred = m.predict(te[fv.FEATURES].to_numpy(float))
    f1 = f1_score(np.array([enc[c] for c in te.label]), pred, average="macro")
    print(f"{idle:6d} {len(df):7d} {len(tr):6d} {len(te):6d} {f1:8.4f}")
print("\nNote: lower idle_timeout = faster alerts but may split long flows; higher = fewer, slower flows.")
