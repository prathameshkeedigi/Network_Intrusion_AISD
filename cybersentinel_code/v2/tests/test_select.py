"""Tests for select_features.py, written before the code (TDD)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import select_features as sf
import features_v2 as fv

FEATS = ["bidirectional_bytes", "src2dst_bytes", "bidirectional_packets", "protocol"]


def synth(n=400, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, n)
    df = pd.DataFrame({
        "bidirectional_bytes": y * 100 + rng.normal(0, 5, n),    # informative
        "src2dst_bytes": y * 100 + rng.normal(0, 5, n),          # ~ duplicate of the above
        "bidirectional_packets": rng.normal(0, 1, n),            # pure noise
        "protocol": np.full(n, 6.0),                             # constant
    })
    df["label"] = np.where(y == 1, "scan", "normal")
    return df


def test_drop_constant():
    kept, dropped = sf.drop_constant(synth(), FEATS)
    assert dropped == ["protocol"] and "protocol" not in kept


def test_drop_correlated_keeps_exactly_one_of_a_pair():
    kept, pairs = sf.drop_correlated(synth(), ["bidirectional_bytes", "src2dst_bytes", "bidirectional_packets"], thresh=0.9)
    assert len([f for f in kept if f in ("bidirectional_bytes", "src2dst_bytes")]) == 1
    assert "bidirectional_packets" in kept          # noise is not correlated, so it stays
    assert len(pairs) == 1


def test_select_returns_subset_and_no_identity():
    res = sf.select(synth(), features=FEATS, seed=0)
    assert set(res["selected"]).issubset(set(FEATS))
    for name in res["selected"]:
        for bad in ("ip", "port", "first_seen", "last_seen", "mac"):
            assert bad not in name


def test_select_drops_constant_and_redundant():
    res = sf.select(synth(), features=FEATS, seed=0)
    assert "protocol" in res["dropped_constant"]
    assert len([f for f in res["selected"] if f in ("bidirectional_bytes", "src2dst_bytes")]) == 1


def test_informative_ranks_above_noise():
    res = sf.select(synth(), features=FEATS, seed=0)
    # the informative feature must rank above the pure-noise one
    assert res["selected"].index("bidirectional_packets") == len(res["selected"]) - 1


def test_reproducible_with_same_seed():
    assert sf.select(synth(), features=FEATS, seed=0) == sf.select(synth(), features=FEATS, seed=0)


def test_default_features_are_the_66_with_no_identity():
    # a smoke test on the real feature list: nothing in the envelope leaks in
    rng = np.random.default_rng(0)
    data = {c: rng.normal(0, 1, 60) for c in fv.FEATURES}
    data["label"] = rng.choice(["normal", "scan"], 60)
    res = sf.select(pd.DataFrame(data), seed=0)
    assert set(res["selected"]).issubset(set(fv.FEATURES))
    # no raw envelope column (an IP, a port, a timestamp) may be a feature;
    # window COUNTS like win_dst_ports_10s are aggregate behaviour and are allowed.
    assert not (set(res["selected"]) & set(fv.ENVELOPE))
