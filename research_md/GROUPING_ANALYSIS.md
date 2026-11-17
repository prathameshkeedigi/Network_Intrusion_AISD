# IDS Research Papers — Grouping, Reasoning, and How to Think About Them

**Team 10 · CyberSentinel AI · prepared 17 Nov 2026**

This document explains **how the 15 papers (and sir's literature-survey doc) were grouped, and why**, so our team can split the work and each person implements a different methodology, then we compare. It is written to be honest: where I am sure, I say so; where a paper could sit in two groups, I say which and why I chose one.

> **How the grouping was actually done (so you can trust it).** Every PDF was converted to Markdown and scanned by a script that recorded, for each paper, the **model/dataset/technique keywords that truly appear in its text** plus an **abstract snippet** (`_catalog.md`). I grouped by each paper's **primary contribution from its abstract**, *not* by keyword counts — because almost every paper name-drops CNN/LSTM/Transformer/XGBoost in its related-work section, so counting keywords would put everything in one blob. The distinguishing question for each paper was: **"what is the ONE thing this paper is actually proposing?"**

---

## 1. The mindset this project needs (read this first)

Sir gave us survey papers and asked us to "try different methodologies". The trap is to treat this as a shopping list of models and chase the highest accuracy number. That is "answer-generator" thinking. For an intrusion-detection project it is the wrong instinct, for reasons that come from **both** networking and ML:

**From the networking side:**
- **A model is only as honest as its data.** Our own v1/v2 already showed ~100% on lab data, *because the lab is easy* — same attack tools, same settings. A paper reporting 99.9% on CIC-IDS2017 is in the same trap. So when reading these papers, the first question is **"what data, and is the split honest?"**, not "what accuracy?".
- **Flows are not packets, and features decide everything.** Most of these papers run on pre-made flow datasets (NSL-KDD, UNSW-NB15, CIC-IDS2017) where the features were already extracted by someone else's tool. We extract our own with NFStream. A method that wins on NSL-KDD may not transfer, because the *features* differ. Verified earlier (Engelen 2021; arXiv 2412.14021): the flow tool changes the result.
- **Class imbalance is a networking fact, not a nuisance.** Real traffic is mostly normal; attacks are rare and bursty. Our own data is 86% attack flows only because a scan makes 1,000 flows — which is itself a distortion. Many papers here are really about *imbalance*; that is the honest hard problem.

**From the ML/DL side:**
- **Match the model to the data's structure.** Tabular flow features → trees (XGBoost/RF) are usually strongest and fastest. Sequences of packets/flows over time → RNN/LSTM. Relationships *between* features → attention/Transformers. Don't use a Transformer because it is fashionable; use it only if the data has the structure it exploits.
- **Deep learning is not automatically better.** Several papers here (G1) exist *precisely* to show ML-vs-DL is a real contest; on tabular IDS data, gradient-boosted trees very often beat neural nets while being 100× faster. Our v2 measured this: XGBoost 0.67 ms/flow vs Random Forest 59 ms; both at ~F1 1.0.
- **A number without a cost is meaningless.** Every method must report **accuracy AND latency AND false-alarm rate**. An IDS that is 0.1% more accurate but 100× slower, or that cries wolf on normal traffic, is worse. This is the axis our comparison must add that most papers underplay.
- **Interpretability is part of correctness here.** A security analyst must know *why* an alert fired. That is why XAI/SHAP (G5) is its own track, not an afterthought.

**So our comparative study should vary, for each method, these axes:** dataset honesty · feature set · imbalance handling · model family · speed/latency · false-alarm rate · explainability. That is the real "methodology", and it is what will impress sir more than another 99% number.

---

## 2. The groups (with reasoning)

Seven folders. **G0 is reference reading; G1–G6 are implementable methodology families.** Each paper is placed by its *primary* contribution; secondary themes are noted so nothing is lost.

### G0 — Surveys & Reviews *(read first; do not implement)*
| Paper | Why here |
|---|---|
| 05_Wu_2024_J_Imaging_IDS_Survey | Explicitly a survey: reviews the common datasets and 7 DL model families (autoencoder, DBN, DNN, CNN, RNN, GAN, Transformer). |
| 14_Ali_2024_Front_Comput_Sci_Review | A review of datasets, features and model families across the field. |
**Reasoning:** neither proposes a method — they map the landscape. Read these two **before** picking a track, so everyone shares the same vocabulary and knows which datasets/models exist. They are our shortcut to "what has been tried".

### G1 — Comparative Benchmarks *(the template for OUR deliverable)*
| Paper | Primary contribution |
|---|---|
| 01_Elsayed_2024_DL_NIDS_Comparative | Runs 6 DL models head-to-head (DNN, CNN, RNN, LSTM, GRU, CNN-LSTM) on NSL-KDD, binary + multiclass. |
| 06_Ali_2025_DL_vs_ML_IDS | Compares DL (MLP, CNN, LSTM) **against** classical ML (LR, NB, RF, KNN, DT), with SMOTE for imbalance. |
**Reasoning:** these papers' *contribution is the comparison itself* — exactly what our team must produce. Use them as the **method template**: same data, same split, same metrics across all models. Copy their table structure; add the speed/false-alarm axes they skip.

### G2 — Sequence & Attention Deep Architectures
| Paper | Primary contribution |
|---|---|
| 04_Berhanu_2025_RNN_NIDS | An optimized **LSTM-RNN** to capture temporal dependencies in traffic sequences. |
| 03_Zhu_2025_TransNeSt | Hybrid **ResNeSt (split-attention) + Transformer** for multi-scale + long-range temporal features. |
| 11_Zaim_2025_FPE_Transformer | A **Transformer** with feature positional encoding (models relationships between features). |
**Reasoning:** all three propose *deep architectures that model dependencies* — either over time (recurrence) or across features (self-attention). This is the "modern architecture" track. Note the honest caveat: these shine when input has real sequential/relational structure; on single completed-flow feature vectors (like ours) that advantage shrinks. Worth testing, not assuming.

### G3 — Hybrid & Ensemble (ML + DL combined)
| Paper | Primary contribution |
|---|---|
| 02_Almuhanna_2025_Front_AI | Hybrid system stacking **XGBoost + RF + GNN + LSTM + Autoencoder**. |
| 08_Pavithra_2024_Unbalanced_Traffic | Hybrid **XGBoost + LSTM + Mini-VGGNet + AlexNet**, RF for feature importance, oversampling. |
**Reasoning:** the contribution is *combining heterogeneous learners* into one detector, hoping each covers the others' blind spots. Distinct from the single-architecture papers in G2. Caveat for us: more models = slower and harder to explain, which fights our "live and fast" requirement — a good thing to measure, not take on faith.

### G4 — Feature Engineering & Class-Imbalance Pipelines *(closest to our current XGBoost work)*
| Paper | Primary contribution |
|---|---|
| 12_Talukder_2024_J_Big_Data | Random Oversampling + **stacking feature embedding (clustering)** + PCA for large imbalanced data. |
| 13_Farhan_2025_Sci_Rep | Feed-forward **DNN + Extra-Tree-Classifier feature selection**. |
| 09_Mohammad_2024_Systems | **Data augmentation** across 4 datasets to fix imbalance for DL. |
**Reasoning:** here the model is almost secondary — the contribution is the **data pipeline**: oversampling/augmentation, feature selection/embedding, dimensionality reduction. This is the *direct extension of what we already do* (our 66→22 feature selection, class weights). The natural "improve the existing pipeline" track.

### G5 — Explainable & Multi-Stage IDS (XAI / SHAP)
| Paper | Primary contribution |
|---|---|
| 10_Mohale_2025_XAI | ML IDS made interpretable with **XAI/SHAP** on UNSW-NB15. |
| 15_Mahmoud_2025_XI2S | **Two-stage** IDS with **SHAP-based** explanations (coarse filter → fine classifier). |
**Reasoning:** the contribution is *transparency and staged detection*, not a new classifier. This is a **cross-cutting layer** — it can wrap any model from G1–G4. It directly answers a weakness our guide cares about (knowing *why* an alert fired; our next-steps already list SHAP).

### G6 — Deployment / System Architecture
| Paper | Primary contribution |
|---|---|
| 07_Alromaihi_2025_ML_IDS_Architecture | A **centralized proxy-server architecture** that aggregates traffic from many interfaces so one attacker hitting several servers is seen as one actor. |
**Reasoning:** this paper is about *where the IDS sits and how traffic reaches it*, not the model. A singleton, but genuinely different and relevant to our live-deployment angle (and to the "know the attacker IP across sources" idea we already demo with the innocent user). Keep separate so it isn't mistaken for a modeling paper.

---

## 3. Suggested team split (4 members, different methodologies)

Everyone reads **G0** (surveys) and uses **G1**'s comparison structure. Then one implementable track each, all compared against our existing **XGBoost v2** baseline on **our own NFStream flow data**:

| Member | Track | Builds | Why this is a distinct methodology |
|---|---|---|---|
| 1 | **G4 — Feature eng. + imbalance** | Oversampling (SMOTE/RO) + feature selection/embedding + PCA, with tree models | Extends our current pipeline; tabular, fast, the honest baseline to beat |
| 2 | **G2 — Sequence/attention DL** | An LSTM **or** a small Transformer on flow features | Tests whether deep sequence/attention models beat trees on OUR data |
| 3 | **G3 — Hybrid/ensemble** | Stack XGBoost + an LSTM/autoencoder | Tests whether combining learners helps, and at what speed cost |
| 4 | **G5 — Explainable (XAI/SHAP)** | Wrap the best model with SHAP + a 2-stage filter | Adds the "why" an analyst needs; answers interpretability |

G6 (architecture) and the surveys are shared references, not a person's build. **Our comparison table must report, for every track: macro-F1, per-class recall, false-alarm rate on normal, single-flow latency, and model size** — the same honest axes from our v2 work, so the four methodologies are judged on the same ruler.

---

## 4. Honest caveats
- **I grouped from abstracts, not full reads.** The placement is sound for the primary contribution, but a paper's details may add secondary methods (noted above). Read the full MD of your assigned track before implementing.
- **Most papers use public datasets (NSL-KDD, UNSW-NB15, CIC-IDS2017).** Their headline accuracies are **not** directly comparable to ours, because our features and traffic are our own. Treat their *methods* as transferable, their *numbers* as not.
- **"Try different methodologies" ≠ "find the highest number".** The value we add is the fair, cost-aware comparison on our own live-captured data — that is what the groups are organised to enable.

## 5. Where everything is
```
research_md/
  IDS_ML_DL_Literature_Survey.md     ← sir's document, converted
  GROUPING_ANALYSIS.md               ← this file
  _catalog.md                        ← auto-extracted keywords + abstracts (grouping evidence)
  source_pdfs/                       ← the 15 original PDFs
  (the original .docx is in AISD_Project/docs/)
  G0_Surveys_Reviews/                (05, 14)
  G1_Comparative_Benchmarks/         (01, 06)
  G2_Sequence_Attention_DL/          (03, 04, 11)
  G3_Hybrid_Ensemble/                (02, 08)
  G4_FeatureEng_Imbalance/           (09, 12, 13)
  G5_Explainable_XAI/                (10, 15)
  G6_Deployment_Architecture/        (07)
```
