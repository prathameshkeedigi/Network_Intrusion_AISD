"""Testable helpers for Phase 4 (no heavy training at import). Runs on Windows."""
import json, os, glob, time
import numpy as np
import pandas as pd
import features_v2 as fv

HERE = os.path.dirname(os.path.abspath(__file__))
NORMAL = "normal"


def load_dataset(data_dir=None):
    data_dir = data_dir or os.path.join(HERE, "data/flows")
    files = sorted(glob.glob(os.path.join(data_dir, "round*.csv")))
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def get_features(path=None):
    """The working feature set chosen in Phase 3; falls back to all FEATURES."""
    path = path or os.path.join(HERE, "results/selected_features.json")
    if os.path.exists(path):
        feats = json.load(open(path))["final_features"]
        return [f for f in feats if f in fv.FEATURES]
    return list(fv.FEATURES)


def split(df, train_rounds, test_round):
    tr = df[df["round"].isin(train_rounds)].reset_index(drop=True)
    te = df[df["round"] == test_round].reset_index(drop=True)
    return tr, te


def binary_metrics(y_true, y_pred, normal=NORMAL):
    """Treat any non-normal label as 'attack'. Returns attack recall and normal false-alarm rate."""
    yt = np.asarray(y_true); yp = np.asarray(y_pred)
    true_attack = yt != normal
    pred_attack = yp != normal
    n_attack = int(true_attack.sum())
    n_normal = int((~true_attack).sum())
    recall = float((pred_attack & true_attack).sum() / n_attack) if n_attack else float("nan")
    false_alarm = float((pred_attack & ~true_attack).sum() / n_normal) if n_normal else float("nan")
    return {"attack_recall": recall, "normal_false_alarm": false_alarm}


def time_single_flow(predict_fn, X_row, reps=200):
    """Average ms to predict ONE flow (how the live detector actually calls the model)."""
    predict_fn(X_row)
    s = time.perf_counter()
    for _ in range(reps):
        predict_fn(X_row)
    return (time.perf_counter() - s) / reps * 1000
