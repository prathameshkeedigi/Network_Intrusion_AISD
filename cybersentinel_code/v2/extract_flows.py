"""Run INSIDE Mint after a round:  ~/nids-env/bin/python extract_flows.py <round_no>
Reads  ~/cybersentinel/data/pcap/round<N>.pcap  and  ~/cybersentinel/data/logs/v2_round<N>_attack_log.csv
Writes ~/cybersentinel/data/flows/round<N>.csv  and prints sanity checks."""
import os, sys
import pandas as pd
from nfstream import NFStreamer
import dataset as ds
from plugins import EndOnRstFin

N = int(sys.argv[1])
D = os.path.expanduser("~/cybersentinel/data")
pcap = f"{D}/pcap/round{N}.pcap"
log_path = f"{D}/logs/v2_round{N}_attack_log.csv"
out = f"{D}/flows/round{N}.csv"

log = pd.read_csv(log_path)
print(f"Round {N}: attack log has {len(log)} rows:", list(log.label))

flows = NFStreamer(source=pcap, statistical_analysis=True, idle_timeout=5, active_timeout=30,
                   n_dissections=0, udps=EndOnRstFin()).to_pandas()
flows = flows[flows.src_ip.str.startswith("10.10.10.")].reset_index(drop=True)   # keep labnet only
table = ds.make_table(flows, log, round_no=N)
os.makedirs(os.path.dirname(out), exist_ok=True)
table.to_csv(out, index=False)

print(f"\nSaved {out}: {len(table)} flows x {table.shape[1]} columns")
print("\nFlows per label:\n" + table.label.value_counts().to_string())
print("\nFlows per source IP:\n" + table.src_ip.value_counts().to_string())

innocent = table[table.src_ip == "10.10.10.3"]
print(f"\nInnocent user 10.10.10.3: {len(innocent)} flows, labels: {innocent.label.unique().tolist()}")

print("\nAttack-window check (0 attacker flows = a step did not run or clocks differ):")
print(ds.attack_window_report(table, log).to_string(index=False))
