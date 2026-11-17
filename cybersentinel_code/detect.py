"""Live detector: NFStream flows -> same features as training -> XGBoost -> ALERT."""
import json, sys, time
import pandas as pd
from nfstream import NFStreamer
from xgboost import XGBClassifier
from features import FLOW_FEATURES, FEATURES, WindowTracker

BASE = "/home/prathamesh/cybersentinel/"
iface = sys.argv[1] if len(sys.argv) > 1 else "enp0s8"

model = XGBClassifier()
model.load_model(BASE + "model.json")
classes = json.load(open(BASE + "classes.json"))
tracker = WindowTracker()
throttle = {}                      # (src_ip, label) -> [last_print_time, flows_since_last_print]
totals = {c: 0 for c in classes}

print(f"CyberSentinel live detector on {iface} | classes: {classes} | Ctrl+C to stop", flush=True)
try:
    for f in NFStreamer(source=iface, statistical_analysis=True, idle_timeout=5, active_timeout=30):
        row = {c: getattr(f, c) for c in FLOW_FEATURES}
        row.update(tracker.update(f.src_ip, f.bidirectional_first_seen_ms, f.dst_port))
        proba = model.predict_proba(pd.DataFrame([row], columns=FEATURES))[0]
        k = int(proba.argmax())
        label, conf = classes[k], float(proba[k])
        totals[label] += 1
        t = time.strftime("%H:%M:%S")

        if label == "normal":
            print(f"{t}  ok      {f.src_ip} -> {f.dst_ip}:{f.dst_port}  ({conf:.2f})", flush=True)
            continue

        # Attacks create hundreds of flows: print one ALERT line per source+attack every 3 s
        st = throttle.setdefault((f.src_ip, label), [0.0, 0])
        st[1] += 1
        now = time.time()
        if now - st[0] >= 3:
            print(f"{t}  [ALERT] {label.upper():10s} from {f.src_ip} -> {f.dst_ip}  "
                  f"(+{st[1]} flows, confidence {conf:.2f}, ports in last 10 s: {row['win_dst_ports_10s']})",
                  flush=True)
            st[0], st[1] = now, 0
except KeyboardInterrupt:
    pass
print("\nStopped. Flows per predicted class:", totals)
