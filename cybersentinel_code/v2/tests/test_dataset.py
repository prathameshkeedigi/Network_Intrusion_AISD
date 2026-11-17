"""Tests for dataset.py (flow table -> labelled training table), written before the code."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import features_v2 as fv
import dataset as ds


def flow(src, t, dport=80, **kw):
    f = {k: 0 for k in fv.NFSTREAM_FEATURES}
    f.update(src_ip=src, dst_ip="10.10.10.2", src_port=40000, dst_port=dport, protocol=6,
             bidirectional_first_seen_ms=t, bidirectional_last_seen_ms=t, expiration_id=-1)
    f.update(kw)
    return f


LOG = pd.DataFrame([{"label": "scan", "start_ms": 10_000, "end_ms": 20_000},
                    {"label": "synflood", "start_ms": 50_000, "end_ms": 70_000}])


def make():
    flows = pd.DataFrame([flow("10.10.10.1", 1_000),          # attacker, before attacks -> normal
                          flow("10.10.10.1", 12_000, 22),     # attacker in scan window -> scan
                          flow("10.10.10.3", 12_500),         # innocent during scan -> normal
                          flow("10.10.10.1", 60_000),         # attacker in flood window -> synflood
                          flow("10.10.10.3", 61_000),         # innocent during flood -> normal
                          flow("10.10.10.1", 200_000)])       # attacker, long after -> normal
    return ds.make_table(flows, LOG, round_no=3)


def test_columns_and_order():
    t = make()
    assert list(t.columns) == ["round"] + fv.ENVELOPE + fv.FEATURES + ["label"]
    assert (t["round"] == 3).all()


def test_labels_innocent_always_normal():
    t = make()
    assert list(t["label"]) == ["normal", "scan", "normal", "synflood", "normal", "normal"]
    assert (t.loc[t.src_ip == "10.10.10.3", "label"] == "normal").all()


def test_attack_window_report_counts_attacker_flows():
    rep = ds.attack_window_report(make(), LOG)
    assert list(rep["label"]) == ["scan", "synflood"]
    assert list(rep["attacker_flows"]) == [1, 1]
    assert list(rep["duration_s"]) == [10.0, 20.0]


def test_empty_attack_window_is_flagged():
    log = pd.DataFrame([{"label": "bruteforce", "start_ms": 500_000, "end_ms": 510_000}])
    rep = ds.attack_window_report(make(), log)
    assert rep["attacker_flows"].iloc[0] == 0 and rep["ok"].iloc[0] == False
