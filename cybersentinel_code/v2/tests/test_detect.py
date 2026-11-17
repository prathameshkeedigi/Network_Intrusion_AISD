"""Tests for detect_core.py, written before the live runner. Uses the shipped model + round6 data."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os as _os
import pandas as pd
import pytest
import detect_core as dc

HERE = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
ROUND6 = _os.path.join(HERE, "data", "flows", "round6.csv")
HAVE_MODEL = _os.path.exists(_os.path.join(HERE, "models", "best_xgb.json"))
HAVE_DATA = _os.path.exists(ROUND6)


def test_alert_text_contains_attacker_ip_and_timing():
    a = dc.make_alert({"src_ip": "10.10.10.1", "dst_ip": "10.10.10.2", "dst_port": 22},
                      "scan", 0.99, 0.6, 0.4)
    t = dc.alert_text(a)
    assert "10.10.10.1" in t and "SCAN" in t and "predict" in t and "delay" in t


def test_throttle_limits_rate():
    th = dc.Throttle(seconds=3)
    assert th.allow(("10.10.10.1", "scan"), now=100) is True
    assert th.allow(("10.10.10.1", "scan"), now=101) is False     # within 3 s -> blocked
    assert th.allow(("10.10.10.1", "scan"), now=104) is True      # after 3 s -> allowed


def test_incident_tracker_aggregates_per_ip():
    inc = dc.IncidentTracker()
    for port, lab in [(22, "scan"), (23, "scan"), (80, "synflood")]:
        inc.add(dc.make_alert({"src_ip": "10.10.10.1", "dst_ip": "10.10.10.2", "dst_port": port},
                              lab, 0.9, 0.5, 0.0))
    s = inc.summary()
    assert len(s) == 1 and s[0]["attacker_ip"] == "10.10.10.1"
    assert s[0]["flows"] == 3 and s[0]["distinct_ports"] == 3
    assert set(s[0]["attacks"].split(",")) == {"scan", "synflood"}


@pytest.mark.skipif(not (HAVE_MODEL and HAVE_DATA), reason="needs trained model + round6 data")
def test_replay_flags_attacker_not_innocent():
    df = pd.read_csv(ROUND6)
    alerts, incidents = dc.replay(df)
    attacker_ips = {a["attacker_ip"] for a in alerts}
    # the innocent user 10.10.10.3 must NEVER raise an alert
    assert "10.10.10.3" not in attacker_ips
    # the attacker 10.10.10.1 must be flagged, and its incident lists real attack types
    assert "10.10.10.1" in attacker_ips
    inc = {r["attacker_ip"]: r for r in incidents}
    assert "10.10.10.1" in inc
    assert {"scan", "synflood"} <= set(inc["10.10.10.1"]["attacks"].split(","))


@pytest.mark.skipif(not (HAVE_MODEL and HAVE_DATA), reason="needs trained model + round6 data")
def test_replay_every_alert_has_attacker_ip():
    df = pd.read_csv(ROUND6)
    alerts, _ = dc.replay(df)
    assert len(alerts) > 0
    for a in alerts:
        assert a["attacker_ip"] and a["label"] != "normal" and a["predict_ms"] >= 0
