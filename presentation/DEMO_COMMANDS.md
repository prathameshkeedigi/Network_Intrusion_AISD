# CyberSentinel AI: Live Demo Commands

**Mint VM** = victim + detector, IP `10.10.10.2`, SSH port **2222**
**Attacker VM** = attacker, IP `10.10.10.1`, SSH port **2223**
Log in as `prathamesh` in both.

---

## A. Before the presentation (about 5 minutes)

| # | Where | Command | What it does |
|---|---|---|---|
| 1 | VirtualBox | Start **LINUXMINT-OS** and **Attacker**, log in as `prathamesh` | Turns on both virtual machines |
| 2 | Windows terminal 1 | `ssh -p 2222 prathamesh@127.0.0.1` | Opens a terminal **inside the Mint VM** from Windows (port 2222 leads to Mint) |
| 3 | Windows terminal 2 | `ssh -p 2223 prathamesh@127.0.0.1` | Opens a terminal **inside the Attacker VM** (port 2223 leads to Attacker). The prompt shows `prathamesh@attacker` |
| 4 | Attacker | `ping -c 2 10.10.10.2` | Checks that the attacker can reach Mint over the private lab network. Expect `0% packet loss` |
| 5 | Mint | `systemctl is-active ssh apache2` | Checks that the victim services (SSH server and web server) are running. Expect `active` twice |

If step 4 or 5 fails, restart both VMs and try again.

---

## B. During the demo (after slide 11)

| # | Where | Command | What it does | What you should see on Mint |
|---|---|---|---|---|
| 1 | **Mint** | `sudo ~/nids-env/bin/python ~/cybersentinel/detect.py enp0s8` | Starts our live detector. It reads every packet on the lab network card `enp0s8`, groups packets into flows, computes the 22 features, asks the trained XGBoost model, and prints `ok` or `[ALERT]`. `sudo` is needed because reading live packets needs admin rights | `CyberSentinel live detector on enp0s8 ...` |
| 2 | **Attacker** | `~/run_normal.sh 600 > /dev/null 2>&1 &` | Runs normal traffic (opening web pages and logging in over SSH) for 10 minutes in the background. The `&` lets you keep typing. This also keeps the network busy so alerts show up quickly | Lines ending in `ok` |
| 3 | **Attacker** | `nmap -p 1-1000 10.10.10.2` | **Port scan attack.** Knocks on 1000 ports of Mint in under a second to find open services | `[ALERT] SCAN from 10.10.10.1 ...` (can keep printing for up to a minute) |
| 4 | **Attacker** | `hydra -l victim -P ~/pw_demo.txt -t 4 -f ssh://10.10.10.2` | **Password guessing (brute force) attack.** Tries 31 passwords for the user `victim` over SSH, 4 at a time, and stops when it finds the right one | `[ALERT] BRUTEFORCE from 10.10.10.1 ...` (takes about 1 minute) |
| 5 | **Attacker** | `sudo timeout 10 hping3 -S -p 80 -i u10000 10.10.10.2` | **SYN flood attack.** For 10 seconds, sends about 100 fake "start connection" packets per second to the web server (port 80) and never finishes them | `[ALERT] SYNFLOOD from 10.10.10.1 ...` |
| 6 | **Mint** | Press **Ctrl+C** | Stops the detector | A summary: how many flows were predicted as normal, scan, bruteforce and synflood |
| 7 | **Attacker** | `kill %1` | Stops the background normal traffic from step 2 | — |

**Wait 20 to 30 seconds between the attacks** so each alert is clearly separate.

---

## C. If something goes wrong

| Problem | What to do |
|---|---|
| `ssh: connect to host 127.0.0.1 port 2222: Connection refused` | The VM is not fully started yet. Wait 30 seconds and try again |
| Detector shows no lines at all | Check that step 2 (normal traffic) is running. Check `ip -br a` on Mint: `enp0s8` must show `10.10.10.2` |
| Scan alert is slow to appear | Normal. The slow VM checks about 1000 flows one by one. Keep talking and it will appear |
| Attacker asks for a password during hping3 | Type the Linux password. `sudo` needs it |
| Need to show the training results again | On Mint: `cd ~/cybersentinel && ~/nids-env/bin/python train.py` (prints the 99.8% result and confusion matrix, about 1 minute) |

---

## D. Where the project files are (inside the Mint VM)

| File | What it is |
|---|---|
| `~/cybersentinel/capture.py` | Records flows from the network into a CSV file (used to collect our dataset) |
| `~/cybersentinel/features.py` | Labelling and the 22 features. Shared by training and the live detector |
| `~/cybersentinel/train.py` | Trains XGBoost on round 1 and tests on round 2 |
| `~/cybersentinel/detect.py` | The live detector |
| `~/cybersentinel/model.json`, `classes.json` | The saved trained model |
| `~/cybersentinel/data/` | Our dataset: `round1_flows.csv`, `round2_flows.csv`, `normal_extra_flows.csv`, and the attack time logs |
| Attacker: `~/run_round.sh`, `~/run_normal.sh`, `~/pw.txt`, `~/pw_demo.txt` | Scripts that generated normal traffic and attacks, and the password lists |
