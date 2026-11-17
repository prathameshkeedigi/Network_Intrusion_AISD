"""Feature selection for CyberSentinel v2 (runs on Windows, no nfstream).
Three filter steps, argued in PIPELINE_V2.md 4.1:
  1. drop constant features (no information);
  2. of any pair with |correlation| >= threshold, drop one (repeated information);
  3. rank the rest by mutual information with the label.
The final choice of top-k (by F1) is done in run_phase3.py, which trains a quick model."""
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
import features_v2 as fv


def drop_constant(df, features):
    kept = [f for f in features if df[f].nunique(dropna=False) > 1]
    dropped = [f for f in features if f not in kept]
    return kept, dropped


def drop_correlated(df, features, thresh=0.95):
    """Greedy: walk the pairs; when two are >= thresh correlated, drop the lower-variance one."""
    corr = df[features].corr().abs()
    kept = list(features)
    dropped_pairs = []
    for i, a in enumerate(features):
        if a not in kept:
            continue
        for b in features[i + 1:]:
            if b not in kept:
                continue
            c = corr.loc[a, b]
            if pd.notna(c) and c >= thresh:
                drop = b if df[a].var() >= df[b].var() else a
                keep = a if drop == b else b
                kept.remove(drop)
                dropped_pairs.append({"kept": keep, "dropped": drop, "corr": round(float(c), 3)})
                if drop == a:
                    break
    return kept, dropped_pairs


def rank_mutual_info(df, features, label_col="label", seed=0):
    X = df[features].to_numpy(dtype=float)
    y = df[label_col].astype("category").cat.codes.to_numpy()
    mi = mutual_info_classif(X, y, random_state=seed)
    order = sorted(zip(features, mi), key=lambda t: (-t[1], t[0]))
    return [f for f, _ in order], {f: round(float(s), 5) for f, s in order}


def select(df, features=None, corr_thresh=0.95, label_col="label", seed=0):
    features = list(fv.FEATURES if features is None else features)
    kept0, const = drop_constant(df, features)
    kept1, corr_pairs = drop_correlated(df, kept0, corr_thresh)
    ranked, scores = rank_mutual_info(df, kept1, label_col, seed)
    return {
        "n_start": len(features),
        "dropped_constant": const,
        "dropped_correlated": corr_pairs,
        "selected": ranked,           # non-redundant features, best first
        "mi_scores": scores,
    }
