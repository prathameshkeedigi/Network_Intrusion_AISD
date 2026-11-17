"""Builds the CyberSentinel versions of Lab 2 and Lab 3 (new files; originals untouched)."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
DATE = "13 November 2026"


def new_doc(lab_title):
    d = Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2.2)
        s.left_margin = s.right_margin = Cm(2.2)
    st = d.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(6)
    for name, size in (("Heading 1", 15), ("Heading 2", 13), ("Heading 3", 12)):
        h = d.styles[name]
        h.font.name = FONT
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = RGBColor(0x1F, 0x2A, 0x44)
        rf = h.element.rPr.rFonts
        rf.set(qn("w:eastAsia"), FONT)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(6)
    t = d.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(lab_title)
    r.bold = True
    r.font.size = Pt(17)
    sub = d.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run("Project: CyberSentinel AI – Live Network Intrusion Detection").italic = True
    info = d.add_table(rows=0, cols=2)
    info.style = "Table Grid"
    for k, v in (("Name", "Prathamesh K Eedigi"), ("SRN / Roll number", "01fe24bci006 / 163"),
                 ("Division", "A"), ("Team", "Team 10 (Bachu Venkata Siva Jaideep, Nilaksha Nath, Sunayana Kamath, Prathamesh Eedigi)"),
                 ("Course", "AI-Assisted Software Development (AISD)"), ("Date", DATE)):
        row = info.add_row().cells
        row[0].text, row[1].text = k, v
        row[0].paragraphs[0].runs[0].bold = True
        shade(row[0], "E8EEF5")
    set_widths(info, [4.5, 12.1])
    d.add_paragraph()
    return d


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_widths(table, widths_cm):
    table.autofit = False
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)


def table(d, header, rows, widths, font=11):
    tb = d.add_table(rows=1, cols=len(header))
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        c = tb.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        shade(c, "D9E2EC")
    for r in rows:
        cells = tb.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = ""
            parts = v if isinstance(v, list) else [v]
            for j, part in enumerate(parts):
                p = cells[i].paragraphs[0] if j == 0 else cells[i].add_paragraph()
                p.add_run(part)
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.size = Pt(font)
    # repeat header row on new pages
    trPr = tb.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    set_widths(tb, widths)
    d.add_paragraph()
    return tb


def para(d, text, bold=False, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    return p


def bullets(d, items):
    for it in items:
        d.add_paragraph(it, style="List Bullet")


def code(d, text):
    for line in text.strip("\n").split("\n"):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(line if line else " ")
        r.font.name = "Courier New"
        r.element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
        r.font.size = Pt(9)
    d.add_paragraph()


# =====================================================================
# LAB 2
# =====================================================================
d = new_doc("Lab 2: Requirements Engineering")

d.add_heading("Part A: Functional and Non-functional Requirements", level=1)
para(d, "First, I wrote each requirement in my own words. Then I asked the AI to make it clearer and testable. "
        "In the last column I recorded my decision and the reason for it.")
d.add_heading("A1. Functional requirements (FR)", level=2)
table(d, ["Original FR", "AI-Refined FR", "Human Decision"], [
    ["i) The system should capture network traffic.",
     "The system shall capture live packets from a chosen network card (for example enp0s8) and group them into flows using NFStream.",
     "Accept. The refined version names the network card and the tool, so it can be tested."],
    ["ii) The system should detect attacks.",
     "The system shall classify every finished flow as normal, port scan, brute force or SYN flood, using a trained model.",
     "Accept. It lists the exact four classes the system must recognise."],
    ["iii) The system should show alerts.",
     "The system shall print an alert with the time, the attack type, the attacker's IP address and the number of flows whenever a flow is classified as an attack.",
     "Accept. It says exactly what an alert must contain."],
    ["iv) The system should store traffic for training.",
     "The system shall save every captured flow, with its statistics, into a CSV file so that it can be used for training and testing.",
     "Accept. It says what is stored and in which format."],
    ["v) The system should label the data.",
     "The system shall label each flow automatically, using the attacker's IP address and the logged start and end time of each attack.",
     "Accept. It explains how labels are created without manual work."],
    ["vi) The system should train a model.",
     "The system shall train the model on one recorded session and test it on a different session that was not used for training.",
     "Accept. Testing on a separate session gives an honest accuracy."],
], [5.0, 6.3, 5.3])

d.add_heading("A2. Non-functional requirements (NFR)", level=2)
table(d, ["Original NFR", "AI-Refined NFR", "Human Decision"], [
    ["The system should be fast.",
     "The system shall raise an alert within 10 seconds after an attack flow ends.",
     "Modify. In our tests, alerts were delayed when the network was completely silent. The requirement must say \"when other traffic is present on the network\"."],
    ["The system should be accurate.",
     "The system shall correctly classify at least 95% of the flows in a test session that was not used for training.",
     "Accept. It is measurable. Our model reached 99.8% on the test session."],
    ["The system should not give too many false alarms.",
     "The system shall wrongly flag less than 2% of normal flows as attacks in the test session.",
     "Accept. It is measurable. Our result was 3 out of 296 normal flows (about 1%)."],
    ["The system should be safe to test.",
     "All attack testing shall happen only on a private virtual network inside one laptop, and never on the hostel or college network.",
     "Accept. This is needed for safety and because attacking real networks without permission is illegal (IT Act 2000, Sections 43 and 66)."],
    ["Training and live detection should behave the same.",
     "The system shall use the same feature code (features.py) for training and for live detection.",
     "Accept. If the features are calculated differently, the model will make wrong predictions on live traffic."],
    ["The system should be easy to use.",
     "The detector shall start with a single command and print results as simple text lines (\"ok\" or \"ALERT\").",
     "Modify. \"Easy to use\" was vague. The refined version says how, but a dashboard is still needed later."],
], [4.6, 6.0, 6.0])

d.add_heading("Part B: Gap Analysis Record", level=1)
para(d, "I chose the function label_flows(flows, attack_log). It decides the correct label (normal or an attack name) "
        "for every recorded flow. If this function is wrong, the whole model learns wrong answers, so it is important "
        "to find its gaps before writing it.")
table(d, ["Function", "Boundary gaps", "Error path gaps", "Domain constraint gaps"], [
    ["label_flows(flows, attack_log)",
     ["1. What happens to a flow that starts exactly at the start or end time of an attack?",
      "2. What happens if the attack log is empty, meaning no attacks happened in that session?",
      "3. What happens if two attack time windows overlap?",
      "4. What happens to a flow that starts a few seconds before an attack and continues into it?",
      "5. What happens to a flow that starts inside an attack window but comes from a different IP address?"],
     ["1. What happens if the attack log file is missing or a column name is wrong?",
      "2. What happens if the clocks of the two virtual machines are not in sync?",
      "3. What happens if an attack command fails silently, so its time window contains no attack flows?",
      "4. What happens if the capture stopped early and some flows are missing?",
      "5. What happens if the flow CSV file has empty or broken rows?"],
     ["1. Which IP address belongs to the attacker? Is it always 10.10.10.1?",
      "2. How much extra time should be allowed around each attack window?",
      "3. Should reply flows that start from the victim's side be labelled as attacks?",
      "4. Should normal traffic from the attacker's IP during an attack window count as an attack?",
      "5. How long must the silent gap between two parts of a session be?"]],
], [3.3, 4.5, 4.5, 4.3], font=10)

d.add_heading("Part C: Structured Prompt", level=1)
para(d, "Below is the code generated from the six-element prompt (the full prompt is in Part E). Each element is marked in the comments.")
code(d, r'''
# ============================================================
# Element 3: Field Specification
# ============================================================
# flows      : table (pandas DataFrame) with one row per flow.
#              Needed columns: src_ip, bidirectional_first_seen_ms
# attack_log : table with one row per attack.
#              Columns: label, start_ms, end_ms
#              (times are in milliseconds since 1970)
import numpy as np
import pandas as pd

ATTACKER = "10.10.10.1"   # fixed IP of the attacker VM
MARGIN_MS = 5000          # 5 seconds of extra time around each attack

# ============================================================
# Element 1: Signature
# ============================================================
# label_flows(flows, attack_log) -> numpy array of labels
#
# Input:
#   flows      -> all flows recorded in one session
#   attack_log -> start and end time of every attack in that session
# Output:
#   one label per flow: "normal", "scan", "bruteforce" or "synflood"

# ============================================================
# Element 2: Business Rules
# ============================================================
# 1. Every flow is "normal" unless a rule below says otherwise.
# 2. A flow gets an attack's label only if:
#      - it comes from the attacker's IP, AND
#      - it starts between (attack start - 5 s) and (attack end + 5 s).
# 3. The labels are returned in the same order as the flows.

# ============================================================
# Element 4: Error Conditions
# ============================================================
def label_flows(flows, attack_log):
    # Check 1: the needed columns must exist
    for col in ("src_ip", "bidirectional_first_seen_ms"):
        if col not in flows.columns:
            raise ValueError("flows table is missing column: " + col)
    for col in ("label", "start_ms", "end_ms"):
        if col not in attack_log.columns:
            raise ValueError("attack log is missing column: " + col)

    # Start with every flow marked as normal
    labels = np.array(["normal"] * len(flows), dtype=object)

    # Check 2: an empty attack log simply means "no attacks"
    if len(attack_log) == 0:
        return labels

    # Give each flow the label of the attack window it falls into
    for _, attack in attack_log.iterrows():
        inside = ((flows.src_ip == ATTACKER) &
                  (flows.bidirectional_first_seen_ms >= attack.start_ms - MARGIN_MS) &
                  (flows.bidirectional_first_seen_ms <= attack.end_ms + MARGIN_MS)).values
        labels[inside] = attack.label
    return labels

# ============================================================
# Element 5: Edge Cases
# ============================================================
# Tested through main():
# 1. A flow from the attacker inside the scan window  -> "scan"
# 2. A flow from the attacker outside every window    -> "normal"
# 3. A flow from another IP inside an attack window   -> "normal"
# 4. A flow starting 3 s before an attack (in margin) -> attack label
# 5. An empty attack log                              -> all "normal"

# ============================================================
# Element 6: Exclusions
# ============================================================
# This function does NOT:
# - fix clock differences between the two virtual machines
# - handle overlapping attack windows (our sessions have 20 s gaps)
# - label reply flows that start from the victim's side
# - read files from disk (the caller passes ready tables)
# - decide which attacks to run

# ============================================================
# MAIN FUNCTION
# ============================================================
def main():
    flows = pd.DataFrame({
        "src_ip": ["10.10.10.1", "10.10.10.1", "10.10.10.2", "10.10.10.1"],
        "bidirectional_first_seen_ms": [10_000, 60_000, 10_500, 7_000],
    })
    log = pd.DataFrame({"label": ["scan"], "start_ms": [10_000], "end_ms": [11_000]})
    print(label_flows(flows, log))    # ['scan' 'normal' 'normal' 'scan']
    empty = pd.DataFrame(columns=["label", "start_ms", "end_ms"])
    print(label_flows(flows, empty))  # all 'normal'

main()
''')

d.add_heading("Part D: Audit Table", level=1)
table(d, ["Function", "Gaps from Part B", "Elements 1-6 added", "Silent decisions remaining", "One change for next generation"], [
    ["label_flows()",
     "Flows at the exact edge of an attack window, flows from other IPs, empty attack log.",
     "Signature, business rules, field specification, error conditions, edge cases and exclusions were all written down.",
     "The attacker's IP (10.10.10.1) and the 5-second margin are fixed values chosen by us.",
     "Read the attacker IP and the margin from a settings file instead of fixing them in the code."],
    ["",
     "Clock differences between the two virtual machines.",
     "Not handled in the code. Instead, we checked that both clocks were synchronised and left 20 seconds of silence between parts.",
     "We assume the clock difference is always smaller than 5 seconds.",
     "Measure the clock difference at the start of every session and store it."],
    ["",
     "Reply flows that start from the victim's side (seen once in the live test).",
     "Placed in the exclusions instead of being silently decided.",
     "These flows are currently labelled normal, even when they belong to an attack.",
     "Decide and write down a rule for reply flows before the next version."],
], [2.6, 3.5, 3.6, 3.5, 3.4], font=10)
para(d, "Note: the version of features.py running in our lab uses the same rules, but it does not yet include the two column checks shown in Part C.", italic=True)

d.add_heading("Part E: Complete Prompt Record", level=1)
table(d, ["FIELD", "CONTENT"], [
    ["FUNCTION", "label_flows(flows, attack_log)"],
    ["PROMPT SUBMITTED",
     "[ELEMENT 1 — SIGNATURE] Write label_flows(flows, attack_log) that returns one label per flow. "
     "[ELEMENT 2 — BUSINESS RULES] Every flow is normal by default. A flow gets an attack's label only if it comes from the attacker's IP (10.10.10.1) and starts within 5 seconds before or after that attack's start and end time. Keep the same order as the input. "
     "[ELEMENT 3 — FIELD SPECIFICATION] flows: src_ip, bidirectional_first_seen_ms. attack_log: label, start_ms, end_ms. Times are in milliseconds. "
     "[ELEMENT 4 — ERROR CONDITIONS] Raise a clear error if a needed column is missing. Return all normal if the attack log is empty. "
     "[ELEMENT 5 — EDGE CASES] Flow inside a window, flow outside all windows, flow from another IP inside a window, flow inside the 5-second margin, empty log. "
     "[ELEMENT 6 — EXCLUSIONS] Do not fix clock differences, do not handle overlapping windows, do not label reply flows from the victim, do not read files."],
    ["GENERATED OUTPUT",
     "Python code containing the constants ATTACKER and MARGIN_MS, the label_flows() function with column checks and an empty-log check, and a main() function that shows the edge cases."],
    ["SILENT DECISIONS IDENTIFIED",
     ["1. The attacker always has the IP 10.10.10.1.",
      "2. A 5-second margin is enough to cover small timing differences.",
      "3. Only the start time of a flow is used, not its end time.",
      "4. Reply flows that start from the victim are labelled normal.",
      "5. If two windows overlap, the later attack in the log wins."]],
    ["DECISION FOR EACH",
     ["1. ACCEPTED for our lab, because the IP is fixed in our setup.",
      "2. ACCEPTED, because our clocks were synchronised and the 20-second gaps make it safe.",
      "3. ACCEPTED, because a flow belongs to the attack during which it started.",
      "4. NEEDS REVISION. We saw one such flow in the live test.",
      "5. ACCEPTED for now, because our sessions never have overlapping attacks."]],
    ["TIMESTAMP", "13-11-2026"],
], [4.2, 12.4], font=10)

d.save("lab2_01fe24bci006_cybersentinel.docx")
print("Lab 2 written")

# =====================================================================
# LAB 3
# =====================================================================
d = new_doc("Lab 3: Software Architecture")

d.add_heading("Part A: Comparing Architecture Options", level=1)
para(d, "CyberSentinel takes live network packets, turns them into flows, calculates features, asks a trained model, and prints an alert. "
        "I compared three architectures that could organise this work.")
d.add_heading("A1. The three options", level=2)
table(d, ["Architecture", "High-level structure", "Advantages", "Limitations"], [
    ["Pipe-and-Filter (pipeline)",
     "The work is split into stages joined in a line. Each stage takes data from the previous stage, does one job, and passes the result on: capture → features → model → alert.",
     "Each stage has one clear job. A stage can be changed or tested on its own. The same stages can be reused for training and for live detection.",
     "If one stage is slow, the whole line waits. Sharing information across many flows (such as the 10-second pattern) needs a small memory inside one stage."],
    ["Layered Architecture",
     "The program is divided into layers placed on top of each other, for example a presentation layer, a logic layer and a data layer. Each layer only talks to the layer below it.",
     "Clear separation of the user interface, the logic and the data. Well known and easy to explain.",
     "Our system is a flow of data, not a set of screens and database tables. Forcing it into layers adds structure that does not match the work."],
    ["Microservices",
     "Each part (capture, features, model, alerts) runs as a separate small program, and the parts talk to each other over the network.",
     "Each part can be deployed and scaled separately. A failure in one part does not stop the others.",
     "Too heavy for one laptop. It adds network delay between the parts, needs extra setup, and makes it harder to keep the features the same in training and live use."],
], [3.2, 4.6, 4.4, 4.4], font=10)

d.add_heading("A2. Comparison against our needs", level=2)
table(d, ["Criterion", "Pipe-and-Filter", "Layered", "Microservices"], [
    ["Maintainability", "High – each stage is a small file with one job.", "Medium – the layers do not match the stages of our work.", "Medium – many small programs to keep in step."],
    ["Ease of testing", "High – each stage can be tested with sample data.", "Medium – layers can be tested, but the data flow crosses all of them.", "Low – testing needs several programs running together."],
    ["Same features in training and live use", "High – the feature stage is one shared file used by both.", "Medium – possible, but not encouraged by the structure.", "Low – training and live parts can drift apart."],
    ["Speed for live detection", "High – everything runs inside one program, with no network calls between stages.", "High – one program.", "Low – every stage adds a network call."],
    ["Suitability for CyberSentinel", "High – our problem is naturally a line of steps.", "Medium – works, but the fit is weak.", "Low – the system is too small for this."],
    ["Implementation complexity", "Low – a few Python files.", "Medium – needs layer rules.", "High – needs separate programs, messaging and deployment."],
], [3.6, 4.4, 4.3, 4.3], font=10)

d.add_heading("A3. Decision", level=2)
table(d, ["Architecture", "Why it was considered", "Selected / Not selected", "Reason or limitation for CyberSentinel"], [
    ["Pipe-and-Filter", "Our system is a line of steps from packets to alerts.", "Selected",
     "It matches the work, keeps every stage simple, and lets training and live detection share the same stages. The limitation is that a slow stage slows everything, which we saw with prediction speed in the slow VM."],
    ["Layered", "It is the most common style and gives clear separation.", "Not selected", "The layers do not match a data pipeline, so it would add structure without benefit."],
    ["Microservices", "It allows each part to run and scale separately.", "Not selected", "Too heavy for one laptop, slower because of network calls, and risky for keeping features the same."],
], [3.2, 4.0, 2.6, 6.8], font=10)

d.add_heading("Part B: Structured Architecture Prompt", level=1)
para(d, "ARCHITECTURE PROMPT — CyberSentinel AI (Live Network Intrusion Detection)", bold=True)
para(d, "You are a software architect. Design the architecture of CyberSentinel using the eight elements below. "
        "The selected architecture is Pipe-and-Filter. Follow all eight elements exactly.")

d.add_heading("[ELEMENT 1 — SYSTEM SCOPE AND TECHNOLOGY STACK]", level=3)
para(d, "CyberSentinel is a network intrusion detection system that:")
bullets(d, ["captures live packets from a network card and groups them into flows",
            "records labelled flows to build its own training data",
            "trains a model to tell normal traffic from attacks",
            "classifies live flows and prints alerts"])
para(d, "Use the following technology stack:")
bullets(d, ["Python 3.12 on Linux Mint 22.2", "NFStream 6.6 for capturing packets and building flows",
            "pandas for tables", "XGBoost for the model and scikit-learn for measuring results",
            "VirtualBox with two virtual machines joined by a private Internal Network called labnet"])

d.add_heading("[ELEMENT 2 — PIPELINE STAGES AND RESPONSIBILITY]", level=3)
para(d, "Use Pipe-and-Filter as the main architecture, with these stages:")
bullets(d, ["Capture – reads packets from the network card and builds flows (NFStream).",
            "Features – turns each flow into 22 numbers, including the 10-second pattern features.",
            "Labelling – used only during training; gives each recorded flow its correct label.",
            "Model – trained once from labelled data, then used to predict.",
            "Alert – prints \"ok\" for normal flows and \"ALERT\" for attacks."])

d.add_heading("[ELEMENT 3 — STAGE ACCESS RULES]", level=3)
bullets(d, ["Data moves only forward: Capture → Features → Model → Alert.",
            "A stage receives data only from the stage before it.",
            "No stage may skip the Features stage.",
            "The Labelling stage is used only during training, never during live detection.",
            "The Model stage must not read packets directly."])

d.add_heading("[ELEMENT 4 — CROSS-CUTTING CONCERNS]", level=3)
bullets(d, ["The feature code is written once in features.py and shared by training and live detection.",
            "The same capture settings (5-second idle timeout, 30-second active timeout) are used in training and live use.",
            "Settings such as the network card name are passed on the command line.",
            "Live capture needs administrator rights (sudo).",
            "Alerts are limited to one line every 3 seconds per attacker and attack type, so the screen is not flooded."])

d.add_heading("[ELEMENT 5 — KEY COMPONENT PLACEMENT]", level=3)
bullets(d, ["capture.py – records flows into a CSV file (data collection).",
            "features.py – feature list, 10-second pattern tracker, and labelling rules.",
            "train.py – trains on round 1, tests on round 2, saves the model.",
            "detect.py – the live detector.",
            "model.json and classes.json – the saved model.",
            "data/ – recorded flows and attack time logs.",
            "Attacker VM: run_round.sh and run_normal.sh – produce normal traffic and attacks."])

d.add_heading("[ELEMENT 6 — REQUIREMENT OWNERSHIP]", level=3)
para(d, "Map each functional requirement from Lab 2 to the stage that owns it:")
table(d, ["Requirement", "Owning stage"], [
    ["FR1 – Capture live packets and build flows", "Capture (NFStream)"],
    ["FR2 – Classify each flow into one of four classes", "Model"],
    ["FR3 – Print alerts with time, type, IP and flow count", "Alert"],
    ["FR4 – Save captured flows to CSV", "Capture (capture.py)"],
    ["FR5 – Label flows automatically from the attack log", "Labelling (features.py)"],
    ["FR6 – Train on one session and test on another", "Model (train.py)"],
], [10.0, 6.6], font=10)

d.add_heading("[ELEMENT 7 — EXPLICIT EXCLUSIONS]", level=3)
para(d, "Do not:")
bullets(d, ["split the stages into separate programs or microservices",
            "calculate features in two different places",
            "use a downloaded dataset as the training data",
            "send any attack traffic outside the private lab network",
            "block or drop traffic (the system only detects and alerts)",
            "add a database or a web dashboard in this version"])

d.add_heading("[ELEMENT 8 — REQUIRED OUTPUT]", level=3)
para(d, "Generate only:")
bullets(d, ["the architecture style", "a high-level diagram of the pipeline and the lab",
            "the file and component structure", "the responsibility of each stage",
            "the requirement-to-stage mapping", "important assumptions, if any"])
para(d, "Do not generate: full code, test cases or installation scripts.")

d.add_heading("Part C: Comparing My Choice with the AI-Generated Architecture", level=1)
table(d, ["Aspect", "Architecture selected in Part A", "AI-generated architecture", "Difference / Observation"], [
    ["Architecture structure", "Pipe-and-Filter", "Pipe-and-Filter", "Same choice."],
    ["Main stages", "Capture, Features, Model, Alert", "Capture, Features, Labelling, Model, Alert",
     "The AI made Labelling a separate stage used only during training."],
    ["Responsibilities", "Each stage does one job.", "Same, and it also placed the labelling rules in the shared features.py file.",
     "Keeping labels and features in one file made them easier to keep consistent."],
    ["Interaction / communication", "Data moves forward from one stage to the next.",
     "Same, plus a small memory inside the Features stage that remembers the last 10 seconds of flows for each IP.",
     "This memory was needed for the pattern features that catch port scans."],
    ["Lab environment", "Not decided in Part A.", "Two virtual machines (attacker and victim) on a private network inside one laptop.",
     "The AI added a safe and legal way to create labelled attack traffic."],
    ["Overall difference", "—", "—", "No change in the architecture style. The AI added more detail inside the stages."],
], [3.0, 4.0, 4.8, 4.8], font=10)

d.add_heading("Part D: Architecture Decision Record", level=1)
table(d, ["Field", "Content"], [
    ["ID and Title", "ADR-001: Use a Pipe-and-Filter pipeline with one shared feature module for CyberSentinel"],
    ["Status", "Accepted"],
    ["Context",
     ["CyberSentinel must read live traffic and predict attacks. The work is naturally a line of steps: capture packets, build flows, calculate features, predict, and alert.",
      "Research shows that a model trained on features from one tool does not work well on features from a different tool. So training and live detection must calculate features in exactly the same way."]],
    ["Decision",
     ["We use the Pipe-and-Filter architecture inside a single Python program.",
      "The stages are Capture (NFStream), Features (features.py), Model (XGBoost) and Alert.",
      "The feature code lives in one shared file, features.py, which is used by both train.py and detect.py."]],
    ["Consequences",
     ["Easier: each stage is small and can be tested alone; training and live features always match; everything runs on one laptop.",
      "Harder: a slow stage slows the whole line; in our slow virtual machine, predicting each flow took about 60 ms.",
      "Impossible: calculating features differently for training and for live detection, or running the stages as separate services in this version."]],
    ["Review Trigger",
     "Review this decision if the system must watch a much busier network, if one stage needs to run on a different machine, or if prediction speed becomes too slow for real-time alerts."],
], [3.6, 13.0], font=11)

d.add_heading("Part E: Architecture Review Record", level=1)
table(d, ["RR Section", "What to record"], [
    ["1. Architecture version",
     ["System: CyberSentinel AI – Live Network Intrusion Detection", "Architecture: Pipe-and-Filter", "Version: v1.0",
      "Generation date: " + DATE, "Prompt reference: CyberSentinel Architecture Prompt (Part B)"]],
    ["2. Architecture prompt", "The full eight-element prompt is written in Part B of this document."],
    ["3. Generated architecture",
     ["Architecture: Pipe-and-Filter, running as one Python program on the victim virtual machine.",
      "Stages: Capture (NFStream) → Features (features.py) → Model (XGBoost) → Alert. Labelling is used only during training.",
      "Files: capture.py, features.py, train.py, detect.py, model.json, classes.json and the data/ folder.",
      "Lab: an attacker VM (10.10.10.1) and a victim VM (10.10.10.2) joined by the private network labnet inside one laptop.",
      "Key rules: data moves only forward; features are calculated in one shared file; no attack traffic leaves the private network."]],
    ["4. Decision",
     ["Approved. The generated architecture follows the selected Pipe-and-Filter style and adds a safe lab and a shared feature file. "
      "It was built and tested: the model reached 99.8% on an unseen test session, and the live detector raised the correct alerts for all three attacks.",
      "Timestamp: " + DATE]],
], [4.0, 12.6], font=10)

d.add_heading("Diagram of the architecture", level=2)
code(d, r'''
One laptop (Windows 11 + VirtualBox)

Attacker VM (10.10.10.1)              Victim + detector VM (10.10.10.2)
normal traffic, nmap,     labnet      SSH server, Apache web server
hydra, hping3          ------------>          |
                                              v
          Capture    ->   Features     ->   Model     ->   Alert
         (NFStream)     (features.py)     (XGBoost)     ("ok" / "ALERT")
''')

d.save("lab3_01fe24bci006_cybersentinel.docx")
print("Lab 3 written")
