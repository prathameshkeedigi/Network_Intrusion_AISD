# CyberSentinel AI – Live Network Intrusion Detection

**Team 10, AISD (AI-Assisted Software Development)**
Bachu Venkata Siva Jaideep (01fe24bci084) · Nilaksha Nath (01fe24bci087) · Sunayana Kamath (01fe24bci073) · Prathamesh K Eedigi (01fe24bci006)

This README is the **single source of truth** for the project. It tells the whole story from the start: the problem we were given, everything we studied, the first version we built, the review remarks our guide gave us, and the second version (Pipeline v2) we built to answer those remarks. Read it top to bottom once; after that, use the contents list to jump around.

> **Two versions exist.** **v1** is the first prototype (22 features, one model, shown at the first review). **v2** is the upgraded pipeline built after the review (66 features, feature selection, five models, parallel live detector). Both are real and both work. The timeline in section 2 explains how we got from one to the other.

---

## Current status (15 Nov 2026)

| Part | Status |
|---|---|
| v1 prototype (VM lab, 22 features, XGBoost) | ✅ Done, 99.8% on an unseen session |
| Live packets into Windows Wireshark | ✅ Working |
| **v2 Phase 1** – 66 features + RST/FIN plugin | ✅ Done, tested |
| **v2 Phase 2** – data collection (10,676 flows) | ✅ Done |
| **v2 Phase 3** – EDA + feature selection (→ 22) | ✅ Done |
| **v2 Phase 4** – 5 models + ensemble compared | ✅ Done, ship XGBoost |
| **v2 Phase 5** – parallel live detector + window test | ✅ Done, runs live in the VM |
| **v2 Phase 6** – docs + demo wrap-up | ⏳ In progress (this README is part of it) |
| **Tests** | ✅ **40/40 passing** (`cybersentinel_code/v2/tests/`) |

---

## START HERE — for my teammates (read this first)

You have only heard the high-level idea (attacker VM + victim VM + a private network `labnet`). This section gets you from zero to productive. The numbered sections after it are the deep reference.

### A. What already exists (so you don't redo it)
We have a **working** intrusion-detection system, built in two versions:
- **v1** — the first prototype: 2 VMs, 22 features, one XGBoost model, **99.8%** on an unseen session. Shown at the first review.
- **v2** — the upgraded pipeline (after the review): **66 features → selected to 22**, **5 models + an ensemble compared**, a **parallel live detector** that names the attacker IP, **10,676 labelled flows**, **40 automated tests passing**, and live packets visible in **Windows Wireshark**.

So the lab, the data, the features and a strong baseline are **done**. Your job is not to rebuild this — it is to try a **different methodology** and compare.

### B. What YOU need to do
Our guide gave us research papers and asked each of us to implement a **different methodology**, then present a **comparative analysis**. The papers are read, converted and grouped in **`research_md/`** — start with **`research_md/GROUPING_ANALYSIS.md`** (it explains the grouping, the mindset this project needs, and a suggested split). The proposed assignment:

| Member | Track (folder in `research_md/`) | Builds |
|---|---|---|
| 1 | **G4 — Feature eng. + imbalance** | SMOTE/oversampling + feature selection + PCA with tree models (extends our XGBoost) |
| 2 | **G2 — Sequence / attention DL** | an LSTM **or** a small Transformer |
| 3 | **G3 — Hybrid / ensemble** | stack XGBoost + an LSTM/autoencoder |
| 4 | **G5 — Explainable AI** | wrap the best model with SHAP + a 2-stage filter |

Everyone reads **G0 (surveys)** first and uses **G1 (comparative benchmarks)** as the template for the comparison. **All four train on the SAME dataset and report the SAME metrics** (below), so the comparison is fair.

### C. The dataset — use THESE exact CSVs (do not make your own)
```
cybersentinel_code/v2/data/flows/all_flows.csv      ← 10,676 flows, use this
cybersentinel_code/v2/data/flows/round3..6.csv      ← the same data, per recording round
```
- **74 columns** = `round` + 6 "envelope" columns + **66 feature columns** + `label`.
- **Envelope (metadata, NEVER use as model input):** `src_ip, src_port, dst_ip, dst_port, bidirectional_first_seen_ms, bidirectional_last_seen_ms`. These are for labelling and for showing the attacker IP — feeding them to the model would let it cheat on addresses.
- **Label counts:** normal 1,464 · scan 4,008 · synflood 5,071 · bruteforce 133 (brute force is the hard minority class — use class weights).
- **Agreed split (use this so results are comparable):** train on **rounds 3, 4, 5**; test on **round 6**.
- The 22 features our baseline selected are listed in `cybersentinel_code/v2/models/best_meta.json`.
- **Report for every model:** accuracy, macro-F1, per-class recall, false-alarm rate on normal, and **single-flow prediction time (ms)** — speed matters for a live IDS.

Load it like this:
```python
import pandas as pd
from cybersentinel_code.v2 import features_v2 as fv   # or copy FEATURES/ENVELOPE lists
df = pd.read_csv("cybersentinel_code/v2/data/flows/all_flows.csv")
X = df[fv.FEATURES]           # the 66 features (no IPs/ports/time)
y = df["label"]
train = df[df["round"].isin([3,4,5])]; test = df[df["round"]==6]
```

### D. Do you need the VMs?
- **For the ML/DL work: NO.** The data is already captured. Just use `all_flows.csv` on your own laptop (Windows or Linux) with Python + scikit-learn/XGBoost/PyTorch. This is the fastest way to start.
- **Only if you want to capture NEW traffic** do you need the lab (section 18). It runs on **VirtualBox or VMware** with **Linux Mint**. Two VMs on a private network; details in sections 8 and 18.

### E. How we actually drive the VMs (the trouble we hit, and the fix)
This saved us hours — do it from the start.
- **The problem:** at first we typed/pasted commands **directly into the VirtualBox VM windows**. The VMs run slowly (VirtualBox falls back to a slow mode over Windows Hyper-V, and RAM is tight), so long pastes were **slow, unreliable, and sometimes arrived scrambled** as the terminal redrew. Passing commands through WhatsApp/chat into the VM window was clumsy and error-prone.
- **The fix — drive both VMs over SSH from Windows (VS Code terminals):** enable SSH inside each VM, then forward a localhost port to each. Now you paste into a normal Windows terminal, which is fast and reliable, and you can keep several terminals open. On **VirtualBox** (run in **cmd**, VMs powered off):
  ```
  "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "LINUXMINT-OS" --natpf1 "ssh,tcp,127.0.0.1,2222,,22"
  "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Attacker"    --natpf1 "ssh,tcp,127.0.0.1,2223,,22"
  ```
  Then: `ssh -p 2222 prathamesh@127.0.0.1` (victim) and `ssh -p 2223 prathamesh@127.0.0.1` (attacker). Minimise the VM windows and work from the terminals.
  (On **VMware**: no port-forward needed — find the VM's IP with `ip -br a` and `ssh prathamesh@<that-ip>` directly.)

### F. Your 5-minute reading path
1. This START-HERE section.
2. Section 2 — the timeline (how we got here).
3. Section 11 — what v2 is and how it answers the review remarks.
4. The dataset note (C above).
5. `research_md/GROUPING_ANALYSIS.md` + your assigned paper group.

---

## Contents

1. [The project in one paragraph](#1-the-project-in-one-paragraph)
2. [Complete timeline (how the project evolved)](#2-complete-timeline-how-the-project-evolved)
3. [Networking basics you need first](#3-networking-basics-you-need-first)
4. [The problem we were given](#4-the-problem-we-were-given)
5. [Literature survey: everything we studied](#5-literature-survey-everything-we-studied)
6. [Our observations (the four "dots")](#6-our-observations-the-four-dots)
7. [Our main idea and conclusions](#7-our-main-idea-and-conclusions)
8. [The lab: our VM method](#8-the-lab-our-vm-method)
9. [Version 1 (the first review prototype)](#9-version-1-the-first-review-prototype)
10. [The first review: our guide's remarks](#10-the-first-review-our-guides-remarks)
11. [Version 2 (Pipeline v2: answering the remarks)](#11-version-2-pipeline-v2-answering-the-remarks)
12. [Results](#12-results)
13. [How to run everything](#13-how-to-run-everything)
14. [All project files](#14-all-project-files)
15. [Problems we hit and how we solved them](#15-problems-we-hit-and-how-we-solved-them)
16. [Limitations](#16-limitations)
17. [Next steps](#17-next-steps)
18. [Rebuilding the lab from scratch](#18-rebuilding-the-lab-from-scratch)
19. [Where everything is](#19-where-everything-is)

---

## 1. The project in one paragraph

CyberSentinel AI watches network traffic **live** and decides, for every conversation between two computers, whether it is **normal** or one of three **attacks** (port scan, password guessing, SYN flood). Instead of training on a downloaded dataset, we built a **safe lab of two virtual machines** on one laptop, created our **own labelled traffic** in it, and trained a machine-learning model. The same code records the training data and runs live, so the model sees the same kind of data in both. The live detector prints an alert naming the **attacker's IP address**, the attack type, the confidence, how long prediction took, and how long after the attack the alert appeared.

---

## 2. Complete timeline (how the project evolved)

This is the full story, in order. Exact session notes are in `Claude_sessions.md` at the repo root.

| # | Stage | What happened |
|---|---|---|
| 1 | **Problem given** | Our guide asked us to test the project on **real, live data (like Wireshark)** and predict whether the traffic is an attack. The original synopsis (`CyberSentinel_AI_Synopsis_Justified.docx`) listed modules and a tech stack; we treated those as **not final** and re-decided everything from research. |
| 2 | **Research (≈6–13 Nov)** | We compared live-capture tools and existing IDS systems, read ~10 GitHub projects (descriptions only), and **verified key research claims against the original papers** (section 5). Finding: public datasets and the tools that built them are unreliable, so we should make our own data. |
| 3 | **Plan decided** | A VirtualBox lab on one laptop: a victim VM and an attacker VM on a **private network (`labnet`)** that never leaves the laptop. Capture with **NFStream** (same code for training and live). Attacks only inside this lab, which is **legal** (section 5.4). |
| 4 | **Lab built** | Two VMs, the private network, fixed IPs (attacker `10.10.10.1`, victim `10.10.10.2`), SSH + Apache on the victim as attack targets, and attack tools (`nmap`, `hydra`, `hping3`) on the attacker. We also set up **SSH control from Windows** so we could drive both VMs from VS Code terminals. |
| 5 | **v1 data + model** | Recorded two sessions ("rounds") plus extra normal traffic. Built **22 features**, labelled flows automatically from the attack time-log, trained **XGBoost** on round 1, tested on round 2: **99.8%**. Built a live detector that prints alerts. |
| 6 | **First review** | We presented v1 (slides, script, filled Lab 2 / Lab 3 / SRS). Our guide gave **remarks** (section 10): window size, multiple models, the attacker IP must be shown, at least 10,000 flows, use CICFlowMeter-style features with proper FE/FS/EDA, and build a separate **Wireshark version**. |
| 7 | **Live Wireshark** | We made the private-network packets appear **live in Windows Wireshark** by streaming them over SSH (`dumpcap … \| Wireshark -k -i -`). This is the "human view" that sits next to the detector's "machine view". |
| 8 | **v2 analysis** | We compared our approach with a teammate's separate "loopback + Scapy" plan (`TEAMMATE_CLAUDE_PROMPT.md`) and decided to keep **labnet + NFStream** (a real, separate attacker IP; a faster C capture engine). We designed **Pipeline v2** to answer every remark (`PIPELINE_V2.md`). |
| 9 | **Pipeline v2 built (14 Nov)** | Six phases, each built **test-first (TDD)**: features → data (10,676 flows) → EDA + selection → five models → parallel live detector → docs. Details in section 11. |
| 10 | **Now (15 Nov)** | Phases 1–5 done and verified; Phase 6 (this README, updated slides, demo script) in progress. |

---

## 3. Networking basics you need first

| Term | Simple meaning |
|---|---|
| **IP address** | The address of a computer on a network, like a house address. Attacker `10.10.10.1`, victim `10.10.10.2`, an innocent user (added in v2) `10.10.10.3`. |
| **Port** | A numbered "door" on a computer. Each service waits behind its own door: **22 = SSH**, **80 = web server**, **53 = DNS**. |
| **Packet** | A small piece of data sent over the network. Opening one web page takes dozens of packets. |
| **Flow** | All packets of **one conversation** between two computers, summarised in one row: who talked to whom, on which port, for how long, how many packets and bytes. **Our system judges flows, not single packets.** |
| **TCP handshake** | How two computers start a conversation: **SYN** ("hello?") → **SYN-ACK** ("yes") → **ACK** ("starting"). A closed door answers **RST** ("nobody here"). **FIN** means "goodbye". |
| **SSH** | Secure Shell. Log in to a computer remotely with a username and password and run commands. |
| **Web server (Apache)** | A program that sends a web page to anyone who asks on port 80. |
| **Network card / interface** | The connection between a computer and a network. Our victim VM has two: `enp0s3` (internet via NAT) and `enp0s8` (the lab network). |
| **VM (virtual machine)** | A whole computer that runs as a program inside another computer. We use VirtualBox. |
| **NAT** | VirtualBox sends a VM's internet traffic out using the laptop's address. Used only to install software and to log in from Windows. **No attack ever uses NAT.** |
| **Internal Network (`labnet`)** | A private network VirtualBox creates **only inside the laptop** — a virtual cable between our two VMs and nothing else. All attacks happen here, so they can never reach the hostel, college or internet. |

### The three attacks, in plain words

| Attack | Analogy | In packets | Tool |
|---|---|---|---|
| **Port scan** | Trying every door handle to see which open. Reconnaissance. | SYN to many ports in under a second; closed ports reply RST. | `nmap` |
| **Brute force** | Trying key after key in the SSH door. | Many SSH connections, each trying a few passwords for user `victim`. | `hydra` |
| **SYN flood** | Calling a restaurant 100×/second and hanging up; real customers can't get through. Denial of service. | ~100 SYN packets/second to port 80, never completing the handshake. | `hping3` |

**Normal traffic** = legitimate use: opening web pages and logging in over SSH with the **correct** password, running harmless commands, with random 1–3 s pauses like a real person.

---

## 4. The problem we were given

**Test the project on real, live data (the way Wireshark shows live traffic) and predict whether that traffic is an attack.** Hard for three reasons:
1. **Live, not a ready-made file** — read traffic as it flows through a network card, not a CSV.
2. **Predict, not only capture** — Wireshark only shows packets; we must decide normal vs attack.
3. **No answer key** — live traffic has no labels, so we also need a way to prove our predictions are right.

---

## 5. Literature survey: everything we studied

### 5.1 Live-capture tools we compared
Wireshark / tshark / dumpcap, **Scapy**, pyshark, Windows **pktmon**, **NFStream**, **CICFlowMeter** (the original Java tool and a Python port), **Zeek**, and **nProbe**.

### 5.2 Existing IDS systems we read about
**Snort** and **Suricata** (rule-based), **Zeek** (scripting), **Security Onion** (a full monitoring distro), **Kitsune** (unsupervised neural IDS), and **Slips** (flow-based ML IDS).

**Why we chose NFStream:** it reads live packets **and** builds flow statistics in one Python library; the **same code** records training data and runs live, so features match; it is maintained (v6.6.0) with packages for Python 3.9–3.14 on Linux.

### 5.3 Research claims we verified against the original papers
| Finding | Source |
|---|---|
| Over **20%** of the popular CIC-IDS2017 dataset had errors and had to be rebuilt; the CICFlowMeter tool that made it had bugs (e.g. ending a TCP flow after one FIN, ignoring RST). | Engelen, Rimmer, Joosen — IEEE Security & Privacy Workshops, 2021 |
| Models trained on one public dataset and tested on another perform **close to random**. | Cantone, Marrocco, Bria — arXiv 2402.10974 (2024) |
| The **same** traffic gives **different** results when a different tool turns it into flows. | arXiv 2412.14021 (2024) |
| The Python `cicflowmeter` package calls itself "CICFlowMeter-like" and "not maintained actively" — not an exact copy of the Java tool. | PyPI page |
| NFStream feature list, `expiration_id`, the NFPlugin API and per-packet flags (used to build v2's 66 features and the RST/FIN plugin). | NFStream docs, nfstream.org/docs/api |

### 5.4 Existing GitHub projects
About **10** student/open-source projects that claim live ML detection (most use CIC-IDS2017 + CICFlowMeter, or Scapy + XGBoost). We read their **descriptions only, not their code**, so we treat them as examples, not proof. At least one openly admits a feature mismatch between training and live data — the exact trap we avoid by using one tool for both.

### 5.5 Legal limits
- **IT Act 2000 (India), Sections 43 & 66:** attacking a computer or network without permission is an offence → we attack **only our own VMs** on a private network.
- **DPDP Act 2023:** network traffic can contain personal data → we store **only flow statistics**, never packet contents.

---

## 6. Our observations (the four "dots")

1. **Dot 1 – Look at conversations, not packets.** One packet tells you nothing; a flow does. In our first capture, one YouTube flow had **3,048 packets** while a DNS lookup had **2**.
2. **Dot 2 – Downloaded datasets fail on live traffic** (the research in 5.3).
3. **Dot 3 – One flow alone can look normal** *(found in our own data)*: a normal DNS lookup = 2 packets; one port-scan flow = also 2 packets. The difference is the **pattern** — a scan touches **1000 ports in under a second**. → we added pattern features across flows.
4. **Dot 4 – Live traffic has no answer key, and we cannot attack real networks** → we need a controlled lab where we launch every attack ourselves and know exactly when.

---

## 7. Our main idea and conclusions

**Main idea ("Eureka"):** *Instead of borrowing someone else's traffic, create our own labelled live traffic in a safe lab, using the same code that will later watch the live network.*

- Attack our own VM on a private network that never leaves the laptop.
- Record the **exact start and end time** of every attack, so every flow gets its label automatically.
- The same NFStream + feature code builds the training data and runs live.

**Conclusions:**
- The full pipeline (live capture → features → model → live alert) **works** end to end, in both v1 and v2.
- A **pattern feature** we invented from our own observation (different ports touched in 10 s) is consistently one of the most useful features.
- **Near-100% is a lab result, not a real-world result.** Lab attacks are very clear. It proves the system works; it does not prove real-world accuracy. We say this openly.

---

## 8. The lab: our VM method

```
One laptop (Windows 11, Ryzen 7 7435HS, 16 GB RAM, VirtualBox 7.2.4)

Attacker VM (10.10.10.1 + 10.10.10.3)      Victim + detector VM (10.10.10.2)
normal traffic, nmap, hydra, hping3  labnet   SSH (22) + Apache (80)  +  our detector
  (+ innocent user in v2)        ----------->          enp0s8
```

| VM | VirtualBox name | Role | OS / RAM | Network cards |
|---|---|---|---|---|
| Victim + detector | `LINUXMINT-OS` | SSH + Apache targets **and** the detector | Linux Mint 22.2, 4 GB, 4 CPUs | Adapter 1: NAT (`enp0s3`) · Adapter 2: `labnet` (`enp0s8`, **10.10.10.2**) |
| Attacker | `Attacker` | Honest user **and** attacker | Linked clone, 2 GB, hostname `attacker` | Adapter 1: NAT · Adapter 2: `labnet` (`enp0s8`, **10.10.10.1**; in v2 also **10.10.10.3**) |

- VM folders are on **D:** (`D:\Linux_mint\...`). Log in as **`prathamesh`** in both. The user **`victim` / `Summer2024`** is only a target for the password-guessing attack.
- **SSH from Windows** (easier than the slow VM windows), on `127.0.0.1` only:
  - `ssh -p 2222 prathamesh@127.0.0.1` → victim (Mint)
  - `ssh -p 2223 prathamesh@127.0.0.1` → attacker
- **Which VM am I in?** `ip -br a | grep enp0s8` → `10.10.10.2` = victim, `10.10.10.1` = attacker.

---

## 9. Version 1 (the first review prototype)

The first working system, shown at the first review. Code lives in the victim VM at `~/cybersentinel/` and is backed up on Windows in `cybersentinel_code/`.

- **Data:** round 1 (train) + round 2 (test) + a 10-minute normal-only session. ~2,300 flows per round.
- **22 features:** amounts (packets/bytes, per direction), duration, packet sizes (min/mean/std/max), gaps between packets, TCP flag counts, protocol, and **2 pattern features** (`win_flows_10s`, `win_dst_ports_10s`). **No IP, port or timestamp is a feature**, so the model learns behaviour, not addresses.
- **Labelling:** a flow is an attack **only if** it comes from `10.10.10.1` **and** started within (attack start − 5 s, attack end + 5 s). Everything else is normal. No hand-labelling.
- **Model:** XGBoost (200 trees, depth 4, lr 0.1, balanced class weights). Train on round 1, test on round 2.
- **Result: 99.8%** (2,327 / 2,331). Live detector printed the correct alert for all three attacks.
- **Known weak points (which v2 fixes):** only one model; only ~2,300 flows per round; normal and attack traffic never overlapped in time; prediction was ~60 ms/flow (it built a pandas DataFrame per flow).

Files: `capture.py`, `features.py`, `train.py`, `detect.py`, `model.json`, `classes.json` (in `~/cybersentinel/`), and `attacker/run_round.sh`, `attacker/run_normal.sh`.

---

## 10. The first review: our guide's remarks

Captured in `TEAMMATE_CLAUDE_PROMPT.md`. After the first review our guide asked us to:

1. **Features:** use **CICFlowMeter-style (≈81) features** and do proper **Feature Engineering, Feature Selection, EDA, model building and evaluation**.
2. **Wireshark version:** build a separate version that works with **live Wireshark-style capture**.
3. **(i) Window size:** state clearly what the "window size" of a flow is.
4. **(ii) Multiple models:** don't use only XGBoost — compare **different ML models**.
5. **(iii) Attacker IP:** the system must **know and show the attacker's IP**.
6. **(iv) Scale:** test on **at least 10,000 flows**.

Plus our own main question: **how to legally create attack packets** → only inside our own private lab (`labnet`) or on loopback; never on real/college/hostel networks (IT Act 2000).

---

## 11. Version 2 (Pipeline v2: answering the remarks)

Full design and verified results: **`AISD_Project/docs/PIPELINE_V2.md`**. Code: **`cybersentinel_code/v2/`** (13 Python files, 40 tests). Built in six phases, each **test-first (TDD)**: write the tests, watch them fail, write the code until they pass, then verify on real data.

### How each remark is answered
| Remark | v2 answer |
|---|---|
| ≈81 features + FE/FS/EDA | **66 features** (58 NFStream statistics + 8 engineered), then EDA + feature selection down to **22**, plus a full **ydata-profiling HTML report**. |
| Wireshark version | Three uses of Wireshark: **live view** (dumpcap→SSH→Wireshark), **recording** each round as a `.pcap`, and a **detector that reads any `.pcap`**. |
| (i) Window size | A flow ends after **5 s idle** or **30 s active**, or at once on **RST/FIN** (a plugin). The behaviour window is **10 s per source IP**. Backed by a **sensitivity test** (section 12). |
| (ii) Multiple models | **5 models** + a voting ensemble compared on the same split, on accuracy **and** speed. |
| (iii) Attacker IP | In **every alert**. v2 also runs an **innocent user `10.10.10.3`** during the attacks, so the system must pick the attacker out of two live sources — and it never flags the innocent one. |
| (iv) 10,000 flows | **10,676 flows** across 4 recorded rounds. |

### The six phases (all verified)
1. **Features** (`features_v2.py`, `plugins.py`): 66 features shared by training and live; the `EndOnRstFin` plugin ends scan/flood flows instantly. Checked against real NFStream in the VM (0.136 ms/flow to build features). **18 tests.**
2. **Data** (`extract_flows.py`, `dataset.py`, `attacker/innocent.sh`): 4 rounds recorded as `.pcap` with dumpcap, flows extracted and labelled. **10,676 flows** (synflood 5,071 · scan 4,008 · normal 1,464 · bruteforce 133), 0 packets dropped. **4 tests.**
3. **EDA + selection** (`run_phase3.py`, `select_features.py`): 66 → dropped 9 constant → dropped 35 correlated → **22 features**. Plots + `eda_report.html`. **7 tests.**
4. **Models** (`train_models.py`, `train_lib.py`): Logistic Regression, Random Forest, XGBoost, MLP, Isolation Forest + a voting ensemble; unknown-attack test; single-flow speed. **Ship XGBoost.** **6 tests.**
5. **Live detector** (`detect_v2.py`, `detect_core.py`, `window_sensitivity.py`): **parallel workers** (capture → predict → log) so a slow disk write never delays a prediction; alert shows attacker IP + prediction ms + detection delay; reads a live interface **or** a `.pcap`; window-sensitivity test. **5 tests.**
6. **Docs + demo:** `PIPELINE_V2.md`, this README, `pipeline_v2.png`, `DEMO_COMMANDS_V2.md`, updated slides.

### The v2 architecture
```
 ATTACKER VM                          VICTIM VM (Mint) 10.10.10.2, enp0s8
 10.10.10.1 = attacker   labnet       ┌───────────────┴───────────────┐
 10.10.10.3 = innocent  --------->     ▼                               ▼
                               HUMAN VIEW                       MACHINE VIEW
                        dumpcap → SSH → Windows Wireshark   NFStream + RST/FIN plugin
                                                              → features_v2 (shared)
                                                              → XGBoost in RAM (NumPy row)
                                                              → parallel: predict | log
                                                              → ALERT: time | ATTACKER IP |
                                                                victim:port | type | conf |
                                                                predict ms | delay s
                                                              → alerts.csv + incidents.csv
```

---

## 12. Results

### 12.1 v1 (first review)
- Dataset: round 1 + round 2 + extra normal (~2,300 flows/round).
- **Accuracy 99.8%** (2,327 / 2,331) on the unseen round 2. 3 normal logins flagged as brute force; 1 scan flow missed of 1,002.
- Live: all three attacks alerted correctly; ~60 ms/flow in the VM.

### 12.2 v2 model comparison (test = held-out round 6, 2,735 flows)
| Model | Macro-F1 | Attack recall | False alarm | Speed/flow |
|---|---|---|---|---|
| Logistic Regression | 0.996 | 1.00 | 0.22% | 0.40 ms |
| Random Forest | 1.000 | 1.00 | 0% | 59 ms (too slow for live) |
| **XGBoost (shipped)** | 1.000 | 1.00 | 0% | **0.67 ms** |
| MLP | 1.000 | 1.00 | 0% | 0.54 ms |
| Voting ensemble | 1.000 | 1.00 | 0% | 62 ms |
| Isolation Forest (unsupervised, normal-only) | — | **0.74** | 0.67% | 20.8 ms |

- **Unknown-attack test:** trained **without** SYN flood, RF and XGBoost still flagged **100%** of unseen SYN-flood flows as *some* attack.
- **We ship XGBoost** — a documented choice: among the models tied near F1 = 1.0 it is both fast (< 1 ms) and explainable; Random Forest at 59 ms is too slow, MLP is a black box.
- **Honest reading:** four models tie near 100% because all rounds share the same attack settings, so round 6 nearly repeats training — real but not a hard test. The most realistic result is **Isolation Forest**: never shown an attack, it caught **74%** of them (ROC-AUC 0.993) at 0.67% false alarms.

### 12.3 v2 window-size sensitivity (answers remark (i))
Re-reading the pcaps with different idle timeouts (behaviour window fixed at 10 s; rounds 3,4 train, 6 test):

| idle timeout | flows | macro-F1 |
|---|---|---|
| 2 s | 8,456 | 1.0000 |
| **5 s (chosen)** | 7,955 | 1.0000 |
| 10 s | 7,938 | 0.9959 |
| 30 s | 7,938 | 0.9959 |

**5 s is the best balance:** top accuracy, sensible flow count, fast alerts.

### 12.4 v2 live run (measured in the VM)
- Alerts for scan, SYN flood and brute force, all **from `10.10.10.1`**; the innocent `10.10.10.3` was never flagged.
- **Detection delay 0.07–0.37 s** (the RST/FIN plugin ends scan/flood flows at once).
- **~7.5 ms/flow** in the VM (vs 0.67 ms on the Windows host). Parallel workers lost no flows during the SYN flood.
- Alert example: `[ALERT] SCAN from 10.10.10.1 -> 10.10.10.2:443 | conf 0.999 | predict 7ms | delay 0.24s`.

---

## 13. How to run everything

### 13.1 Live demo (v2) — full runbook in `presentation/DEMO_COMMANDS_V2.md`
Terminals: **T1** attacker (`ssh -p 2223`), **T2** Wireshark (Windows cmd), **T3** Mint (`ssh -p 2222`).

**If the VMs rebooted**, re-add the innocent user on T1: `sudo ip addr add 10.10.10.3/24 dev enp0s8`.

1. **Human view (T2, Windows cmd):**
   `ssh -p 2222 prathamesh@127.0.0.1 "dumpcap -i enp0s8 -q -w -" | "C:\Users\Asus\Desktop\Wireshark\Wireshark.exe" -k -i -` (type the Mint password within 1 min).
2. **Detector (T3, Mint):** `sudo ~/nids-env/bin/python ~/cybersentinel/v2/detect_v2.py enp0s8`
3. **Attacks (T1, attacker):**
   ```bash
   cd ~ && ./innocent.sh 300 > /tmp/i.log 2>&1 &
   nmap -p 1-200 10.10.10.2
   sudo timeout 5 hping3 -S -p 80 -i u10000 10.10.10.2
   hydra -l victim -P ~/pw.txt -t 4 -f ssh://10.10.10.2
   ```
4. **Stop:** Ctrl+C in T3 (prints the incident summary); `pkill -f innocent.sh` in T1.
5. **Fallback if the VM lags:** replay a saved capture — `~/nids-env/bin/python ~/cybersentinel/v2/detect_v2.py ~/cybersentinel/data/pcap/round6.pcap`.

### 13.2 Re-run the v2 analysis on Windows (no VM)
```
cd AISD_Project\cybersentinel_code\v2
python -m pytest -q            # 40 tests
python run_phase3.py          # EDA + feature selection -> results/
python train_models.py        # 5 models + ensemble -> results/model_comparison.csv
```

### 13.3 Record a new round in the VM
T3 (Mint): `dumpcap -i enp0s8 -w ~/cybersentinel/data/pcap/roundN.pcap`
T1 (attacker): `./innocent.sh 900 >/tmp/i.log 2>&1 &` then `./run_round.sh N`, then copy the log:
`scp ~/roundN_attack_log.csv prathamesh@10.10.10.2:~/cybersentinel/data/logs/v2_roundN_attack_log.csv`
T3: Ctrl+C, then `~/nids-env/bin/python ~/cybersentinel/v2/extract_flows.py N`.

---

## 14. All project files

### 14.1 v2 code (`cybersentinel_code/v2/`)
| File | What it does |
|---|---|
| `features_v2.py` | The 66 features + 10-s window tracker + labelling. **Shared by training and live.** |
| `plugins.py` | `EndOnRstFin` — ends a flow at once on RST / on FIN from both sides. |
| `dataset.py` | Turns a flow table into the labelled training table + attack-window sanity check. |
| `extract_flows.py` | (VM) pcap → labelled CSV with 66 features. |
| `check_nfstream.py` | (VM) checks our feature names against the real NFStream. |
| `select_features.py`, `run_phase3.py` | EDA + feature selection (constant → correlated → mutual information → F1-vs-k). |
| `train_lib.py`, `train_models.py` | Train and compare 5 models + ensemble; unknown-attack test; speed; best model. |
| `detect_core.py` | Predict → alert → incident logic (testable, no NFStream). |
| `detect_v2.py` | (VM) the parallel live/pcap detector. |
| `window_sensitivity.py` | (VM) the window-size test. |
| `make_eda_report.py` | Builds the ydata-profiling HTML report. |
| `tests/` | 40 tests: `test_features_v2.py`, `test_dataset.py`, `test_select.py`, `test_train.py`, `test_detect.py`. |
| `results/` | `model_comparison.csv`, `selected_features.json`, `unknown_attack_test.json`, `confusion_best.png`, `eda_report.html`, `eda/` plots, and live `alerts.csv` / `incidents.csv`. |
| `models/` | `best_xgb.json`, `best_meta.json` (the shipped model + its 22 features). |
| `data/flows/` | `round3.csv … round6.csv` (the 10,676-flow dataset). |

### 14.2 v1 code (`cybersentinel_code/`)
`capture.py`, `features.py`, `train.py`, `detect.py`, and `attacker/run_round.sh`, `attacker/run_normal.sh`. In the VM, v2 also uses `attacker/innocent.sh`.

### 14.3 Documents (`AISD_Project/`)
`docs/PIPELINE_V2.md` (v2 design + verified results), `docs/TEAMMATE_CLAUDE_PROMPT.md` (the review remarks), `presentation/` (slides, `DEMO_COMMANDS_V2.md`, `pipeline_v2.png`, script, labs, SRS), `docs/CyberSentinel_AI_Synopsis_Justified.docx` (original synopsis), `research_md/` (the IDS papers grouped by methodology, see `research_md/GROUPING_ANALYSIS.md`), and `Claude_sessions.md` at the repo root (session log).

---

## 15. Problems we hit and how we solved them

| Problem | Cause | Fix |
|---|---|---|
| C: drive low on space | Old Mint attempts on C: | Moved to D:; the real VM was already on D: |
| VM "Inaccessible" / "No bootable medium" | Folder renamed; a VM created with **New** instead of **Add** | Used **Machine → Add** on the real `.vbox` |
| VMs very slow | VirtualBox runs in slow "NEM" mode over Windows Hyper-V; low free RAM | Closed heavy apps; reduced VM RAM. Did **not** turn off Hyper-V (`bcdedit`) — a boot change can trigger a BitLocker recovery prompt and we don't have the key |
| **Mint VM crashed; Caps Lock blinked** | Low RAM + slow mode → Linux kernel panic (VirtualBox passes the blink to the real keyboard) | **Not hacking, no hardware harm.** VirtualBox → Stop → Power Off, restart, wait 2–3 min. Keep fewer apps open |
| Live Wireshark stayed empty | SSH password wasn't typed in time (prompt hidden behind Wireshark) | Click the cmd window and type the Mint password within ~1 min |
| `dpkg-reconfigure` swallowed the next command | Two commands pasted together; the `[More]` prompt ate the second line | Run commands **one at a time** |
| Too few normal flows in v1 | Normal traffic is slow by design | Added a 10-min normal session (v1) and the innocent user during attacks (v2) |
| Scan alert came ~4 min late (v1) | NFStream only closes idle flows when new packets arrive; the network was silent | Keep background traffic; in v2 the RST/FIN plugin ends scan flows at once |
| `round5.pcap` overwritten by a short capture | A second recording wrote to the same filename | The `round5.csv` was already saved, so the dataset is intact; the sensitivity test uses rounds 3,4,6 pcaps |
| ydata-profiling wouldn't import | Python 3.13 venv has no `pkg_resources`; newest setuptools removed it | Installed `setuptools<80` in a **throwaway** venv (main Python untouched) |

---

## 16. Limitations

- **Near-100% is a lab result.** All rounds share the same attack settings, so the test round nearly repeats training. Real-world accuracy will be lower.
- **Brute force is the weak class** (133 flows). It is caught every time but with lower confidence (0.78–0.99). More brute-force data would firm it up.
- Prediction is ~7.5 ms/flow in the slow VM (0.67 ms on the host).
- The labelling rule assumes a fixed attacker IP and VM clocks within 5 s. A **spoofed** source IP (`hping3 --rand-source`) cannot be traced by any packet-based system — we state this openly.
- Only three attack types; no blocking; text + CSV output (no dashboard yet).

---

## 17. Next steps

1. **Vary attack settings per round** and re-test, so the test set is a genuinely harder, novel session (the biggest honest improvement).
2. Add more attacks (slow DoS / slowloris, web attacks).
3. Run the detector on real browsing traffic to measure false alarms.
4. Explain each alert with **SHAP** (which features caused it).
5. A simple **Streamlit dashboard** (live alert feed + attacker IP per row).
6. Compare against **Suricata** (rule-based) on the same traffic.
7. Offline comparison: run the **real Java CICFlowMeter** on our saved pcaps and compare its features with NFStream's.

---

## 18. Rebuilding the lab from scratch

> You only need this if you want to **capture new traffic**. For the ML/DL methodologies, just use `all_flows.csv` (START-HERE section C) — no VMs required.

> **VirtualBox or VMware** both work; the guest is **Linux Mint 22.2**. The steps below show VirtualBox. On **VMware**: create/clone the two VMs and put their second adapter on the same **host-only / LAN-segment** network (the equivalent of VirtualBox's Internal Network `labnet`); SSH straight to each VM's IP instead of using port-forwards.

> Scripts copied from Windows may have Windows line endings. On Linux: `sed -i 's/\r$//' file.sh` before running.

**1. Victim VM (Linux Mint 22.2 in VirtualBox, stored on D:)**
```bash
sudo apt update
sudo apt install -y python3-venv nmap openssh-server apache2 wireshark-common
python3 -m venv ~/nids-env
~/nids-env/bin/pip install nfstream pandas xgboost-cpu scikit-learn
sudo systemctl enable --now ssh apache2
sudo useradd -m victim && echo 'victim:Summer2024' | sudo chpasswd
sudo usermod -aG wireshark prathamesh          # capture without sudo (log out/in after)
mkdir -p ~/cybersentinel/v2 ~/cybersentinel/data/{pcap,logs,flows}
```
**2. Private network** – VM powered off: Settings → Network → Adapter 2 → Enable → *Internal Network* `labnet`. RAM 4096 MB.
**3. Attacker VM** – clone the victim → `Attacker`, **new MAC addresses**, **linked clone**, RAM 2048 MB.
**4. Fixed IPs** (`enp0s8`)
```bash
# victim
sudo nmcli con add type ethernet ifname enp0s8 con-name labnet ipv4.method manual ipv4.addresses 10.10.10.2/24 ipv6.method disabled
sudo nmcli con up labnet
# attacker
sudo nmcli con add type ethernet ifname enp0s8 con-name labnet ipv4.method manual ipv4.addresses 10.10.10.1/24 ipv6.method disabled
sudo nmcli con up labnet
sudo hostnamectl set-hostname attacker
```
**5. Attacker tools and files**
```bash
sudo apt install -y hydra hping3 sshpass curl openssh-server
{ for i in $(seq 1 150); do echo "pass$i"; done; echo Summer2024; } > ~/pw.txt
chmod +x ~/run_round.sh ~/run_normal.sh ~/innocent.sh   # copy these scripts first
```
**6. SSH from Windows** (VMs off; in cmd, without `&`)
```
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "LINUXMINT-OS" --natpf1 "ssh,tcp,127.0.0.1,2222,,22"
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Attacker" --natpf1 "ssh,tcp,127.0.0.1,2223,,22"
```
**7. Copy v2 code into the VM** (from Windows): `scp -P 2222 cybersentinel_code/v2/*.py prathamesh@127.0.0.1:~/cybersentinel/v2/` and the `models/` folder.
**8. Record, extract, detect** — see section 13.3 and 13.1.

---

## 19. Where everything is

| What | Location |
|---|---|
| This README (single source of truth) | `AISD_Project/README.md` |
| v2 design + verified results | `AISD_Project/docs/PIPELINE_V2.md` |
| Review remarks | `AISD_Project/docs/TEAMMATE_CLAUDE_PROMPT.md` |
| Original synopsis + sir's literature-survey doc | `AISD_Project/docs/` |
| IDS research papers (PDFs + grouped MD + analysis) | `AISD_Project/research_md/` (`GROUPING_ANALYSIS.md`, `source_pdfs/`) |
| v2 code, tests, results, models, data | `AISD_Project/cybersentinel_code/v2/` |
| Full dataset (10,676 flows) | `AISD_Project/cybersentinel_code/v2/data/flows/all_flows.csv` (+ per-round `round3..6.csv`) |
| v1 code backups | `AISD_Project/cybersentinel_code/` |
| v2 architecture image | `AISD_Project/presentation/pipeline_v2.png` |
| v2 demo runbook | `AISD_Project/presentation/DEMO_COMMANDS_V2.md` |
| Slides, script, labs, SRS (first review) | `AISD_Project/presentation/` |
| Sample live capture | `AISD_Project/data/labnet.pcap` |
| Session log (full history) | `Claude_sessions.md` (AISD folder root) |
| Running project + data | Inside the victim VM: `~/cybersentinel/` and `~/cybersentinel/v2/` |
| VM files | `D:\Linux_mint\LINUXMINT-OS\`, `D:\Linux_mint\Attacker\` |
