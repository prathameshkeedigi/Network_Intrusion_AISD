"""CyberSentinel v2 features. ONE file shared by training (whole table) and live detection
(one flow at a time), so both always produce identical numbers.

Features = 58 NFStream statistics + 3 engineered rates/ratios + 5 behaviour-window counts = 66.
IPs, ports, MACs and timestamps are NEVER features: they stay in the "envelope" for alerts.
Does not import nfstream, so it can be tested on Windows.
"""
from collections import defaultdict, deque
from collections.abc import Mapping
import numpy as np
import pandas as pd

WINDOW_MS = 10_000            # behaviour window per source IP
KEEP_MS = WINDOW_MS + 60_000  # flows arrive when they END, not when they start: keep a margin
MARGIN_MS = 5_000             # label tolerance around attack start/end

_DIRS = ["bidirectional", "src2dst", "dst2src"]
NFSTREAM_FEATURES = (
    ["protocol"]
    + [f"{d}_duration_ms" for d in _DIRS]
    + [f"{d}_{m}" for d in _DIRS for m in ("packets", "bytes")]
    + [f"{d}_{s}_ps" for d in _DIRS for s in ("min", "mean", "stddev", "max")]
    + [f"{d}_{s}_piat_ms" for d in _DIRS for s in ("min", "mean", "stddev", "max")]
    + [f"{d}_{fl}_packets" for d in _DIRS for fl in ("syn", "cwr", "ece", "urg", "ack", "psh", "rst", "fin")]
)
ENGINEERED_FEATURES = ["bytes_per_s", "packets_per_s", "down_up_ratio"]
WINDOW_FEATURES = ["win_flows_10s", "win_dst_ports_10s", "win_dst_ips_10s",
                   "win_rst_ratio_10s", "win_half_open_10s"]
FEATURES = NFSTREAM_FEATURES + ENGINEERED_FEATURES + WINDOW_FEATURES

ENVELOPE = ["src_ip", "src_port", "dst_ip", "dst_port",
            "bidirectional_first_seen_ms", "bidirectional_last_seen_ms"]


def _get(f, k):
    """Read a field from an NFStream flow (attributes), a dict/Series, or an itertuples row."""
    if isinstance(f, (Mapping, pd.Series)):
        return f[k]
    return getattr(f, k)


class WindowTracker:
    """Per source IP: what it did in the last 10 s (flows, ports, victims, RST share, half-open)."""

    def __init__(self, window_ms=WINDOW_MS):
        self.window_ms = window_ms
        self.history = defaultdict(deque)   # src_ip -> deque[(t, dst_ip, dst_port, had_rst, half_open)]

    def update(self, src_ip, t, dst_ip, dst_port, had_rst, half_open):
        h = self.history[src_ip]
        h.append((t, dst_ip, dst_port, had_rst, half_open))
        while h and h[0][0] < t - KEEP_MS:
            h.popleft()
        lo = t - self.window_ms
        recent = [x for x in h if lo <= x[0] <= t]
        n = len(recent)
        return {
            "win_flows_10s": n,
            "win_dst_ports_10s": len({x[2] for x in recent}),
            "win_dst_ips_10s": len({x[1] for x in recent}),
            "win_rst_ratio_10s": sum(x[3] for x in recent) / n,
            "win_half_open_10s": sum(x[4] for x in recent),
        }


def compute_features(f, tracker):
    """All 66 features for one flow, as a dict. Updates the tracker (call once per flow, in arrival order)."""
    row = {k: float(_get(f, k)) for k in NFSTREAM_FEATURES}
    secs = row["bidirectional_duration_ms"] / 1000.0
    row["bytes_per_s"] = row["bidirectional_bytes"] / secs if secs > 0 else 0.0
    row["packets_per_s"] = row["bidirectional_packets"] / secs if secs > 0 else 0.0
    row["down_up_ratio"] = row["dst2src_bytes"] / (row["src2dst_bytes"] + 1.0)
    had_rst = row["bidirectional_rst_packets"] > 0
    half_open = row["src2dst_syn_packets"] > 0 and row["src2dst_ack_packets"] == 0
    row.update(tracker.update(_get(f, "src_ip"), _get(f, "bidirectional_first_seen_ms"),
                              _get(f, "dst_ip"), _get(f, "dst_port"), had_rst, half_open))
    return row


def feature_vector(f, tracker):
    """Live path: one flow -> NumPy row (1 x 66, float32) in FEATURES order. No pandas, no disk."""
    row = compute_features(f, tracker)
    return np.fromiter((row[k] for k in FEATURES), dtype=np.float32, count=len(FEATURES)).reshape(1, -1)


def build_features(df):
    """Training path: a whole flow table (rows in arrival order) -> envelope + 66 feature columns."""
    tracker = WindowTracker()
    rows = [compute_features(r, tracker) for r in df.itertuples(index=False)]
    feats = pd.DataFrame(rows, columns=FEATURES, index=df.index)
    keep = [c for c in ENVELOPE if c in df.columns]
    return pd.concat([df[keep], feats], axis=1)


def label_flows(df, attack_log, attacker="10.10.10.1", margin_ms=MARGIN_MS):
    """Attack label only if the flow comes from the attacker IP inside an attack's time window."""
    labels = np.array(["normal"] * len(df), dtype=object)
    for a in attack_log.itertuples(index=False):
        inside = ((df["src_ip"] == attacker)
                  & (df["bidirectional_first_seen_ms"] >= a.start_ms - margin_ms)
                  & (df["bidirectional_first_seen_ms"] <= a.end_ms + margin_ms)).to_numpy()
        labels[inside] = a.label
    return labels
