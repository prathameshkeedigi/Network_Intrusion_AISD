"""Run INSIDE Mint:  ~/nids-env/bin/python check_nfstream.py <file.pcap>
Checks against the REAL NFStream: (1) all 58 feature names exist, (2) the RST/FIN plugin ends flows early,
(3) features_v2 builds 66 numbers without errors, (4) single-flow feature time."""
import sys, time
import numpy as np
import nfstream
from nfstream import NFStreamer
import features_v2 as fv
from plugins import EndOnRstFin

pcap = sys.argv[1]
print("NFStream version:", getattr(nfstream, "__version__", "unknown"))

base = NFStreamer(source=pcap, statistical_analysis=True, idle_timeout=5, active_timeout=30,
                  n_dissections=0).to_pandas()
print(f"\n[1] Without plugin: {len(base)} flows, {len(base.columns)} columns")
missing = [c for c in fv.NFSTREAM_FEATURES if c not in base.columns]
print("    Missing feature names:", missing if missing else "NONE  -> all 58 present  OK")

plug = NFStreamer(source=pcap, statistical_analysis=True, idle_timeout=5, active_timeout=30,
                  n_dissections=0, udps=EndOnRstFin()).to_pandas()
print(f"\n[2] With RST/FIN plugin: {len(plug)} flows")
print("    expiration_id counts (0=idle, 1=active, -1=ended by plugin):")
print("   ", plug["expiration_id"].value_counts().to_dict())

feats = fv.build_features(plug)
print(f"\n[3] features_v2 table: {feats.shape[0]} rows x {len(fv.FEATURES)} features")
bad = int((~np.isfinite(feats[fv.FEATURES].to_numpy(dtype=float))).sum())
print("    NaN / infinite values:", bad, " OK" if bad == 0 else " PROBLEM")

tr = fv.WindowTracker()
rows = list(plug.itertuples(index=False))
s = time.perf_counter()
for r in rows:
    fv.feature_vector(r, tr)
ms = (time.perf_counter() - s) / max(len(rows), 1) * 1000
print(f"\n[4] Feature building: {ms:.3f} ms per flow (in this VM)")
print("\nSources seen:", plug["src_ip"].value_counts().head(5).to_dict())
