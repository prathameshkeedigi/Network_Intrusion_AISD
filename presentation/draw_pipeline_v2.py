"""Draws CyberSentinel Pipeline v2 (design answering sir's Round 1 remarks) as a PNG."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = r"c:\Users\Asus\Desktop\AISD\AISD_Project\presentation\pipeline_v2.png"
W, H = 100, 68
fig = plt.figure(figsize=(20, 13.6), dpi=150)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

NAVY, RED, GREEN, GREY, PURPLE, ORANGE = "#1F3A5F", "#C0392B", "#1E8449", "#5D6D7E", "#7D3C98", "#D35400"
BLUE = "#2471A3"

def rbox(x, y, w, h, ec, fc="white", lw=2, ls="-", r=0.7):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                linewidth=lw, edgecolor=ec, facecolor=fc, linestyle=ls))

def badge(x_right, y_top, text, color=ORANGE):
    w = 0.62 * len(text) + 1.4
    rbox(x_right - w, y_top - 1.7, w, 1.35, color, color, lw=1, r=0.45)
    ax.text(x_right - w / 2, y_top - 1.02, text, ha="center", va="center", fontsize=10,
            fontweight="bold", color="white")

def arrow(p, q, color="#333333", ms=16, lw=2.1):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, linewidth=lw, color=color,
                                 shrinkA=0, shrinkB=0))

def label(x, y, text, color, size=11.5):
    ax.text(x, y, text, ha="center", va="center", fontsize=size, fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))

# ---------------- title + legend ----------------
ax.text(W / 2, 66.0, "CyberSentinel AI: Pipeline v2  (answers to Round 1 review remarks)",
        ha="center", va="center", fontsize=24, fontweight="bold", color=NAVY)
ax.text(W / 2, 63.6, "Team 10  ·  Two VirtualBox VMs on a private network (labnet)  ·  "
        "Wireshark + NFStream + 5 ML models  ·  live alerts with the attacker IP",
        ha="center", va="center", fontsize=13.5, color=GREY)
ax.text(W / 2, 61.4, "Orange tags:  NEW = added in v2   ·   R1 = ~81 features, FE, FS, EDA   ·   R2 = Wireshark version   ·   "
        "(i) window size   ·   (ii) multiple models   ·   (iii) attacker IP   ·   (iv) ≥ 10,000 flows",
        ha="center", va="center", fontsize=12, color=ORANGE, fontweight="bold")

# ---------------- row 1: machines ----------------
y1, h1 = 48.0, 11.2
def machine(x, title, lines, color, fill):
    rbox(x, y1, 26, h1, color, fill, lw=2.2, r=0.9)
    ax.text(x + 13, y1 + h1 - 1.3, title, ha="center", va="center", fontsize=14, fontweight="bold", color=color)
    ax.text(x + 13, y1 + (h1 - 2.4) / 2, lines, ha="center", va="center", fontsize=11.8,
            color="#222222", linespacing=1.4)

machine(2, "ATTACKER VM  (one VM, two IPs)",
        "10.10.10.1 = ATTACKER\nscan (nmap) · brute force (hydra) · SYN flood (hping3)\n"
        "settings changed every round\n10.10.10.3 = INNOCENT USER (web + SSH)", RED, "#FDEDEC")
badge(28 - 0.6, y1 + h1 - 2.4, "NEW · (iii)")
machine(37, "VICTIM + DETECTOR VM  (Mint)",
        "IP 10.10.10.2 · interface enp0s8\nweb server (Apache) + SSH = targets\n"
        "dumpcap, NFStream, features,\nmodels and alerts all run here", BLUE, "#EBF5FB")
machine(72, "WINDOWS LAPTOP: WIRESHARK",
        "LIVE packet view for humans\ndumpcap (Mint) → SSH → Wireshark\n"
        "filter: ip.src == 10.10.10.1\n(working since 13 Nov)", PURPLE, "#F4ECF7")
badge(98 - 0.6, y1 + h1 - 2.4, "R2")

mid = y1 + h1 / 2
arrow((28, mid), (37, mid), RED, ms=20, lw=2.4)
label(32.5, mid + 1.9, "labnet", RED)
label(32.5, mid - 1.9, "(private)", RED, 10.5)
arrow((63, mid), (72, mid), PURPLE, ms=20, lw=2.4)
label(67.5, mid + 1.9, "live", PURPLE)
label(67.5, mid - 1.9, "stream", PURPLE, 10.5)

# ---------------- phase containers ----------------
cy, ch = 3.4, 39.6
rbox(2, cy, 45, ch, GREEN, "#F4FBF6", lw=2.2, ls="--", r=1.2)
rbox(53, cy, 45, ch, NAVY, "#F3F6FA", lw=2.2, ls="--", r=1.2)
ax.text(24.5, cy + ch - 1.5, "PHASE A: RECORD + TRAIN  (offline, in Mint)", ha="center", va="center",
        fontsize=15, fontweight="bold", color=GREEN)
ax.text(75.5, cy + ch - 1.5, "PHASE B: LIVE DETECTION  (in Mint)", ha="center", va="center",
        fontsize=15, fontweight="bold", color=NAVY)

# feed arrows from the victim box into both phases
arrow((42, y1), (24.5, cy + ch), GREEN, ms=20, lw=2.4)
arrow((58, y1), (75.5, cy + ch), NAVY, ms=20, lw=2.4)
label(30.5, 45.5, "packets on enp0s8", GREEN, 11)
label(69.5, 45.5, "packets on enp0s8", NAVY, 11)

# ---------------- steps ----------------
bw, bh, step = 40, 4.05, 5.0
tops = [cy + ch - 3.2 - i * step for i in range(7)]      # top y of each step box

def step_box(x, top, title, body, color, tag=None, fill="white", ls="-", tcolor=None):
    y = top - bh
    rbox(x, y, bw, bh, color, fill, lw=1.8, ls=ls, r=0.55)
    ax.text(x + 1.1, y + bh - 1.1, title, ha="left", va="center", fontsize=12.8, fontweight="bold",
            color=tcolor or color)
    ax.text(x + 1.1, y + 1.05, body, ha="left", va="center", fontsize=11.2, color="#222222")
    if tag:
        badge(x + bw - 0.5, top - 0.25, tag)

train = [
    ("1. Record every round as .pcap", "dumpcap → roundN.pcap  ·  6 rounds, varied attacks  ·  ≥ 12,000 flows", "NEW · R2 · (iv)"),
    ("2. NFStream reads the .pcap", "flow ends on RST/FIN, 5 s idle or 30 s active (same as live)", "NEW · (i)"),
    ("3. Label each flow", "from 10.10.10.1 inside attack time ± 5 s → attack, else normal", "(iii)"),
    ("4. Features (features_v2.py)", "58 NFStream stats + 8 engineered ≈ 66  ·  no IP / port / time", "NEW · R1"),
    ("5. EDA + feature selection", "drop constant · drop corr > 0.95 · rank (MI, permutation) · best top-k", "NEW · R1"),
    ("6. Train + compare 5 models", "LogReg · Random Forest · XGBoost · MLP · Isolation Forest", "NEW · (ii)"),
    ("7. Pick + save best model", "rounds 1–4 train, 5–6 test · F1 + ms per flow · window test", "NEW · (i)"),
]
live = [
    ("1. Read packets live", "NFStream on enp0s8 + RST/FIN plugin → scan probes end at once", "NEW"),
    ("2. Flow finished", "RST/FIN, 5 s idle or 30 s active  ·  10 s window per source IP", "(i)"),
    ("3. Same features (features_v2.py)", "shared file → numbers identical to training (selected top-k)", None),
    ("4. Predict, best model in RAM", "one NumPy row per flow, no disk  ·  ~0.6 ms on host (measured)", "NEW"),
    None,  # alert box drawn separately
    ("6. Incident summary per attacker IP", "first/last seen · attack types · flows · ports  →  alerts.csv", "NEW · (iii)"),
    ("ALSO: detector reads any Wireshark .pcap", "detect_v2.py round5.pcap  →  same alerts, offline", "NEW · R2"),
]

for i, (t, b, tag) in enumerate(train):
    step_box(5, tops[i], t, b, GREEN, tag)
    if i:
        arrow((24.5, tops[i - 1] - bh), (24.5, tops[i]), GREEN)

for i, item in enumerate(live):
    if item is None:
        continue
    t, b, tag = item
    if i == 6:
        step_box(56, tops[i], t, b, PURPLE, tag, fill="#FBF7FD", ls="--")
    else:
        step_box(56, tops[i], t, b, NAVY, tag)

# alert box (live step 5)
ay = tops[4] - bh
rbox(56, ay, bw, bh, RED, "#FDEDEC", lw=2.4, r=0.55)
ax.text(76, ay + bh - 1.1, "5. [ALERT] SCAN from 10.10.10.1 → 10.10.10.2",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color=RED, family="monospace")
ax.text(76, ay + 1.05, "time · ATTACKER IP · attack type · confidence · predict ms · delay s",
        ha="center", va="center", fontsize=11.2, color="#222222")

for i in range(1, 6):
    c = RED if i in (4, 5) else NAVY
    arrow((76, tops[i - 1] - bh), (76, tops[i]), c)

# model hand-over: train step 7 -> live step 4 (elbow through the gap)
my = tops[6] - bh / 2
ty = tops[3] - bh / 2
ax.plot([45, 50], [my, my], color=GREEN, linewidth=2.4, solid_capstyle="round")
ax.plot([50, 50], [my, ty], color=GREEN, linewidth=2.4, solid_capstyle="round")
arrow((50, ty), (56, ty), GREEN, ms=18, lw=2.4)
ax.text(50, (my + ty) / 2, "best\nmodel", ha="center", va="center", fontsize=11, fontweight="bold",
        color=GREEN, bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GREEN, lw=1.5))

# footer
ax.text(W / 2, 1.5, "All traffic stays inside the private network labnet on one laptop: legal, no real network touched.   "
        "Status: v2 = design; the Round 1 pipeline is already built and working.",
        ha="center", va="center", fontsize=12, color=GREY, style="italic")

fig.savefig(OUT, dpi=150, facecolor="white")
print("saved", OUT)
