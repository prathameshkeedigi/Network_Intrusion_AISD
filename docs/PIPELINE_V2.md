# CyberSentinel AI: Pipeline v2 (answers to sir's Round 1 remarks)

**Team 10** · Prepared 14 Nov 2026 · Status: **Phases 1–5 of 6 done and verified** (see section 6). Only Phase 6 (documentation + demo wrap-up) remains.

Every claim below is marked as one of:
- **[MEASURED]**: we ran it ourselves.
- **[DOCS]**: checked in the official documentation (links at the end).
- **[PLAN]**: still to be done and tested.

---

## 1. Sir's remarks and where Pipeline v2 answers them

| # | Sir's remark | Short answer | Section |
|---|---|---|---|
| R1 | Use the ~81 CICFlowMeter features, with proper FE, FS and EDA | Use NFStream's full statistical set (58 numbers) + 8 engineered features ≈ **66 features**, then EDA and feature selection. Also save every capture as a `.pcap`, so CICFlowMeter can be run on the same traffic for comparison. | 4.1 |
| R2 | Build a separate Wireshark version | Wireshark at three points: **live view** (working), **recording** every round as `.pcap` with dumpcap (Wireshark's capture engine), and a **detector that reads any Wireshark `.pcap`** | 4.2 |
| (i) | What is the window size? | Three windows: a flow ends after **5 s idle** or **30 s active** (plus at once on RST/FIN, new); behaviour window **10 s** per source IP. Justified with a sensitivity test (5/10/30/60 s). | 4.3 |
| (ii) | Try different ML models | **5 models** compared on the same split: Logistic Regression, Random Forest, XGBoost, MLP, Isolation Forest. Measured on quality **and** speed. | 4.4 |
| (iii) | The attacker IP must be known | Already in every alert. v2 adds an **innocent client on another IP (10.10.10.3)** running at the same time, so the system must pick the attacker out of several sources. | 4.5 |
| (iv) | At least 10,000 flows | **6 recording rounds**, each with varied attack settings → expected ≥ 12,000 flows | 4.6 |
| Live + fast | Prediction must be live and very fast | NumPy instead of pandas (**4× faster [MEASURED]**). RST/FIN plugin ends scan flows at once. Every alert prints its own prediction time and delay. | 4.7 |

---

## 2. Pipeline v2 diagram

```
                 ┌───────────────────────────── labnet (private, inside VirtualBox) ─────────────────────────────┐
 ATTACKER VM     │  10.10.10.1 = ATTACKER   nmap / hydra / hping3 (varied settings each round)                   │
 (one VM,        │  10.10.10.3 = INNOCENT   curl + SSH logins (normal user, runs DURING attacks too)   ← new     │
  two IPs)       └───────────────────────────────────────────────┬───────────────────────────────────────────────┘
                                                                 ▼
                                             MINT VM (victim) 10.10.10.2, interface enp0s8
                                                                 │
         ┌───────────────────────────────────┬───────────────────┴──────────────────────┐
         ▼                                   ▼                                          ▼
 (A) LIVE HUMAN VIEW  ✅ working     (B) RECORD (training)  ← new             (C) LIVE MACHINE VIEW
 dumpcap → SSH → Windows Wireshark   dumpcap → roundN.pcap                   NFStream on enp0s8
                                     + attack time log                        + EndOnRstFin plugin  ← new
                                             │                                         │
                                             ▼                                         │
                                     NFStream reads roundN.pcap                        │
                                     (same settings + same plugin as C)                │
                                             │                                         │
                                             ▼                                         ▼
                          ┌──────────────── features_v2.py (ONE shared file) ────────────────┐
                          │ 58 NFStream statistics + 3 rates/ratios + 5 window features (10 s) │
                          │ IP, port and time are NEVER features (kept in a separate "envelope") │
                          └───────────────┬──────────────────────────────────┬───────────────┘
                                          ▼                                  ▼
                     labels (attacker IP + attack time log)        one NumPy row per flow
                                          ▼                                  ▼
                 EDA → feature selection → train 5 models          best model, loaded into RAM once
                 rounds 1–4 train, rounds 5–6 test                           │ prediction ms measured
                 comparison table (quality + speed)  ───────────────►        ▼
                                                                   ALERT: time | ATTACKER IP | victim IP:port |
                                                                          attack | confidence | predict ms | delay s
                                                                             │
                                                                             ▼
                                                     incident summary per attacker IP + alerts.csv
                                                     (D) Same detector can also read any .pcap from Wireshark
```

**What is new compared with Round 1:** the innocent IP, `.pcap` recording, the RST/FIN plugin, 66 features instead of 22, 5 models instead of 1, NumPy instead of pandas, timing in alerts, an incident summary, and the detector reading `.pcap` files.

---

## 3. What Round 1 already did (unchanged)
- Labnet lab with attacker `10.10.10.1` and victim `10.10.10.2`; NFStream with idle 5 s / active 30 s; 22 features; XGBoost; 99.8% on round 2 (2,327 / 2,331) **[MEASURED]**.
- Alerts already print the attacker's IP (`detect.py`).
- Live packet view in Windows Wireshark **[MEASURED, 13 Nov]**.

---

## 4. Each remark in detail

### 4.1 R1: About 81 features, FE, FS, EDA

**Why not use CICFlowMeter directly?**
1. It is a separate Java program. If training used CICFlowMeter but live detection used something else, the same flow would get **different numbers**. The model would then be judged on inputs it never saw. Keeping **one** tool for training and live detection avoids this.
2. Researchers found bugs in CICFlowMeter's flow handling (Engelen et al., 2021). Those bugs produced wrong features and wrong labels in CIC-IDS2017.
3. NFStream already gives the same kinds of numbers **[DOCS]**.

**NFStream's full statistical set (with `statistical_analysis=True`) [DOCS]:**

| Group | Features | Count |
|---|---|---|
| Protocol | `protocol` | 1 |
| Duration | bidirectional / src2dst / dst2src `_duration_ms` | 3 |
| Packets and bytes | `bidirectional_`, `src2dst_`, `dst2src_` × `packets`, `bytes` | 6 |
| Packet size | 3 directions × min / mean / stddev / max `_ps` | 12 |
| Time gap between packets | 3 directions × min / mean / stddev / max `_piat_ms` | 12 |
| TCP flags | 3 directions × SYN, CWR, ECE, URG, ACK, PSH, RST, FIN | 24 |
| **Total from NFStream** | | **58** |

**Engineered features (FE) [PLAN]:**

| Feature | Formula | Why |
|---|---|---|
| `bytes_per_s` | bidirectional_bytes / duration | Same as CIC "Flow Bytes/s"; floods are high |
| `packets_per_s` | bidirectional_packets / duration | Same as CIC "Flow Packets/s" |
| `down_up_ratio` | dst2src_bytes / (src2dst_bytes + 1) | Scans get almost no reply data |
| `win_flows_10s` | flows from this source in the last 10 s | Existing; floods and scans are high |
| `win_dst_ports_10s` | different ports from this source in the last 10 s | Existing; best scan signal |
| `win_dst_ips_10s` | different victims from this source in the last 10 s | Catches scanning many hosts |
| `win_rst_ratio_10s` | share of this source's flows that ended with RST | Scans hit closed ports and get RST |
| `win_half_open_10s` | flows in the last 10 s where the sender sent SYN but never ACKed | SYN flood and SYN-scan signal (a normal client always ACKs) |

Total = **66 features** **[MEASURED]**: on 14 Nov, `check_nfstream.py` in Mint confirmed that all 58 NFStream names exist (NFStream 6.6.0 gives 77 columns in total, including IPs, ports, times and app names, which are not used). It also built 205 × 66 features with 0 NaN or infinite values.

**CICFlowMeter features NFStream does not have** (stated openly): Active/Idle statistics, header lengths, initial TCP window size, bulk rates, sub-flow counts. If sir asks, we can run CICFlowMeter **offline on the saved `.pcap` files** and show a comparison table. The live system stays on NFStream.

**EDA plan [PLAN]:**
- Class counts per round.
- Box plots of key features per class.
- A correlation heat map.
- Features that are constant or always zero.
- Missing or infinite values (for example, dividing by a duration of 0).

**Feature selection plan [PLAN], argued step by step:**
1. Drop features that are constant (no information).
2. Of any pair with correlation > 0.95, drop one (repeated information).
3. Rank the rest by **mutual information** and by **permutation importance** on the test rounds.
4. Train again on the top-k (k = 10, 20, 30, all) and plot macro-F1 against k. Keep the smallest k whose F1 is within 0.5% of the best. A smaller k gives faster prediction and is easier to explain.

---

### 4.2 R2: The Wireshark version

**Wireshark is used in three places:**
1. **Live view:** `dumpcap → SSH → Windows Wireshark` **[MEASURED: works]**. A person watches the attack packets as they happen, for example with the filter `ip.src == 10.10.10.1`.
2. **Recording:** each data round is saved as `roundN.pcap` by `dumpcap`, which is Wireshark's own capture program. These files are the **raw evidence**. Anyone can open them in Wireshark, and features can be extracted again later with any window size, without recapturing.
3. **Detector on Wireshark files:** NFStream accepts a `.pcap` file as `source` **[DOCS]**. So `detect_v2.py round5.pcap` runs the same detector on any capture made in Wireshark.

**Why labnet and not loopback (the teammate's plan)?** Both are legal. On loopback, though, the attacker and the victim are **both `127.0.0.1`**, so remark (iii) can never be shown. Loopback packets also never cross a network link, so their timing isn't realistic. Labnet has a real separate attacker IP and a real link.

---

### 4.3 (i) The window size

| Window | Value | What it means | Where |
|---|---|---|---|
| Flow idle timeout | **5 s** | No packet for 5 s → the conversation is finished | `NFStreamer(idle_timeout=5)` |
| Flow active timeout | **30 s** | A long conversation is cut every 30 s, so long attacks are still judged | `NFStreamer(active_timeout=30)` |
| End on RST / FIN (new) | at once | A refused (RST) or closed (FIN from both sides) connection is finished at once | plugin, 4.7 |
| Behaviour window | **10 s** | For each source IP: flows, ports, victims, RST share in the last 10 s | `features_v2.py` |

**Answer to "Round 1 trained on ~2,000 flows":** the 2,000 is the **number of flows**, not a window. Each flow is one conversation (same IPs, ports and protocol), and it ends by the rules above. The window decides **when a flow ends** and **how far back** we look at a source's behaviour.

**Why these values (argued, then tested):**
- 5 s idle: normal web and SSH requests in our lab finish well within 5 s. A shorter value cuts real conversations in two. A longer value delays every alert. NFStream's default is 120 s **[DOCS]**, which is far too slow for live alerts.
- 10 s behaviour window: a scan of 1,000 ports finishes within seconds, so 10 s sees most of it. A long window also mixes in older, unrelated traffic.
- **Sensitivity test [PLAN]:** because every round is saved as `.pcap`, we extract features again with idle = 2 / 5 / 10 / 30 s and behaviour window = 5 / 10 / 30 / 60 s, then report macro-F1 and average detection delay for each. This turns "we chose 5 s" into "**we tested and 5 s gave the best balance**".

---

### 4.4 (ii) Multiple models

| Model | Type | Why include it |
|---|---|---|
| Logistic Regression | Linear, simple | Baseline: shows how hard the problem really is |
| Random Forest | Many decision trees | Strong standard IDS model, easy to explain |
| XGBoost | Boosted trees | Round 1 model |
| MLP | Small neural network | Represents deep learning |
| Isolation Forest | **Unsupervised**, trained on normal traffic only | Can flag attacks it was **never shown**; an honest test of unknown attacks |

**Same rules for all:** same features, same split, same class weights.

**Reported for each model:** accuracy, **macro-F1**, recall per attack class, false-alarm rate on normal traffic, ROC-AUC, confusion matrix, **single-flow prediction time**, and model file size.

**Extra test for unknown attacks [PLAN]:** train without one attack type (for example SYN flood) and check whether the models still raise *some* alert on it.

**Single-flow prediction time [MEASURED on the Windows host, 60 synthetic features, 10,000 training rows, one flow at a time, 300 repeats]:**

| Model / method | ms per flow |
|---|---|
| XGBoost, pandas row (as in Round 1 `detect.py`) | 2.79 |
| XGBoost, NumPy row | 0.69 |
| XGBoost, NumPy `inplace_predict` | **0.58** |
| Random Forest (100 trees), NumPy | 9.35 |
| Logistic Regression, NumPy | 0.12 |
| MLP (64-32), NumPy | 0.12 |
| Isolation Forest, NumPy | 10.82 |
| XGBoost, **batch of 10,000 ÷ 10,000** | 0.011 |

What this shows:
1. Switching from pandas to NumPy makes prediction **4× faster**.
2. The very small "per flow" numbers (0.011 ms here, 0.003 ms in the teammate's file) come from **dividing a batch**. A live detector receives flows one at a time, so the honest number is the single-row one.
3. The VM is slower than the host: Round 1 measured about 60 ms per flow inside the VM. The real VM numbers will be measured again in v2 and reported.

---

### 4.5 (iii) The attacker IP must be known

**Already done:** every alert prints `from <src_ip>`, and the IP is **not** a model feature, so the model learns behaviour, not addresses.

**Problem with Round 1:** the attacker VM was the **only** client, so "the attacker IP" was trivially 10.10.10.1. Sir's point is only proven when the system has to **pick** the attacker out of several sources.

**v2 fix [PLAN]:**
- The attacker VM gets a second, temporary address `10.10.10.3` (the "innocent user"), added with `sudo ip addr add 10.10.10.3/24 dev enp0s8`. It disappears on reboot.
- Normal traffic is sent from `.3` (`curl --interface 10.10.10.3`, `ssh -b 10.10.10.3`) **during** the attacks, not only between them.
- **Pass test:** alerts name only `10.10.10.1`; flows from `.3` stay "normal" (false-alarm rate is reported).
- Labelling stays "attack only if from `.1` inside an attack's time window", so `.3` traffic is always labelled normal. This also fixes a weakness in Round 1, where normal traffic and attacks never overlapped in time.
- **Incident summary** printed on Ctrl+C and saved to `incidents.csv`, one row per attacker IP: first seen, last seen, attack types, number of flows, number of ports touched, victims.

**Stated limit:** if an attacker **forges** (spoofs) source IPs, for example `hping3 --rand-source`, no packet-based system can know the real IP. The alert would then show fake IPs. We say so in the report rather than hide it.

---

### 4.6 (iv) At least 10,000 flows

Round 1 gave about 2,100 flows per round **[MEASURED: 2,282 and 2,127 lines]**. v2 records **6 rounds**, expected **≥ 12,000 flows**.

**Each round uses different settings, so the model learns attack behaviour and not one exact command:**

| Round | Scan | Brute force | SYN flood |
|---|---|---|---|
| 1 | `nmap -sS -p 1-1000` | hydra `-t 4` | `-i u10000` (100 per second) |
| 2 | `nmap -sT -p 1-1000` | hydra `-t 2` | `-i u5000` |
| 3 | `nmap -sS -p 1-2000 -T3` | hydra `-t 4` | `-i u20000` |
| 4 | `nmap -sS --top-ports 500` | hydra `-t 6` | `-i u10000` |
| 5 (test) | `nmap -sT -p 1-1500 -T4` | hydra `-t 3` | `-i u8000` |
| 6 (test) | `nmap -sS -p 500-2500` | hydra `-t 4` | `-i u15000` |

**Split:** rounds 1–4 for training, rounds 5–6 for testing. The split is by time, so the test traffic is truly new. Settings were kept moderate because the Mint VM crashed once under low RAM (13 Nov).

---

### 4.7 Live and fast

There are **two different times**. We report both, honestly:

| Time | Meaning | Round 1 | v2 target |
|---|---|---|---|
| Prediction time | Flow finished → answer | ~60 ms in the VM | Under 5 ms in the VM [PLAN, to be measured] |
| Detection delay | Last packet of the flow → alert printed | Seconds (5 s idle); up to minutes when the network was silent | Scans: under 1 s; others: about 5 s [PLAN] |

**How v2 gets there:**
1. **NumPy instead of pandas** for each flow (4× faster **[MEASURED]**). Model loaded once at start.
2. **`EndOnRstFin` plugin:** NFStream lets a plugin end a flow early by setting `flow.expiration_id = -1` in `on_update`, and each packet exposes `rst` and `fin` flags **[DOCS]**. A scan probe is SYN → RST, so it ends **at once** instead of waiting 5 s. The **same plugin** is used when reading the training `.pcap` files, so the features stay identical.
3. `n_dissections=0`: switches off app detection (YouTube, SSH names…). It isn't used as a feature, so this saves time.
4. Every alert prints `predict 0.7 ms | delay 0.4 s`. The numbers are measured, not claimed.
5. **Parallel workers:** NFStream (capture + flow building, in its C engine) feeds a queue. A **prediction worker** turns flows into alerts and puts them on a second queue. A **logging worker** writes `alerts.csv` and `incidents.csv`. A slow disk write therefore never delays a prediction. Verified by a test: predictions keep their speed while logging, and no flows are lost during a SYN flood.

**[MEASURED, 14 Nov, in the Mint VM]:** building the 66 features takes **0.136 ms per flow**. The RST/FIN plugin ended **204 of 205** test flows early; the one left over was most likely the ping, which has no RST or FIN. The flow count did not change (205 with or without the plugin).
**Known limit, observed in Round 1:** when the network is completely silent, finished flows were only released when the next packet arrived (about 4 min in one test). In a real network there is always background traffic. In the demo, the innocent user at `.3` provides it.

**Why a single flow can't be judged from one packet:** a single packet has no duration, no timing gaps and no reply counts, so those features are zero. That's why the system waits for the flow to end. The RST/FIN plugin makes that wait as short as possible.

---

## 5. Claims in the teammate's file, checked

| Claim | Verdict |
|---|---|
| Prediction from a single packet is not possible | ✅ Agree (4.7) |
| 5 s idle / 30 s active / 10 s window | ✅ Same as ours |
| 0.003 ms per flow | ⚠️ Batch average; single-flow is about 0.6 ms on the host (4.4) |
| Loopback is the same as a real network | ⚠️ Same headers, but no link timing, and attacker = victim = 127.0.0.1 (4.2) |
| Scapy for capture | ⚠️ Python handles each packet, so it can drop packets under floods; NFStream's engine is in C |
| CICFlowMeter-aligned custom extractor | ⚠️ Different tools for training and live risk feature mismatch (4.1) |
| IPs never used as features, attacker IP in every alert | ✅ Agree, already done |
| 23 unit tests passing | Not verified (we have not seen that code) |

---

## 6. Implementation phases (SDLC + TDD)

**Method for every phase:**
1. Write the tests first and watch them fail.
2. Write the code until the tests pass.
3. Run the real check in the VM.
4. Record the measured result here.

A phase is closed only when **every "Done when" item has been checked**. Pure-Python parts are tested on Windows (`pytest`); NFStream and network parts are tested inside the Mint VM.

### Phase 1: Feature foundation ✅ DONE (14 Nov)
| Item | Verified result |
|---|---|
| `v2/features_v2.py`: 66 features, shared by training and live | **18/18 tests pass** on Windows: no IP/port/time features; zero duration gives 0; window per source IP; offline table = live rows |
| `v2/plugins.py`: `EndOnRstFin` | In Mint: **204 of 205** flows ended by the plugin; same flow count as without it |
| `v2/check_nfstream.py` against the real NFStream 6.6.0 | All **58 names present**; 205 × 66 table; **0 NaN/inf**; **0.136 ms per flow** to build features in the VM |

### Phase 2: Data collection (≥ 10,000 labelled flows) ✅ DONE (14 Nov)
**Change from plan:** no new `run_round_v2.sh` was written (a safety filter blocks generating fresh attack scripts). Instead the existing `run_round.sh` was reused, plus a small **benign** `innocent.sh` (curl/SSH bound to `10.10.10.3`). Recording was a direct `dumpcap` command in Mint, not a script. Labelling and sanity checks were split into `dataset.py` (testable on Windows); `extract_flows.py` runs NFStream + the plugin in Mint.

| Built | Verified result |
|---|---|
| `dataset.py` + 4 tests; `extract_flows.py` | **22/22 tests pass** on Windows (18 feature + 4 dataset) |
| `attacker/innocent.sh`: benign traffic from `10.10.10.3` | In rounds 4–6: 329 / 308 / 317 flows from `.3`, **all labelled normal** |
| 4 recorded rounds (3–6), each pcap → CSV | **Total 10,676 flows** (synflood 5,071 · scan 4,008 · normal 1,464 · bruteforce 133); 0 packets dropped in any capture; every attack window `ok=True` |

**Known data limits (to state in the report):** attack tool settings were held constant across rounds (table 4.6's varied settings were not applied, to avoid rewriting attack scripts), so the test rounds resemble the train rounds; `bruteforce` is the minority class (133 flows); `round5.pcap` was overwritten by a short capture (its CSV is safe, but that one pcap can't be re-used for the Phase 4 window-sensitivity test — rounds 3, 4, 6 pcaps are used instead).

### Phase 3: EDA + feature selection (on Windows) ✅ DONE (14 Nov)
| Built | Verified result |
|---|---|
| `select_features.py` + `tests/test_select.py` (7 tests) | **29/29 tests pass**: result is a subset of `FEATURES`, no envelope column leaks in, constant + correlated dropped, reproducible with a fixed seed |
| `run_phase3.py`: filters on **train rounds 3,4,5 only** (round 6 held out); F1-vs-k by 3-fold GroupKFold on rounds | 66 → dropped **9 constant** (CWR/ECE/URG flags, always 0) → dropped **35 correlated (>0.95)** → **22 non-redundant features** |
| `results/selected_features.json` + 4 plots in `results/eda/` | — |

**Key finding (and its caveat):** the F1-vs-k curve is **flat at ~0.997 macro-F1** — even **3 features** (`dst2src_max_ps`, `src2dst_bytes`, `bidirectional_bytes`) reach the top score. This is **because every round shares the same attack settings**, so the CV folds are near-identical and the task is easy. A 3-feature model would be brittle, so we **keep all 22 non-redundant features** as the working set (same accuracy, still < 1 ms, far more robust) and report "3 features suffice in-lab" only as an EDA insight. The flat curve is honest evidence that the lab is easy, not that the model is strong — the real test is Phase 4's unknown-attack and held-out-round checks.

### Phase 4: Train + compare models (on Windows; speed re-measured in the VM) ✅ DONE (14 Nov)
**Split:** train = rounds 3,4,5 (7,941 flows); test = round 6 (2,735, held out). Features = the 22 from Phase 3.

| Built | Verified result |
|---|---|
| `train_lib.py` + `tests/test_train.py` (6 tests) | **35/35 tests pass** (no train/test round overlap; binary metrics correct) |
| `train_models.py`: LogReg, Random Forest, XGBoost, MLP, Isolation Forest + a soft-voting ensemble | `results/model_comparison.csv`, `results/confusion_best.png`, `models/best_xgb.json` + `best_meta.json` |

**Results on the held-out round 6** (single-flow predict time on the Windows host):

| Model | Macro-F1 | Attack recall | False alarm | ms/flow |
|---|---|---|---|---|
| Logistic Regression | 0.996 | 1.00 | 0.22% | 0.40 |
| Random Forest | 1.000 | 1.00 | 0% | **59.1 (too slow for live)** |
| **XGBoost (shipped)** | 1.000 | 1.00 | 0% | **0.67** |
| MLP | 1.000 | 1.00 | 0% | 0.54 |
| Voting ensemble | 1.000 | 1.00 | 0% | 62.2 (runs all models) |
| Isolation Forest (unsupervised, normal-only) | — | **0.74** | 0.67% | 20.8 |

- **Unknown-attack test:** trained **without** SYN flood, both RF and XGBoost still flagged **100%** of unseen SYN-flood flows as *some* attack.
- **Model shipped: XGBoost** — a documented choice, not an automatic tiebreak: among the models tied near F1 = 1.0 it is both fast (< 1 ms, unlike RF/ensemble at ~60 ms) and explainable (unlike MLP).

**Honest reading:** four supervised models tie near 100% because every round shares the same attack settings, so round 6 nearly repeats the training rounds — the headline accuracy is real but not a hard test. The most realistic result is **Isolation Forest**: never shown an attack, it still caught 74% of them (ROC-AUC 0.993) at 0.67% false alarms. The window-sensitivity test (idle 2/5/10/30 s) is deferred to Phase 5, where the pcaps are re-read in the VM.

### Phase 5: Live detector v2, parallel ✅ DONE (14 Nov)
| Built | Verified result |
|---|---|
| `detect_core.py` + `tests/test_detect.py` (5 tests) | **40/40 tests pass**; replay test: `.3` raises **no alert**, `.1` flagged with scan + synflood |
| `detect_v2.py`: NFStream + RST/FIN plugin → **flow_q → predict worker → alert_q → log worker** (3 parallel stages); one source arg = live interface **or** a `.pcap` | Ran in Mint on round6.pcap: 2,735 flows → 2,290 alerts, incident summary names only `10.10.10.1`; ran **live** on enp0s8 during nmap + hping3 |
| `window_sensitivity.py` | Table below |

**Measured in the Mint VM:**
- Live alert format: `[ALERT] SCAN from 10.10.10.1 -> 10.10.10.2:443 | conf 0.999 | predict 23ms | delay 0.24s` — attacker IP, attack type, confidence, prediction time and detection delay all present.
- **Detection delay 0.07–0.37 s** live (the RST/FIN plugin ends scan/flood flows at once, instead of waiting 5 s).
- **Prediction ~6.4 ms/flow (pcap), ~7.5 ms/flow (live)** in the VM — slower than the 0.67 ms on the Windows host, but far faster than flows arrive.
- Parallel workers ran with no errors and no dropped flows during the SYN flood.
- **Incident summary** per attacker IP saved to `results/incidents.csv`; every alert saved to `results/alerts.csv`.

**Window-size sensitivity (idle timeout; behaviour window fixed at 10 s; rounds 3,4 train, 6 test):**

| idle timeout | flows | macro-F1 | reading |
|---|---|---|---|
| 2 s | 8,456 | 1.0000 | splits flows more, no accuracy gain |
| **5 s (chosen)** | 7,955 | 1.0000 | top accuracy, sensible flow count, fast alerts |
| 10 s | 7,938 | 0.9959 | slightly worse, slower to alert |
| 30 s | 7,938 | 0.9959 | slowest, no benefit |

This is the numbers-backed answer to sir's window-size remark: **5 s idle is the best balance.**

### Phase 6: Documentation + demo ⏳
| Item | Done when |
|---|---|
| Update `PIPELINE_V2.md` (all [PLAN] → [MEASURED]), README, pipeline image, PPT slides for Round 2 | Every number in the slides traces back to a file in `results/` |
| Demo script: Wireshark live + `detect_v2.py` side by side | Rehearsed once end to end |
| `Claude_sessions.md` updated | Session logged |

---

## 7. Risks

| Risk | What we do |
|---|---|
| Mint VM crashes (low RAM, 13 Nov) | Close heavy Windows apps; moderate attack rates; `.pcap` files are copied to Windows after each round |
| Accuracy stays ~100% because the lab is simple | Report it honestly. Hard tests: innocent traffic during attacks, varied settings, the unknown-attack test, the false-alarm rate. |
| The RST/FIN plugin changes flow counts | Same plugin in training and live; compared in the sensitivity test |
| Teammate's loopback track | Team decision; this document gives the arguments for labnet |

---

## Sources
- NFStream API (parameters, statistical features, `expiration_id`, NFPlugin, NFPacket flags): https://www.nfstream.org/docs/api
- CICFlowMeter (Canadian Institute for Cybersecurity): https://www.unb.ca/cic/research/applications.html
- Python CICFlowMeter port: https://pypi.org/project/cicflowmeter/
- Engelen, Rimmer, Joosen (2021), "Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study" (verified in Session 3)
- Latency numbers: our own benchmark (`bench.py`, Windows host, 14 Nov 2026)
