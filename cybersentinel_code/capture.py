import csv, sys
from nfstream import NFStreamer

iface, out = sys.argv[1], sys.argv[2]
COLS = ["src_ip","src_port","dst_ip","dst_port","protocol",
        "bidirectional_first_seen_ms","bidirectional_last_seen_ms","bidirectional_duration_ms",
        "bidirectional_packets","bidirectional_bytes",
        "src2dst_packets","src2dst_bytes","dst2src_packets","dst2src_bytes",
        "bidirectional_min_ps","bidirectional_mean_ps","bidirectional_stddev_ps","bidirectional_max_ps",
        "bidirectional_mean_piat_ms","bidirectional_stddev_piat_ms","bidirectional_max_piat_ms",
        "bidirectional_syn_packets","bidirectional_ack_packets","bidirectional_psh_packets",
        "bidirectional_rst_packets","bidirectional_fin_packets","application_name"]
streamer = NFStreamer(source=iface, statistical_analysis=True, idle_timeout=5, active_timeout=30)
n = 0
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(COLS)
    print("Recording on", iface, "->", out, "(Ctrl+C to stop)", flush=True)
    try:
        for f in streamer:
            w.writerow([getattr(f, c) for c in COLS])
            fh.flush()
            n += 1
            if n % 100 == 0:
                print(n, "flows saved", flush=True)
    except KeyboardInterrupt:
        pass
print("Stopped. Total flows saved:", n)
