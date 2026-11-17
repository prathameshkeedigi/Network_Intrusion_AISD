"""Turns an NFStream flow table into the labelled training table. No nfstream import (testable on Windows)."""
import pandas as pd
import features_v2 as fv

ATTACKER = "10.10.10.1"


def make_table(flows, attack_log, round_no):
    """flows (NFStream rows, arrival order) -> round + envelope + 66 features + label."""
    t = fv.build_features(flows)
    t.insert(0, "round", round_no)
    t["label"] = fv.label_flows(t, attack_log, attacker=ATTACKER)
    return t[["round"] + fv.ENVELOPE + fv.FEATURES + ["label"]]


def attack_window_report(table, attack_log, margin_ms=fv.MARGIN_MS):
    """Sanity check per attack: how many attacker flows fall inside its time window.
    0 flows = clocks out of sync or the step did not run -> ok=False."""
    rows = []
    for a in attack_log.itertuples(index=False):
        inside = ((table.src_ip == ATTACKER)
                  & (table.bidirectional_first_seen_ms >= a.start_ms - margin_ms)
                  & (table.bidirectional_first_seen_ms <= a.end_ms + margin_ms))
        n = int(inside.sum())
        rows.append({"label": a.label, "duration_s": (a.end_ms - a.start_ms) / 1000,
                     "attacker_flows": n, "ok": n > 0})
    return pd.DataFrame(rows)
