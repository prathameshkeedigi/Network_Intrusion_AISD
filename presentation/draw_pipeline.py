"""Draws the current (Round 1, built and tested) CyberSentinel pipeline as a PNG."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = r"c:\Users\Asus\Desktop\AISD\AISD_Project\presentation\pipeline_current.png"
W, H = 100, 62
fig = plt.figure(figsize=(20, 12.4), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("white")

NAVY, RED, BLUE, GREEN, GREY, PURPLE = "#1F3A5F", "#C0392B", "#2471A3", "#1E8449", "#5D6D7E", "#7D3C98"

def box(x, y, w, h, title, body, color, fill="#FFFFFF", tsize=14, bsize=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                linewidth=2, edgecolor=color, facecolor=fill))
    if body:
        ax.text(x + w / 2, y + h - 1.05, title, ha="center", va="top", fontsize=tsize,
                fontweight="bold", color=color)
        ax.text(x + w / 2, y + (h - 2.2) / 2, body, ha="center", va="center", fontsize=bsize,
                color="#222222", linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=tsize,
                fontweight="bold", color=color)

def arrow(p, q, color="#333333", label=None, loff=(0, 0.9), lsize=11.5, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=22, linewidth=2.2, color=color))
    if label:
        ax.text((p[0] + q[0]) / 2 + loff[0], (p[1] + q[1]) / 2 + loff[1], label, ha="center",
                va="center", fontsize=lsize, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))

# ---------- title ----------
ax.text(W / 2, 60.2, "CyberSentinel AI: Current Pipeline (Round 1, built and tested)",
        ha="center", va="center", fontsize=24, fontweight="bold", color=NAVY)
ax.text(W / 2, 57.6, "Team 10  ·  Two VirtualBox VMs on a private network  ·  NFStream + XGBoost  ·  live alerts with attacker IP",
        ha="center", va="center", fontsize=13.5, color=GREY)

# ---------- row 1: machines ----------
y1, h1 = 45.5, 9.5
box(2, y1, 26, h1, "ATTACKER VM  (10.10.10.1)",
    "Normal: web pages (curl) + SSH logins\nAttacks: port scan (nmap),\nbrute force (hydra), SYN flood (hping3)", RED, "#FDEDEC")
box(37, y1, 26, h1, "VICTIM + DETECTOR VM  (Mint)",
    "IP 10.10.10.2, interface enp0s8\nRuns web server (Apache) + SSH\nNFStream + XGBoost run here", BLUE, "#EBF5FB")
box(72, y1, 26, h1, "WINDOWS LAPTOP: WIRESHARK",
    "Live packet view for humans\ndumpcap (in Mint) → SSH → Wireshark\nfilter: ip.src == 10.10.10.1", PURPLE, "#F4ECF7")
arrow((28, y1 + h1 / 2), (37, y1 + h1 / 2), RED, "labnet\n(private)", loff=(0, 2.1))
arrow((63, y1 + h1 / 2), (72, y1 + h1 / 2), PURPLE, "live\nstream", loff=(0, 2.1))

# ---------- containers ----------
cy, ch = 2.5, 37.5
ax.add_patch(FancyBboxPatch((2, cy), 45, ch, boxstyle="round,pad=0,rounding_size=1.2",
                            linewidth=2.2, edgecolor=GREEN, facecolor="#F4FBF6", linestyle="--"))
ax.add_patch(FancyBboxPatch((53, cy), 45, ch, boxstyle="round,pad=0,rounding_size=1.2",
                            linewidth=2.2, edgecolor=NAVY, facecolor="#F3F6FA", linestyle="--"))
ax.text(24.5, cy + ch - 1.6, "PHASE A: TRAINING  (offline, inside Mint)", ha="center", va="center",
        fontsize=15.5, fontweight="bold", color=GREEN)
ax.text(75.5, cy + ch - 1.6, "PHASE B: LIVE DETECTION  (inside Mint)", ha="center", va="center",
        fontsize=15.5, fontweight="bold", color=NAVY)

# arrows from victim into both phases
arrow((44, y1), (24.5, cy + ch + 0.05), GREEN, "packets on enp0s8", loff=(-4.5, 0.4))
arrow((56, y1), (75.5, cy + ch + 0.05), NAVY, "packets on enp0s8", loff=(4.5, 0.4))

# ---------- step rows ----------
bx_w, bh = 39, 4.3
rows = [32.2, 26.8, 21.4, 16.0, 10.6, 5.2]   # bottom y of each step box

train = [
    ("1. Capture flows  (capture.py)", "NFStream groups packets into flows: ends after 5 s idle / 30 s active"),
    ("2. Save to CSV", "round1_flows.csv (2,282)  ·  round2_flows.csv (2,127)  ·  extra normal (682)"),
    ("3. Label each flow", "from 10.10.10.1 inside attack time ± 5 s → attack, else normal"),
    ("4. Make 22 features  (features.py)", "20 flow statistics + 2 window counts (last 10 s)  ·  no IP / port / time"),
    ("5. Train XGBoost  (train.py)", "train: round 1  →  test: round 2  =  99.8 % correct (2,327 / 2,331)"),
    ("6. Save model", "model.json + classes.json  (normal, scan, bruteforce, synflood)"),
]
live = [
    ("1. Read packets live", "NFStream on enp0s8, same settings (5 s idle / 30 s active)"),
    ("2. Flow finished", "one conversation = same IPs, ports, protocol"),
    ("3. Same 22 features  (features.py)", "shared file → numbers identical to training"),
    ("4. Predict  (detect.py)", "XGBoost loaded once in RAM  ·  ~60 ms per flow in the VM"),
    ("5. Decide", "normal → \"ok\" line   ·   attack → ALERT (max 1 per 3 s)"),
]

def step_box(x, y, title, body, color):
    ax.add_patch(FancyBboxPatch((x, y), bx_w, bh, boxstyle="round,pad=0,rounding_size=0.6",
                                linewidth=1.8, edgecolor=color, facecolor="white"))
    ax.text(x + 1.2, y + bh - 1.15, title, ha="left", va="center", fontsize=13, fontweight="bold", color=color)
    ax.text(x + 1.2, y + 1.15, body, ha="left", va="center", fontsize=11.5, color="#222222")

for i, (t, b) in enumerate(train):
    step_box(5, rows[i], t, b, GREEN)
    if i:
        arrow((24.5, rows[i - 1]), (24.5, rows[i] + bh), GREEN)
for i, (t, b) in enumerate(live):
    step_box(56, rows[i], t, b, NAVY)
    if i:
        arrow((75.5, rows[i - 1]), (75.5, rows[i] + bh), NAVY)

# alert box (live step 6 slot)
ax.add_patch(FancyBboxPatch((56, rows[5]), bx_w, bh, boxstyle="round,pad=0,rounding_size=0.6",
                            linewidth=2.2, edgecolor=RED, facecolor="#FDEDEC"))
ax.text(75.5, rows[5] + bh - 1.15, "[ALERT] SCAN from 10.10.10.1 -> 10.10.10.2",
        ha="center", va="center", fontsize=13, fontweight="bold", color=RED, family="monospace")
ax.text(75.5, rows[5] + 1.15, "attacker IP  ·  attack type  ·  confidence  ·  ports touched in last 10 s",
        ha="center", va="center", fontsize=11.5, color="#222222")
arrow((75.5, rows[4]), (75.5, rows[5] + bh), RED)

# model hand-over: train step 6 -> live step 4 (elbow through the gap)
mx, my = 44, rows[5] + bh / 2
ty = rows[3] + bh / 2
ax.plot([mx, 50], [my, my], color=GREEN, linewidth=2.4)
ax.plot([50, 50], [my, ty], color=GREEN, linewidth=2.4)
arrow((50, ty), (56, ty), GREEN)
ax.text(50, (my + ty) / 2, "model\n.json", ha="center", va="center", fontsize=11.5, fontweight="bold",
        color=GREEN, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GREEN, lw=1.5))

# footer
ax.text(W / 2, 1.1, "Both VMs run on one laptop (VirtualBox).  Attacks stay inside the private network labnet: no real network is touched.",
        ha="center", va="center", fontsize=12, color=GREY, style="italic")

fig.savefig(OUT, dpi=150, facecolor="white")
print("saved", OUT)
