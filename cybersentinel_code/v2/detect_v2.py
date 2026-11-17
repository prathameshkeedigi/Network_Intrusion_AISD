"""Live detector v2 with PARALLEL workers. Run INSIDE Mint.
  live:  ~/nids-env/bin/python detect_v2.py enp0s8
  pcap:  ~/nids-env/bin/python detect_v2.py ~/cybersentinel/data/pcap/round6.pcap

Stages run in parallel so a slow disk write never delays a prediction:
  [capture] NFStream (C engine) --flow_q--> [predict worker] --alert_q--> [log worker]
One predict worker only: flows must be fed to the window tracker in arrival order."""
import sys, os, time, csv, queue, threading
from nfstream import NFStreamer
import features_v2 as fv
import detect_core as dc
from plugins import EndOnRstFin

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else "enp0s8"
is_live = not src.endswith(".pcap")

model, feat_order, classes = dc.load_model()
tracker = fv.WindowTracker()
flow_q = queue.Queue(maxsize=20000)
alert_q = queue.Queue(maxsize=20000)
stop = threading.Event()
stats = {"flows": 0, "alerts": 0, "sum_ms": 0.0}


def predict_worker():
    while not (stop.is_set() and flow_q.empty()):
        try:
            flow = flow_q.get(timeout=0.2)
        except queue.Empty:
            continue
        row = fv.compute_features(flow, tracker)
        label, conf, ms = dc.predict_row(model, feat_order, classes, row)
        stats["flows"] += 1
        stats["sum_ms"] += ms
        if label != dc.NORMAL:
            delay = (time.time() * 1000 - flow.bidirectional_last_seen_ms) / 1000 if is_live else 0.0
            env = {"src_ip": flow.src_ip, "dst_ip": flow.dst_ip, "dst_port": flow.dst_port}
            alert_q.put(dc.make_alert(env, label, conf, ms, delay))
        flow_q.task_done()


def log_worker():
    th = dc.Throttle(3)
    inc = dc.IncidentTracker()
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    fh = open(os.path.join(HERE, "results", "alerts.csv"), "w", newline="")
    cols = ["time", "attacker_ip", "victim_ip", "dst_port", "label", "confidence", "predict_ms", "delay_s"]
    w = csv.writer(fh); w.writerow(cols)
    while not (stop.is_set() and alert_q.empty()):
        try:
            a = alert_q.get(timeout=0.2)
        except queue.Empty:
            continue
        stats["alerts"] += 1
        inc.add(a)
        w.writerow([a[k] for k in cols]); fh.flush()
        if th.allow((a["attacker_ip"], a["label"])):
            print(dc.alert_text(a), flush=True)
        alert_q.task_done()
    fh.close()
    rows = inc.summary()
    with open(os.path.join(HERE, "results", "incidents.csv"), "w", newline="") as ifh:
        if rows:
            iw = csv.DictWriter(ifh, fieldnames=list(rows[0].keys())); iw.writeheader(); iw.writerows(rows)
    print("\n=== INCIDENT SUMMARY (per attacker IP) ===", flush=True)
    for r in rows:
        print(f"  {r['attacker_ip']}: {r['attacks']} | {r['flows']} flows | {r['distinct_ports']} ports "
              f"| {r['victims']} victim(s) | {r['first_seen']} -> {r['last_seen']}", flush=True)


pw = threading.Thread(target=predict_worker)
lw = threading.Thread(target=log_worker)
pw.start(); lw.start()
print(f"CyberSentinel v2 detector on {src} | XGBoost | {len(feat_order)} features | Ctrl+C to stop", flush=True)
streamer = NFStreamer(source=src, statistical_analysis=True, idle_timeout=5, active_timeout=30,
                      n_dissections=0, udps=EndOnRstFin())
try:
    for flow in streamer:
        flow_q.put(flow)
except KeyboardInterrupt:
    print("\nstopping...", flush=True)
finally:
    flow_q.join()
    stop.set()
    pw.join(); lw.join()
    avg = stats["sum_ms"] / stats["flows"] if stats["flows"] else 0
    print(f"\nflows={stats['flows']} alerts={stats['alerts']} avg_predict={avg:.3f} ms/flow", flush=True)
