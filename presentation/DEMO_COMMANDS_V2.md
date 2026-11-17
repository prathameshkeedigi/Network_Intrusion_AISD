# CyberSentinel AI v2 — Live Demo Runbook (for the Round 2 review)

**Idea to convey:** attacks on a private network → captured live → judged by ML in real time →
the alert names the attacker's IP, while a real innocent user is also active.

Terminals used:
- **T1 = Attacker** (`ssh -p 2223 prathamesh@127.0.0.1`, prompt `prathamesh@attacker`)
- **T2 = Wireshark live stream** (plain Windows cmd)
- **T3 = Mint detector** (`ssh -p 2222 prathamesh@127.0.0.1`)
- **T4 = Windows cmd** (to open result files) — optional

---

## 0. Before sir arrives (setup, ~5 min)
1. Close heavy Windows apps (Chrome). Start both VMs in VirtualBox. Wait ~3 min.
2. Open the 3 terminals and connect (T1 attacker, T3 Mint). Leave T2 for the Wireshark command.
3. **If the VMs were rebooted**, re-add the innocent user on T1 (Attacker):
   ```bash
   sudo ip addr add 10.10.10.3/24 dev enp0s8
   ip -br a | grep enp0s8        # should show 10.10.10.1 AND 10.10.10.3
   ```

---

## 1. Human view — live packets in Wireshark

**T2 (Windows cmd)** — one line, then type the Mint password within 1 minute:
```cmd
ssh -p 2222 prathamesh@127.0.0.1 "dumpcap -i enp0s8 -q -w -" | "C:\Users\Asus\Desktop\Wireshark\Wireshark.exe" -k -i -
```
**T1 (Attacker)** — make a few packets:
```bash
ping -c 5 10.10.10.2
```
> Say: "These are real packets travelling on a private network inside my laptop, streamed live into Wireshark. No real network is touched."
> In Wireshark, type the filter `ip.src == 10.10.10.1` to show only the attacker's packets.

---

## 2. Machine view — the live ML detector (the main demo)

**T3 (Mint)** — start the detector (needs sudo for live capture):
```bash
sudo ~/nids-env/bin/python ~/cybersentinel/v2/detect_v2.py enp0s8
```

**T1 (Attacker)** — start the innocent user in the background, then run the three attacks one by one:
```bash
cd ~ && ./innocent.sh 300 > /tmp/i.log 2>&1 &
nmap -p 1-200 10.10.10.2
sudo timeout 5 hping3 -S -p 80 -i u10000 10.10.10.2
hydra -l victim -P ~/pw.txt -t 4 -f ssh://10.10.10.2
```
> Say after each: the detector prints `[ALERT] SCAN / SYNFLOOD / BRUTEFORCE from 10.10.10.1`,
> with confidence, the prediction time in ms, and the detection delay in seconds.
> "Notice the innocent user 10.10.10.3 is active the whole time and is never flagged.
> The system names the attacker: 10.10.10.1."

**Stop:** press **Ctrl+C** in T3 → it prints the **incident summary per attacker IP** and saves
`results/alerts.csv` and `results/incidents.csv`.

---

## 3. Replay a saved capture (optional, if live is slow)
Any recorded round can be replayed through the same detector with no network:
```bash
~/nids-env/bin/python ~/cybersentinel/v2/detect_v2.py ~/cybersentinel/data/pcap/round6.pcap
```

---

## 4. The results that answer sir's remarks (open on Windows)

| Open this | Shows / answers |
|---|---|
| `presentation/pipeline_v2.png` | The whole architecture |
| `cybersentinel_code/v2/results/model_comparison.csv` | **(ii)** 5 models + ensemble, accuracy and speed |
| The window table in `docs/PIPELINE_V2.md` 4.3 / Phase 5 | **(i)** window size: 5 s is best, with numbers |
| `cybersentinel_code/v2/results/eda_report.html` | **R1** full EDA on 10,676 flows |
| `cybersentinel_code/v2/results/confusion_best.png` | XGBoost result on the held-out round |
| the live alerts + incident summary | **(iii)** attacker IP, **(iv)** 10,676 flows, live + parallel |

---

## If something breaks
- **Wireshark empty:** the password wasn't typed in time → close it and redo step 1.
- **No alerts live:** make sure you ran `detect_v2.py` with `sudo`; run an attack again.
- **VM frozen / Caps Lock blinking:** VirtualBox → Stop → Power Off, restart, wait 3 min. Then replay a pcap (step 3) instead of live.
- **Fallback:** the pcap replay (step 3) always works and shows the same alerts.
