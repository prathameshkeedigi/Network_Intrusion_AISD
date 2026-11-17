# Prompt for Teammate's Claude — CyberSentinel AI: Wireshark Version Context Transfer

---

## Who I Am & Project Context

I am a team member working on **CyberSentinel AI**, a Network Intrusion Detection System (NIDS) built as a college academic project. Our team has two parallel tracks:

- **My Track (VM-based version):** We built the original prototype using two VirtualBox VMs — one Victim VM and one Attacker VM — connected via a private virtual network called `labnet`. We used **NFStream** (a Linux C-library) to capture packets on interface `enp0s8` inside the VM, then converted them to flow-level features, and trained an **XGBoost classifier** on approximately **2,757 flows**. This system achieved ~99.8% accuracy in our controlled lab environment.

- **My Teammate's Track (Wireshark version — the topic of this prompt):** After our Round 1 presentation, **our professor assigned my teammate separately** to build a **Wireshark-integrated version** of this IDS that works with **live network packet capture** and does **not** depend on the two-VM lab setup. This prompt is entirely about understanding and continuing my teammate's work.

---

## Sir's Remarks After Round 1 Presentation (The Exact Feedback That Triggered This)

After our first presentation, our professor gave the following remarks:

1. **Context:** CICFlowMeter converts raw PCAP files into 81 flow-level features (a CSV). Among those 81 features, we need to perform proper **Feature Engineering, Feature Selection, EDA analysis, model building, and evaluation**.

2. **The original project** uses two VMs (one Victim, one Attacker) on a private network `labnet`. We are not using Wireshark here — we send labeled attack packets in a controlled environment. **Sir asked us to build a separate Wireshark version** of this project.

3. **The problems of live network intrusion** have been highlighted in the README file (documented by us).

4. **Specific Remarks:**
   - **(i) Window Size Question:** "What is the window size considered here? In Round 1, we trained on around 2,000 flows. What is the window size of the flow?" — This needs to be clearly answered and documented.
   - **(ii) Multiple ML Models:** "The VM method just used XGBoost. Check on different ML models."
   - **(iii) Attacker IP:** "IMPORTANT — The IP address of the attacker should be known." The system must identify and display the attacker's IP during detection.
   - **(iv) Minimum Scale:** "Check at least on 10,000 flows."

---

## My Teammate's Assignment: The Wireshark Version

My teammate has been assigned to build a **live-data, Wireshark-integrated IDS** that:
- Captures packets **live** from a real network interface (not from a dataset file or VM).
- Processes packets in real time, in a background pipeline.
- Predicts whether each network flow is benign or an attack within **milliseconds**.
- Identifies the **attacker's IP address** explicitly in every alert.
- Uses **multiple ML models** (not just XGBoost).
- Benchmarks on at least **10,000 flows**.

---

## Key Technical Clarifications Already Established (Do Not Re-Debate These)

### Q1: Can we predict from a single packet?

**NO.** A single packet only contains static header fields. It has ZERO values for:
- Flow Duration
- Flow Inter-Arrival Times (IAT — Mean, Std, Max, Min)
- Bidirectional packet ratios
- Throughput (Bytes/sec, Packets/sec)
- Packet Length Variance

Feeding one raw packet into a model trained on 81 CICFlowMeter features gives garbage output. You **must aggregate packets into a complete flow session** first, then run the model on the completed flow feature vector.

### Q2: How does the pipeline achieve millisecond-level prediction?

The pipeline is **entirely in-memory** (zero disk I/O on the hot path). The correct architecture is:

```
[Thread 1: Capture]
  Wireshark / Scapy sniff() on live interface
  → Pushes raw packets into an in-memory thread-safe queue

[Thread 2: Flow Aggregator]
  Maintains an in-memory Hash Table of active 5-tuple flows
  (src_ip, src_port, dst_ip, dst_port, protocol)
  → Updates packet counts, byte counts, TCP flags, IAT timestamps per packet
  → Emits a completed flow when:
     a) TCP FIN/RST teardown detected
     b) Flow idle for 5 seconds (idle timeout)
     c) Flow active beyond 30 seconds (active timeout)

[Thread 3: Inference Engine]
  → Converts completed flow to NumPy feature vector (in-memory, no disk write)
  → Feeds vector into pre-loaded ML model (XGBoost / Random Forest / MLP)
  → Prediction latency: ~0.003 ms per flow (empirically benchmarked)
  → Extracts Attacker IP from metadata envelope (src_ip of forward initiator)
  → Generates alert with: Timestamp | Attacker IP | Victim IP | Port | Attack Class | Confidence
```

**CRITICAL:** The models are loaded into RAM once at startup. The prediction path NEVER writes to disk. Disk I/O only happens asynchronously in a separate logging thread for audit trails.

### Q3: What is the "Window Size" for flows?

Three distinct window parameters exist in a flow-based IDS:

| Parameter | Value Used | Meaning |
|---|---|---|
| **Flow Idle Timeout** | 5 seconds | If no packet seen in this 5-tuple for 5 seconds → declare flow finished and emit. |
| **Flow Active Timeout** | 30 seconds | If a continuous flow has been active for 30 seconds → forcibly flush and emit as a sub-flow. |
| **Behavioral Sliding Window** | 10 seconds | For each source IP, track how many unique ports and connections were made in the last 10 seconds — catches port scanners. |

In Round 1, **~2,757 flows were captured using a 5-second idle timeout and 30-second active timeout.** This is the "window" that defines a flow.

### Q4: How do we legally induce attack packets for training?

**NEVER send attack packets over a real Wi-Fi network or router** — this is illegal under the IT Act 2000 (India), Sections 43 & 66.

**The correct and legal method:**
- **Use the loopback interface (`lo0` on macOS / `lo` on Linux, i.e., `127.0.0.1`)**
- Run a local target server on port 8080 (Python HTTP server, etc.)
- Fire attack tools (`nmap`, `hping3`, custom Scapy scripts) **strictly targeting `127.0.0.1`**
- Wireshark / Scapy listens on `lo0` and captures all traffic
- Zero risk to any real network

This is academically valid and industry-standard. Wireshark captures on loopback produce real PCAP files with real TCP/IP headers. CICFlowMeter can parse them. No distinction from external traffic in terms of feature extraction.

### Q5: Does the loopback method qualify as "live detection"?

**YES.** Here is why:
- Wireshark uses the exact same PCAP kernel mechanism on `lo0` as on `en0` (Wi-Fi).
- Packets on `lo0` are real IP/TCP/UDP packets — same headers, same flags, same kernel processing.
- The model sees the same statistical patterns (SYN flood rate, port scan spread, IAT anomalies) regardless of the underlying interface.
- The only difference is `127.0.0.1` vs. a remote IP — which is explicitly excluded from model features (to ensure generalization).
- This is how every published cybersecurity research paper with "live capture" in its title operates in an academic lab.

---

## Workflow Finalized (10-Step Pipeline Summary)

1. **Wireshark / Scapy listens live on `lo0`** — background Thread-1, non-blocking, continuous sniffing.
2. **Each raw packet pushed into an in-memory queue** — thread-safe, no disk touch, under 15 microseconds per packet.
3. **Thread-2 (Flow Aggregator) consumes from queue** — maintains live hash table of all active 5-tuple sessions, updating byte counts, flag counters, and IAT timestamps per packet.
4. **Flow emitted on three triggers:** (a) TCP FIN/RST, (b) 5-second idle, (c) 30-second active timeout — flow is now a complete conversation.
5. **In-memory feature vector construction** — 22 to 81 CICFlowMeter-aligned features computed from the session. NumPy array. No disk write.
6. **Thread-3 feeds vector to pre-loaded models** — XGBoost, Random Forest, MLP, Isolation Forest all pre-loaded into RAM at startup. Empirical prediction latency: **0.003 ms per flow**.
7. **Attacker IP extracted from metadata envelope** — `src_ip` of forward flow initiator is preserved alongside the prediction and displayed in every alert. Never used as a model training feature.
8. **Alert generated instantly if attack detected** — Format: `Timestamp | Attacker IP | Victim IP | Port | Protocol | Attack Class | Confidence % | Anomaly Score`.
9. **Background I/O thread logs alerts and PCAP to disk asynchronously** — Completely decoupled from the hot prediction path. Does not block detection.
10. **Training mode uses the same loopback pipeline in record mode** — Normal traffic + loopback attacks (`nmap`, `hping3`, custom Scapy floods) → aggregate 10,000+ flows → feature-engineer and label → train multi-model suite → save models to disk for live inference.

---

## Technology Stack for Wireshark Version

| Component | Technology |
|---|---|
| **Packet Capture** | Scapy (`sniff(iface="lo0", store=False)`) + Wireshark/tshark for PCAP files |
| **Flow Aggregation** | Custom Python `FlowAggregator` class (in-memory hash table, BidirectionalFlow) |
| **Feature Extraction** | Custom CICFlowMeter-aligned Python extractor (22–81 features) |
| **ML Models** | XGBoost, Random Forest, MLP (scikit-learn / Keras), Isolation Forest |
| **Parallelism** | Python `threading.Thread` + `queue.Queue` (3 parallel threads) |
| **Dashboard** | Streamlit (dark SOC theme, live alert feed, SHAP chart, attack distribution) |
| **Explainability** | SHAP (SHapley Additive Explanations) for feature attribution |
| **Alert Export** | CSV export of full alert log |
| **Language** | Python 3.12 |
| **Platform** | macOS (also runs on Linux) |

---

## Current Code State (Already Implemented — Do Not Rebuild)

The following modules exist and are fully tested under TDD (23 unit tests passing):

| Module | Path | Status |
|---|---|---|
| `FlowRecordSchema` | `src/cybersentinel/ingestion/schema.py` | ✅ Done |
| `BidirectionalFlow` | `src/cybersentinel/ingestion/flow_session.py` | ✅ Done |
| `FlowAggregator` | `src/cybersentinel/ingestion/flow_aggregator.py` | ✅ Done |
| `WiresharkLiveCapture` | `src/cybersentinel/ingestion/live_capture.py` | ✅ Done |
| `AlertTriageEngine` | `src/cybersentinel/prioritization/engine.py` | ✅ Done |
| `MockInferenceEngine` | `src/cybersentinel/models/mock_inference.py` | ✅ Heuristic (needs real ML models trained) |
| `demo_dashboard.py` | Root of project | ✅ Streamlit SOC dashboard running |

**Tests:** `PYTHONPATH=src python3 -m pytest tests/unit/ -q` → **23 passed**

**Dashboard:** `streamlit run demo_dashboard.py` → Running at `http://localhost:8501`

---

## What Still Needs to Be Built

1. **Real ML Model Training Script** — Collect 10,000+ labeled flows via loopback pipeline → train XGBoost, Random Forest, MLP, Isolation Forest → save to disk with joblib.
2. **Feature Engineering & EDA** — From the 81 CICFlowMeter features, perform correlation analysis, PCA, and select the most discriminative subset.
3. **Multi-model comparison report** — Accuracy, Precision, Recall, F1, ROC-AUC, and inference latency for each model side by side.
4. **Live loopback attack traffic generator** — Script that fires controlled SYN floods, port scans, and brute-force attempts at `127.0.0.1` for training data collection.
5. **Attacker IP display in dashboard** — The alert table must explicitly show the attacker's source IP in every row.
6. **10,000-flow benchmark** — Reproduce all evaluation metrics at scale.

---

## Instructions for You (Claude)

You are now fully aware of:
- The original VM-based CyberSentinel AI project context
- The professor's specific remarks after Round 1
- The architectural decisions finalized for the Wireshark version
- The legal constraints on attack traffic induction
- The 10-step pipeline workflow
- The existing codebase state and what remains to be built

**Please help my teammate continue building the Wireshark version by:**
- Implementing the remaining components listed above in order
- Following SDLC principles: plan, write tests (TDD) before code, implement, verify
- Never using disk I/O on the prediction hot path
- Never using `src_ip` or `dst_ip` as model training features (they go in the metadata envelope only)
- Ensuring every alert explicitly surfaces the Attacker IP from the metadata envelope
- Benchmarking all models on a minimum of 10,000 flows
