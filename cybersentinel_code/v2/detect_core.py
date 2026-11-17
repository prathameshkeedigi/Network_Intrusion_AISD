"""Core of the v2 live detector: predict -> alert -> incident. No nfstream here, so it is
testable on Windows and reused unchanged by the live/pcap runner (detect_v2.py)."""
import json, os, time
import numpy as np
from xgboost import XGBClassifier
import features_v2 as fv

HERE = os.path.dirname(os.path.abspath(__file__))
NORMAL = "normal"


def load_model(models_dir=None):
    models_dir = models_dir or os.path.join(HERE, "models")
    meta = json.load(open(os.path.join(models_dir, "best_meta.json")))
    model = XGBClassifier()
    model.load_model(os.path.join(models_dir, "best_xgb.json"))
    return model, meta["features"], meta["classes"]


def predict_row(model, feat_order, classes, row):
    """row: dict-like with all 66 feature values. Returns (label, confidence, predict_ms)."""
    x = np.fromiter((row[k] for k in feat_order), dtype=np.float32, count=len(feat_order)).reshape(1, -1)
    t = time.perf_counter()
    proba = model.predict_proba(x)[0]
    ms = (time.perf_counter() - t) * 1000
    k = int(proba.argmax())
    return classes[k], float(proba[k]), ms


def make_alert(env, label, confidence, predict_ms, delay_s, now=None):
    return {"time": time.strftime("%H:%M:%S", time.localtime(now)) if now else time.strftime("%H:%M:%S"),
            "attacker_ip": env["src_ip"], "victim_ip": env["dst_ip"], "dst_port": int(env["dst_port"]),
            "label": label, "confidence": round(confidence, 3),
            "predict_ms": round(predict_ms, 3), "delay_s": round(delay_s, 2)}


def alert_text(a):
    return (f"{a['time']}  [ALERT] {a['label'].upper():10s} from {a['attacker_ip']} -> "
            f"{a['victim_ip']}:{a['dst_port']}  | conf {a['confidence']} | "
            f"predict {a['predict_ms']}ms | delay {a['delay_s']}s")


class Throttle:
    """At most one printed line per key every `seconds` (keeps a flood from flooding the screen)."""
    def __init__(self, seconds=3):
        self.sec = seconds
        self.last = {}

    def allow(self, key, now=None):
        now = time.time() if now is None else now
        if now - self.last.get(key, -1e9) >= self.sec:
            self.last[key] = now
            return True
        return False


class IncidentTracker:
    """One row per attacker IP: when, what, how much. Printed and saved on stop."""
    def __init__(self):
        self.by_ip = {}

    def add(self, a):
        d = self.by_ip.setdefault(a["attacker_ip"],
                                  {"first": a["time"], "last": a["time"], "labels": set(),
                                   "flows": 0, "ports": set(), "victims": set()})
        d["last"] = a["time"]; d["labels"].add(a["label"]); d["flows"] += 1
        d["ports"].add(a["dst_port"]); d["victims"].add(a["victim_ip"])

    def summary(self):
        return [{"attacker_ip": ip, "first_seen": d["first"], "last_seen": d["last"],
                 "attacks": ",".join(sorted(d["labels"])), "flows": d["flows"],
                 "distinct_ports": len(d["ports"]), "victims": len(d["victims"])}
                for ip, d in self.by_ip.items()]


def replay(df, model=None, feat_order=None, classes=None):
    """Run the predict->alert->incident path over a flow table (same core as live).
    df has the envelope + 66 feature columns. Returns (alerts, incident_rows)."""
    if model is None:
        model, feat_order, classes = load_model()
    inc = IncidentTracker()
    alerts = []
    for r in df.itertuples(index=False):
        row = r._asdict()
        label, conf, ms = predict_row(model, feat_order, classes, row)
        if label == NORMAL:
            continue
        a = make_alert({"src_ip": row["src_ip"], "dst_ip": row["dst_ip"], "dst_port": row["dst_port"]},
                       label, conf, ms, delay_s=0.0)
        alerts.append(a); inc.add(a)
    return alerts, inc.summary()
