"""Phase 4: train and compare models on the v2 dataset. Runs on Windows.
TRAIN = rounds 3,4,5 ; TEST = round 6 (held out). Features = Phase 3 working set.
Models: Logistic Regression, Random Forest, XGBoost, MLP (separate, supervised),
Isolation Forest (unsupervised, trained on normal only), and one soft-voting ensemble.
Also: unknown-attack test, single-flow speed, confusion matrix, best model saved."""
import json, os, pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, recall_score
from xgboost import XGBClassifier
import train_lib as tl

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(os.path.join(HERE, "models"), exist_ok=True)
TRAIN_ROUNDS, TEST_ROUND = [3, 4, 5], 6
SEED = 0

df = tl.load_dataset()
feats = tl.get_features()
tr, te = tl.split(df, TRAIN_ROUNDS, TEST_ROUND)
Xtr, ytr = tr[feats].to_numpy(float), tr["label"].to_numpy()
Xte, yte = te[feats].to_numpy(float), te["label"].to_numpy()
classes = sorted(df["label"].unique())
print(f"{len(feats)} features | train {len(tr)} (rounds {TRAIN_ROUNDS}) | test {len(te)} (round {TEST_ROUND})")
print("classes:", classes)


def supervised_models():
    return {
        "LogisticRegression": make_pipeline(StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight="balanced")),
        "RandomForest": RandomForestClassifier(n_estimators=200, class_weight="balanced",
            random_state=SEED, n_jobs=-1),
        "XGBoost": XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1,
            tree_method="hist", n_jobs=1, verbosity=0),
        "MLP": make_pipeline(StandardScaler(),
            MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=400, random_state=SEED)),
    }


def eval_supervised(name, model, needs_int):
    # XGBoost wants integer labels
    enc = {c: i for i, c in enumerate(classes)}; dec = {i: c for c, i in enc.items()}
    ytr_f = np.array([enc[c] for c in ytr]) if needs_int else ytr
    model.fit(Xtr, ytr_f)
    raw = model.predict(Xte)
    yp = np.array([dec[i] for i in raw]) if needs_int else raw
    proba = model.predict_proba(Xte)
    norm_i = list(model.classes_).index(enc["normal"] if needs_int else "normal")
    attack_score = 1 - proba[:, norm_i]
    auc = roc_auc_score((yte != "normal").astype(int), attack_score)
    row = {"model": name, "type": "multiclass",
           "accuracy": round(accuracy_score(yte, yp), 4),
           "macro_f1": round(f1_score(yte, yp, average="macro"), 4),
           **{f"recall_{c}": round(recall_score(yte == c, yp == c, zero_division=0), 3) for c in classes},
           **{k: round(v, 4) for k, v in tl.binary_metrics(yte, yp).items()},
           "roc_auc": round(float(auc), 4),
           "predict_ms": round(tl.time_single_flow(
               (lambda r: model.predict(r)), Xte[:1]), 3),
           "size_kb": round(len(pickle.dumps(model)) / 1024, 1)}
    return row, yp


rows, preds = [], {}
for name, model in supervised_models().items():
    row, yp = eval_supervised(name, model, needs_int=(name == "XGBoost"))
    rows.append(row); preds[name] = (model, yp)
    print(f"  {name:20s} acc {row['accuracy']} macroF1 {row['macro_f1']} "
          f"attackRecall {row['attack_recall']} falseAlarm {row['normal_false_alarm']} {row['predict_ms']}ms")

# ---- soft-voting ensemble of the 4 supervised (string labels; skip XGBoost's int quirk by refitting) ----
vote = VotingClassifier(estimators=[
    ("lr", make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))),
    ("rf", RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=SEED, n_jobs=-1)),
    ("mlp", make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=400, random_state=SEED))),
], voting="soft", n_jobs=-1)
vote.fit(Xtr, ytr); yv = vote.predict(Xte)
rows.append({"model": "VotingEnsemble", "type": "ensemble",
             "accuracy": round(accuracy_score(yte, yv), 4),
             "macro_f1": round(f1_score(yte, yv, average="macro"), 4),
             **{f"recall_{c}": round(recall_score(yte == c, yv == c, zero_division=0), 3) for c in classes},
             **{k: round(v, 4) for k, v in tl.binary_metrics(yte, yv).items()},
             "roc_auc": round(float(roc_auc_score((yte != "normal").astype(int), 1 - vote.predict_proba(Xte)[:, list(vote.classes_).index("normal")])), 4),
             "predict_ms": round(tl.time_single_flow(lambda r: vote.predict(r), Xte[:1]), 3),
             "size_kb": round(len(pickle.dumps(vote)) / 1024, 1)})
print(f"  {'VotingEnsemble':20s} acc {rows[-1]['accuracy']} macroF1 {rows[-1]['macro_f1']}")

# ---- Isolation Forest: unsupervised, trained on NORMAL training flows only ----
iso = IsolationForest(n_estimators=200, contamination=0.02, random_state=SEED)
iso.fit(Xtr[ytr == "normal"])
iso_pred = np.where(iso.predict(Xte) == -1, "attack", "normal")
iso_bin = tl.binary_metrics(yte, iso_pred)
iso_auc = roc_auc_score((yte != "normal").astype(int), -iso.score_samples(Xte))
rows.append({"model": "IsolationForest", "type": "anomaly", "accuracy": "", "macro_f1": "",
             **{f"recall_{c}": "" for c in classes},
             **{k: round(v, 4) for k, v in iso_bin.items()}, "roc_auc": round(float(iso_auc), 4),
             "predict_ms": round(tl.time_single_flow(lambda r: iso.predict(r), Xte[:1]), 3),
             "size_kb": round(len(pickle.dumps(iso)) / 1024, 1)})
print(f"  {'IsolationForest':20s} (anomaly) attackRecall {iso_bin['attack_recall']} falseAlarm {iso_bin['normal_false_alarm']}")

comp = pd.DataFrame(rows)
comp.to_csv(os.path.join(RES, "model_comparison.csv"), index=False)
print("\nSaved results/model_comparison.csv")

# ---- unknown-attack test: drop synflood from training, can models still flag it? ----
print("\nUnknown-attack test (train WITHOUT synflood, check synflood flows in test):")
mask = ytr != "synflood"
unk = {}
for name, mk in [("RandomForest", RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=SEED, n_jobs=-1)),
                 ("XGBoost", None)]:
    if name == "XGBoost":
        enc = {c: i for i, c in enumerate([c for c in classes if c != "synflood"])}
        dec = {i: c for c, i in enc.items()}
        m = XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1, tree_method="hist", n_jobs=1, verbosity=0)
        m.fit(Xtr[mask], np.array([enc[c] for c in ytr[mask]]))
        yp = np.array([dec[i] for i in m.predict(Xte)])
    else:
        mk.fit(Xtr[mask], ytr[mask]); yp = mk.predict(Xte)
    syn = yte == "synflood"
    flagged = float((yp[syn] != "normal").mean())
    unk[name] = round(flagged, 3)
    print(f"  {name}: {flagged*100:.1f}% of unseen synflood flows still flagged as SOME attack")
json.dump(unk, open(os.path.join(RES, "unknown_attack_test.json"), "w"), indent=2)

# ---- pick the model to SHIP for live detection ----
# Several models tie near macro-F1 = 1.0 (the lab is easy). For a LIVE IDS we need a model that is
# both fast (< 5 ms/flow, so Random Forest at ~58 ms is out) and explainable. Among the tied-best
# fast models we prefer, in order: XGBoost (fast + explainable + Round-1 continuity), then LogReg,
# then MLP (black box), then the ensemble. This is a documented choice, not an automatic tiebreak.
sup = [r for r in rows if r["type"] in ("multiclass", "ensemble")]
top_f1 = max(r["macro_f1"] for r in sup)
PREF = ["XGBoost", "LogisticRegression", "MLP", "VotingEnsemble", "RandomForest"]
fast_tied = [r for r in sup if r["macro_f1"] >= top_f1 - 0.002 and r["predict_ms"] < 5]
best = min(fast_tied, key=lambda r: PREF.index(r["model"]))
print(f"\nShipped model: {best['model']} (macro-F1 {best['macro_f1']}, {best['predict_ms']} ms/flow) "
      f"— chosen for speed + explainability among the tied-best")

# save best model + confusion matrix
best_name = best["model"]
if best_name == "XGBoost":
    bm, yp = preds["XGBoost"]
    bm.save_model(os.path.join(HERE, "models/best_xgb.json"))
else:
    bm = preds[best_name][0] if best_name in preds else vote
    yp = preds[best_name][1] if best_name in preds else yv
    pickle.dump(bm, open(os.path.join(HERE, "models/best.pkl"), "wb"))
json.dump({"best": best_name, "features": feats, "classes": classes},
          open(os.path.join(HERE, "models/best_meta.json"), "w"), indent=2)

cm = confusion_matrix(yte, yp, labels=classes)
plt.figure(figsize=(6, 5))
plt.imshow(cm, cmap="Blues")
for i in range(len(classes)):
    for j in range(len(classes)):
        plt.text(j, i, cm[i, j], ha="center", va="center",
                 color="white" if cm[i, j] > cm.max() / 2 else "black")
plt.xticks(range(len(classes)), classes, rotation=45); plt.yticks(range(len(classes)), classes)
plt.xlabel("predicted"); plt.ylabel("true"); plt.title(f"Confusion matrix: {best_name} (test round 6)")
plt.colorbar(); plt.tight_layout(); plt.savefig(os.path.join(RES, "confusion_best.png"), dpi=130); plt.close()
print("Saved results/confusion_best.png and models/")
