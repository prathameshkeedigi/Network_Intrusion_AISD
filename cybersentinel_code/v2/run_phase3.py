"""Phase 3: EDA + feature selection on the 4 recorded rounds. Runs on Windows.
Split kept for the whole project: TRAIN = rounds 3,4,5 ; TEST = round 6 (held out, not touched here).
Selection uses TRAIN only (no peeking at the test round)."""
import json, glob, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score
import features_v2 as fv
import select_features as sf

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
EDA = os.path.join(RES, "eda")
os.makedirs(EDA, exist_ok=True)

TRAIN_ROUNDS, TEST_ROUND = [3, 4, 5], 6

df = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(HERE, "data/flows/round*.csv")))],
               ignore_index=True)
train = df[df["round"].isin(TRAIN_ROUNDS)].reset_index(drop=True)
print(f"Total {len(df)} flows | train (rounds {TRAIN_ROUNDS}) {len(train)} | test (round {TEST_ROUND}) {len(df)-len(train)}")

# ---- 1. selection filters on TRAIN only ----
res = sf.select(train, seed=0)
print(f"\nDropped {len(res['dropped_constant'])} constant, "
      f"{len(res['dropped_correlated'])} correlated. {len(res['selected'])} features remain.")

# ---- 2. F1 vs number of features (top-k by mutual information), 3-fold by round ----
ranked = res["selected"]
Xtr, ytr, groups = train[ranked].to_numpy(float), train["label"].to_numpy(), train["round"].to_numpy()
gkf = GroupKFold(n_splits=len(TRAIN_ROUNDS))
ks = [k for k in [3, 5, 8, 10, 15, 20, 25, 30, len(ranked)] if k <= len(ranked)]
f1_by_k = {}
for k in ks:
    cols = [ranked.index(f) for f in ranked[:k]]
    scores = []
    for tr_i, va_i in gkf.split(Xtr, ytr, groups):
        m = RandomForestClassifier(n_estimators=60, class_weight="balanced", random_state=0, n_jobs=-1)
        m.fit(Xtr[tr_i][:, cols], ytr[tr_i])
        scores.append(f1_score(ytr[va_i], m.predict(Xtr[va_i][:, cols]), average="macro"))
    f1_by_k[k] = float(np.mean(scores))
    print(f"  k={k:3d}  macro-F1 (CV) = {f1_by_k[k]:.4f}")

best_f1 = max(f1_by_k.values())
minimal_k = min(k for k, v in f1_by_k.items() if v >= best_f1 - 0.005)   # smallest k within 0.5% of best
# Working set = ALL non-redundant features (robust). The curve is flat because every round shares
# the same attack settings, so a tiny k is optimistic; we keep the full 22 for robustness and still
# report that minimal_k features already reach the top F1 in-lab.
final_features = ranked
print(f"\nminimal_k (in-lab) = {minimal_k} at F1 {best_f1:.4f}  ->  working set kept = {len(final_features)} features (robust)")

# ---- 3. save selection result ----
out = {"train_rounds": TRAIN_ROUNDS, "test_round": TEST_ROUND, **res,
       "f1_by_k": f1_by_k, "minimal_k_in_lab": minimal_k, "working_k": len(final_features),
       "final_features": final_features}
with open(os.path.join(RES, "selected_features.json"), "w") as fh:
    json.dump(out, fh, indent=2)
print("Saved results/selected_features.json")

# ---- 4. EDA plots ----
plt.figure(figsize=(7, 4))
df.label.value_counts().plot.bar(color="#2471A3")
plt.title("Flows per class (all 4 rounds)"); plt.ylabel("flows"); plt.tight_layout()
plt.savefig(os.path.join(EDA, "class_counts.png"), dpi=130); plt.close()

top = ranked[:min(15, len(ranked))]
plt.figure(figsize=(8, 7))
corr = train[top].corr()
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.xticks(range(len(top)), top, rotation=90, fontsize=7); plt.yticks(range(len(top)), top, fontsize=7)
plt.colorbar(label="correlation"); plt.title("Correlation of top-15 features (train)"); plt.tight_layout()
plt.savefig(os.path.join(EDA, "correlation_top15.png"), dpi=130); plt.close()

plt.figure(figsize=(7, 6))
mi = res["mi_scores"]; names = ranked[:20][::-1]
plt.barh(names, [mi[n] for n in names], color="#1E8449")
plt.xlabel("mutual information with label"); plt.title("Top-20 features by information"); plt.tight_layout()
plt.savefig(os.path.join(EDA, "mutual_info_top20.png"), dpi=130); plt.close()

plt.figure(figsize=(7, 4))
plt.plot(list(f1_by_k), list(f1_by_k.values()), "o-", color="#C0392B")
plt.axvline(minimal_k, ls="--", color="grey"); plt.text(minimal_k, min(f1_by_k.values()), f" minimal k={minimal_k}", color="grey")
plt.xlabel("number of features (k)"); plt.ylabel("macro-F1 (3-fold CV)")
plt.title("F1 vs number of features"); plt.tight_layout()
plt.savefig(os.path.join(EDA, "f1_vs_k.png"), dpi=130); plt.close()

print("Saved 4 plots in results/eda/")
print("\nFinal features:", final_features)
