"""Tests for features_v2.py, written BEFORE the code (TDD). Run: python -m pytest -q  (inside v2/)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import pytest
import features_v2 as fv


def flow(src="10.10.10.1", dst="10.10.10.2", dport=80, t=0, **kw):
    """A fake NFStream flow as a dict: every feature 0 unless given."""
    f = {k: 0 for k in fv.NFSTREAM_FEATURES}
    f.update(src_ip=src, dst_ip=dst, src_port=40000, dst_port=dport,
             bidirectional_first_seen_ms=t, bidirectional_last_seen_ms=t, protocol=6)
    f.update(kw)
    return f


# ---------- feature list ----------
def test_feature_count_is_66():
    assert len(fv.NFSTREAM_FEATURES) == 58
    assert len(fv.FEATURES) == 58 + 3 + 5


def test_feature_names_unique():
    assert len(set(fv.FEATURES)) == len(fv.FEATURES)


@pytest.mark.parametrize("bad", ["ip", "port", "first_seen", "last_seen", "mac", "oui", "id"])
def test_no_identity_or_time_features(bad):
    # The model must learn behaviour, not addresses or clock times
    for name in fv.FEATURES:
        parts = name.split("_")
        assert bad not in parts, f"{name} contains '{bad}'"


# ---------- engineered features ----------
def test_rates_zero_duration_give_zero_not_inf():
    tr = fv.WindowTracker()
    row = fv.compute_features(flow(bidirectional_bytes=100, bidirectional_packets=2,
                                   bidirectional_duration_ms=0), tr)
    assert row["bytes_per_s"] == 0 and row["packets_per_s"] == 0


def test_rates_normal_case():
    tr = fv.WindowTracker()
    row = fv.compute_features(flow(bidirectional_bytes=1000, bidirectional_packets=10,
                                   bidirectional_duration_ms=500), tr)
    assert row["bytes_per_s"] == pytest.approx(2000.0)
    assert row["packets_per_s"] == pytest.approx(20.0)


def test_down_up_ratio():
    tr = fv.WindowTracker()
    row = fv.compute_features(flow(src2dst_bytes=99, dst2src_bytes=500), tr)
    assert row["down_up_ratio"] == pytest.approx(5.0)


# ---------- 10-second window ----------
def test_window_counts_ports_ips_and_expires_after_10s():
    tr = fv.WindowTracker()
    for i, p in enumerate([21, 22, 23, 80, 443]):
        r = fv.compute_features(flow(dport=p, t=i * 100), tr)
    assert r["win_flows_10s"] == 5 and r["win_dst_ports_10s"] == 5 and r["win_dst_ips_10s"] == 1
    r = fv.compute_features(flow(dport=8080, dst="10.10.10.9", t=11_000), tr)   # 11 s later
    assert r["win_flows_10s"] == 1 and r["win_dst_ports_10s"] == 1


def test_window_is_per_source_ip():
    tr = fv.WindowTracker()
    for i in range(20):
        fv.compute_features(flow(src="10.10.10.1", dport=1000 + i, t=i), tr)
    r = fv.compute_features(flow(src="10.10.10.3", dport=80, t=50), tr)
    assert r["win_flows_10s"] == 1     # innocent user not affected by attacker's scan


def test_rst_ratio_and_half_open():
    tr = fv.WindowTracker()
    # scan probe: SYN from attacker, RST from victim, attacker never ACKs
    fv.compute_features(flow(t=0, src2dst_syn_packets=1, bidirectional_rst_packets=1), tr)
    # normal web flow: SYN + ACKs from client, no RST
    r = fv.compute_features(flow(t=10, src2dst_syn_packets=1, src2dst_ack_packets=4), tr)
    assert r["win_rst_ratio_10s"] == pytest.approx(0.5)
    assert r["win_half_open_10s"] == 1


# ---------- vector + parity ----------
def test_vector_order_and_type():
    tr = fv.WindowTracker()
    v = fv.feature_vector(flow(bidirectional_bytes=7), tr)
    assert isinstance(v, np.ndarray) and v.shape == (1, len(fv.FEATURES)) and v.dtype == np.float32
    assert v[0, fv.FEATURES.index("bidirectional_bytes")] == 7


def test_offline_table_equals_live_rows():
    """Training (whole table) and live (one flow at a time) must give identical numbers."""
    flows = [flow(src=s, dport=p, t=t, bidirectional_bytes=b, bidirectional_duration_ms=d,
                  src2dst_syn_packets=1, bidirectional_rst_packets=r)
             for s, p, t, b, d, r in [("10.10.10.1", 22, 0, 120, 3, 1), ("10.10.10.3", 80, 5, 900, 40, 0),
                                      ("10.10.10.1", 23, 9, 120, 2, 1), ("10.10.10.1", 22, 12_000, 4000, 900, 0)]]
    table = fv.build_features(pd.DataFrame(flows))
    tr = fv.WindowTracker()
    live = np.vstack([fv.feature_vector(f, tr) for f in flows])
    np.testing.assert_allclose(table[fv.FEATURES].to_numpy(dtype=np.float32), live)


# ---------- labels ----------
def test_labels_only_attacker_ip_inside_attack_time():
    df = pd.DataFrame([flow(src="10.10.10.1", t=10_000), flow(src="10.10.10.3", t=10_000),
                       flow(src="10.10.10.1", t=60_000)])
    log = pd.DataFrame([{"label": "scan", "start_ms": 8_000, "end_ms": 12_000}])
    assert list(fv.label_flows(df, log)) == ["scan", "normal", "normal"]
