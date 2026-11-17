import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
from features import FEATURES, add_window_features, label_flows

D = "/home/prathamesh/cybersentinel/data/"

def load_round(n):
    df = add_window_features(pd.read_csv(D + f"round{n}_flows.csv"))
    df["label"] = label_flows(df, pd.read_csv(D + f"round{n}_attack_log.csv"))
    return df

r1, r2 = load_round(1), load_round(2)
nx = add_window_features(pd.read_csv(D + "normal_extra_flows.csv"))
nx["label"] = "normal"
cut = int(len(nx) * 0.7)                                   # time-based split, no shuffling
train = pd.concat([r1, nx.iloc[:cut]], ignore_index=True)  # round 1 + first 70% of extra normal
test  = pd.concat([r2, nx.iloc[cut:]], ignore_index=True)  # round 2 + last 30% (never seen in training)

print("TRAIN label counts:", train.label.value_counts().to_dict())
print("TEST  label counts:", test.label.value_counts().to_dict())

classes = sorted(train.label.unique())
to_id = {c: i for i, c in enumerate(classes)}
y_train, y_test = train.label.map(to_id), test.label.map(to_id)

model = XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1, eval_metric="mlogloss")
model.fit(train[FEATURES], y_train, sample_weight=compute_sample_weight("balanced", y_train))

pred = model.predict(test[FEATURES])
print("\n=== RESULTS ON ROUND 2 (unseen session) ===")
print(classification_report(y_test, pred, labels=list(range(len(classes))), target_names=classes, digits=3))
cm = pd.DataFrame(confusion_matrix(y_test, pred, labels=list(range(len(classes)))),
                  index=["true_" + c for c in classes], columns=["pred_" + c for c in classes])
print("Confusion matrix:\n", cm)

imp = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1])[:8]
print("\nTop features:")
for name, v in imp:
    print(f"  {name:32s} {v:.3f}")

model.save_model("/home/prathamesh/cybersentinel/model.json")
json.dump(classes, open("/home/prathamesh/cybersentinel/classes.json", "w"))
print("\nSaved model.json and classes.json")
