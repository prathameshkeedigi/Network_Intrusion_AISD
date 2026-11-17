"""Tests for train_lib.py, written before the Phase 4 runner."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import train_lib as tl
import features_v2 as fv


def test_split_has_no_overlap():
    df = pd.DataFrame({"round": [3, 3, 4, 5, 6], "x": range(5)})
    tr, te = tl.split(df, [3, 4, 5], 6)
    assert set(tr["round"]) == {3, 4, 5} and set(te["round"]) == {6}
    assert len(tr) == 4 and len(te) == 1          # 5 rows: 4 in train (two round-3s, 4, 5), 1 in test
    assert set(tr["round"]).isdisjoint(set(te["round"]))   # train and test rounds never overlap

def test_split_counts():
    df = pd.DataFrame({"round": [3, 4, 5, 6, 6], "x": range(5)})
    tr, te = tl.split(df, [3, 4, 5], 6)
    assert len(tr) == 3 and len(te) == 2


def test_binary_metrics_perfect():
    y = ["normal", "scan", "synflood", "normal"]
    m = tl.binary_metrics(y, y)
    assert m["attack_recall"] == 1.0 and m["normal_false_alarm"] == 0.0


def test_binary_metrics_counts():
    yt = ["normal", "normal", "scan", "scan"]
    yp = ["attack", "normal", "scan", "normal"]   # 1 false alarm of 2 normals; 1 of 2 attacks caught
    m = tl.binary_metrics(yt, yp)
    assert m["attack_recall"] == 0.5 and m["normal_false_alarm"] == 0.5


def test_get_features_subset_of_FEATURES():
    feats = tl.get_features()
    assert len(feats) >= 1 and set(feats).issubset(set(fv.FEATURES))
    assert not (set(feats) & set(fv.ENVELOPE))


def test_time_single_flow_runs():
    ms = tl.time_single_flow(lambda r: r.sum(), np.zeros((1, 5)), reps=10)
    assert ms >= 0
