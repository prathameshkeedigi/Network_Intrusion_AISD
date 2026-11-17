"""Shared by training (train.py) and live detection, so features are identical."""
from collections import defaultdict
import numpy as np

ATTACKER = "10.10.10.1"
MARGIN_MS = 5000      # tolerance around attack start/end times
WINDOW_MS = 10000     # 10-second pattern window

# Per-flow statistics from NFStream (IPs, ports and timestamps are deliberately left out,
# so the model learns behaviour, not "port 80 = attack")
FLOW_FEATURES = ["protocol", "bidirectional_duration_ms", "bidirectional_packets", "bidirectional_bytes",
    "src2dst_packets", "src2dst_bytes", "dst2src_packets", "dst2src_bytes",
    "bidirectional_min_ps", "bidirectional_mean_ps", "bidirectional_stddev_ps", "bidirectional_max_ps",
    "bidirectional_mean_piat_ms", "bidirectional_stddev_piat_ms", "bidirectional_max_piat_ms",
    "bidirectional_syn_packets", "bidirectional_ack_packets", "bidirectional_psh_packets",
    "bidirectional_rst_packets", "bidirectional_fin_packets"]
# Pattern across flows (the finding from the first scan test)
WINDOW_FEATURES = ["win_flows_10s", "win_dst_ports_10s"]
FEATURES = FLOW_FEATURES + WINDOW_FEATURES


class WindowTracker:
    """For each source IP: how many flows, and how many different destination ports,
    started in the last 10 s. Flows are fed in arrival order: the CSV row order offline
    is the same order the live detector receives them, so both give identical values."""
    def __init__(self, window_ms=WINDOW_MS):
        self.window_ms = window_ms
        self.history = defaultdict(list)          # src_ip -> [(first_seen_ms, dst_port)]

    def update(self, src_ip, first_seen_ms, dst_port):
        h = self.history[src_ip]
        h.append((first_seen_ms, dst_port))
        lo = first_seen_ms - self.window_ms
        if len(h) > 5000:                          # forget very old flows
            h[:] = [x for x in h if x[0] >= lo - 60000]
        recent = [p for t, p in h if lo <= t <= first_seen_ms]
        return {"win_flows_10s": len(recent), "win_dst_ports_10s": len(set(recent))}


def add_window_features(df):
    tracker = WindowTracker()
    rows = [tracker.update(s, t, p) for s, t, p in
            zip(df.src_ip, df.bidirectional_first_seen_ms, df.dst_port)]
    out = df.copy()
    for k in WINDOW_FEATURES:
        out[k] = [r[k] for r in rows]
    return out


def label_flows(df, attack_log):
    """Attack label if the flow comes from the attacker inside an attack's time window."""
    labels = np.array(["normal"] * len(df), dtype=object)
    for _, a in attack_log.iterrows():
        inside = ((df.src_ip == ATTACKER) &
                  (df.bidirectional_first_seen_ms >= a.start_ms - MARGIN_MS) &
                  (df.bidirectional_first_seen_ms <= a.end_ms + MARGIN_MS)).values
        labels[inside] = a.label
    return labels
