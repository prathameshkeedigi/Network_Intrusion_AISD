"""Builds the filled SRS for CyberSentinel AI (new file; the template is left untouched)."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
DATE = "13 November 2026"

d = Document()
for s in d.sections:
    s.page_width, s.page_height = Cm(21.59), Cm(27.94)
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(2.54)
st = d.styles["Normal"]
st.font.name, st.font.size = FONT, Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.space_after = Pt(6)
for name, size in (("Heading 1", 15), ("Heading 2", 13), ("Heading 3", 12)):
    h = d.styles[name]
    h.font.name, h.font.size, h.font.bold = FONT, Pt(size), True
    h.font.color.rgb = RGBColor(0x1F, 0x2A, 0x44)
    rf = h.element.rPr.rFonts
    rf.set(qn("w:eastAsia"), FONT)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def table(header, rows, widths, font=10.5):
    tb = d.add_table(rows=1, cols=len(header))
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(header):
        c = tb.rows[0].cells[i]
        c.text = hd
        c.paragraphs[0].runs[0].bold = True
        shade(c, "D9E2EC")
    for r in rows:
        cells = tb.add_row().cells
        for i, v in enumerate(r):
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
    trPr = tb.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
    tb.autofit = False
    for row in tb.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    d.add_paragraph()


def para(text, bold=False, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text); r.bold, r.italic = bold, italic
    return p


def bullets(items):
    for it in items:
        d.add_paragraph(it, style="List Bullet")


def code(text):
    for line in text.strip("\n").split("\n"):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line if line else " ")
        r.font.name = "Courier New"; r.font.size = Pt(9)
        r.element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
    d.add_paragraph()


H1 = lambda t: d.add_heading(t, level=1)
H2 = lambda t: d.add_heading(t, level=2)
H3 = lambda t: d.add_heading(t, level=3)

# ---------------- Title page ----------------
for _ in range(4):
    d.add_paragraph()
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Software Requirements Specification (SRS)"); r.bold = True; r.font.size = Pt(22)
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CyberSentinel AI – Live Network Intrusion Detection"); r.bold = True; r.font.size = Pt(16)
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Version 1.0  |  " + DATE).italic = True
d.add_paragraph()
info = d.add_table(rows=0, cols=2); info.style = "Table Grid"; info.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in (("Course", "AI-Assisted Software Development (AISD)"), ("Team", "Team 10"),
             ("Members", "Bachu Venkata Siva Jaideep (01fe24bci084), Nilaksha Nath (01fe24bci087), Sunayana Kamath (01fe24bci073), Prathamesh K Eedigi (01fe24bci006)"),
             ("Status", "Version 1.0 built and tested in a virtual lab")):
    c = info.add_row().cells
    c[0].text, c[1].text = k, v
    c[0].paragraphs[0].runs[0].bold = True
    shade(c[0], "E8EEF5")
info.autofit = False
for row in info.rows:
    row.cells[0].width, row.cells[1].width = Cm(3.5), Cm(12.5)
d.add_page_break()

# ---------------- Contents ----------------
H1("Table of Contents")
for line in ["1. Introduction", "    1.1 Purpose", "    1.2 Document Conventions", "    1.3 Intended Audience and Reading Suggestions",
             "    1.4 Product Scope", "    1.5 Definitions, Acronyms and Abbreviations",
             "2. Overall Description", "    2.1 Product Perspective", "    2.2 Product Functions", "    2.3 User Classes and Characteristics",
             "    2.4 Operating Environment", "    2.5 Design and Implementation Constraints", "    2.6 User Documentation", "    2.7 Assumptions and Dependencies",
             "3. External Interface Requirements", "    3.1 User Interfaces", "    3.2 Hardware Interfaces", "    3.3 Software Interfaces", "    3.4 Communications Interfaces",
             "4. System Features and Functional Requirements", "    4.1 Live Flow Capture", "    4.2 Labelled Dataset Creation", "    4.3 Model Training and Testing",
             "    4.4 Live Attack Detection and Alerts", "    4.5 Use Cases",
             "5. Non-Functional Requirements", "    5.1 Performance Requirements", "    5.2 Safety Requirements", "    5.3 Security Requirements",
             "    5.4 Software Quality Attributes", "    5.5 Business Rules and Compliance",
             "6. Appendix", "    Appendix A: Glossary", "    Appendix B: Analysis Models", "    Appendix C: Requirements Traceability Matrix"]:
    q = d.add_paragraph(line); q.paragraph_format.space_after = Pt(1)
d.add_page_break()

# ---------------- 1. Introduction ----------------
H1("1. Introduction")
H2("1.1 Purpose")
para("This document describes what CyberSentinel AI version 1.0 must do and how well it must do it. CyberSentinel AI is a network "
     "intrusion detection system: a program that watches network traffic as it happens and raises an alert when it sees an attack.")
para("The document is written for our project guide, who reviews the project, and for our team, who build and test it. "
     "It is used as the agreed list of requirements, as the basis for design decisions, and as the checklist for testing.")

H2("1.2 Document Conventions")
bullets(["\"Shall\" means the requirement is mandatory. \"Should\" means it is desirable but not mandatory.",
         "Functional requirements are numbered FR-1, FR-2 and so on. Non-functional requirements are numbered NFR-1, NFR-2 and so on.",
         "Each feature has a priority: High (needed for the core goal), Medium (important but not core) or Low (nice to have).",
         "File names, commands and code are written in plain names such as detect.py.",
         "Measured results are taken from our own test runs in the lab and are marked as \"measured\"."])

H2("1.3 Intended Audience and Reading Suggestions")
table(["Reader", "What they need", "Suggested sections"], [
    ["Project guide / evaluator", "What the system does, how it was tested, and its limits", "1.4, 2.1, 2.2, 4, 5.1, Appendix C"],
    ["Team members (developers)", "Every detail needed to build or change the system", "All sections"],
    ["Testers", "What to check and the expected results", "4, 5, Appendix C"],
    ["A new reader with no networking background", "The basic terms first", "1.5 and Appendix A first, then 1.4 and 2"],
], [4.8, 6.5, 4.7])

H2("1.4 Product Scope")
para("Product name: CyberSentinel AI, version 1.0.", bold=True)
para("Main goal: detect network attacks on live traffic and predict, for every connection, whether it is normal or an attack.")
para("Why it is needed: tools like Wireshark show live packets but do not say whether they are attacks. Many student projects train "
     "a model on a downloaded dataset such as CIC-IDS2017, but research shows that such models perform close to random on a "
     "different network, and that more than 20% of CIC-IDS2017 traffic had errors. CyberSentinel instead trains on traffic that "
     "we capture and label ourselves in a safe lab, using the same code that later watches live traffic.")
para("Benefits:")
bullets(["Works on live traffic, not only on a stored file.",
         "Training data and live data are processed by the same code, so they match.",
         "All testing is safe and legal, because attacks never leave the laptop.",
         "Each alert is printed with the attack type and the attacker's address."])
para("What is inside the scope of version 1.0:")
bullets(["Capturing live packets and grouping them into flows.",
         "Creating a labelled dataset in a lab of two virtual machines.",
         "Training and testing a model that recognises four classes: normal, port scan, brute force (password guessing) and SYN flood.",
         "Printing live results as \"ok\" or \"ALERT\" lines in a terminal."])
para("What is outside the scope of version 1.0:")
bullets(["Blocking or stopping attacks. The system only detects and reports.",
         "A graphical dashboard (planned for a later version).",
         "Other attack types, such as web attacks or slow denial-of-service attacks.",
         "Reading the contents of encrypted traffic.",
         "Monitoring the hostel, college or any network we do not own."])

H2("1.5 Definitions, Acronyms and Abbreviations")
para("Longer explanations of these and other terms are in Appendix A.")
table(["Term", "Meaning"], [
    ["IDS / NIDS", "Intrusion Detection System / Network Intrusion Detection System: software that watches traffic and reports attacks."],
    ["IP address", "The address of a computer on a network, for example 10.10.10.2."],
    ["Port", "A numbered \"door\" on a computer. Each service listens on its own port, for example port 22 for SSH and port 80 for web pages."],
    ["TCP / UDP", "The two main ways computers send data. TCP sets up a conversation first; UDP just sends."],
    ["SYN, ACK, RST, FIN", "Control messages in TCP. SYN = \"hello, can we talk?\", ACK = \"received\", RST = \"refused\", FIN = \"goodbye\"."],
    ["SSH", "Secure Shell: a service for logging in to a computer remotely with a username and password."],
    ["HTTP", "The protocol used to request and send web pages."],
    ["DNS", "Domain Name System: turns a name like google.com into an IP address."],
    ["VM", "Virtual Machine: a complete computer that runs as a program inside another computer."],
    ["NAT", "Network Address Translation: lets a VM reach the internet through the laptop's own connection."],
    ["labnet", "The private network (VirtualBox \"Internal Network\") that connects our two VMs only."],
    ["DoS", "Denial of Service: an attack that overloads a service so real users cannot use it."],
    ["CSV", "Comma-Separated Values: a simple table stored as a text file."],
    ["ML", "Machine Learning: programs that learn patterns from examples."],
    ["XGBoost", "A machine learning method that combines many small decision trees."],
    ["FR / NFR", "Functional Requirement / Non-Functional Requirement."],
    ["RTM", "Requirements Traceability Matrix: a table linking each requirement to its design and test."],
], [3.6, 12.4])

# ---------------- 2. Overall description ----------------
H1("2. Overall Description")
H2("2.1 Product Perspective")
para("CyberSentinel AI is a new, self-contained system. It is not part of a larger product. It is different from two kinds of existing tools:")
bullets(["Packet viewers such as Wireshark only show packets. CyberSentinel decides whether each conversation is an attack.",
         "Projects trained on public datasets learn from someone else's traffic. CyberSentinel learns from traffic captured in its own lab by the same capture code it uses live."])
para("The system runs inside a lab built on one laptop:")
bullets(["Attacker VM (IP 10.10.10.1): produces normal traffic and the three attacks.",
         "Victim and detector VM (IP 10.10.10.2): runs the services that are attacked (SSH and a web server) and the CyberSentinel detector.",
         "labnet: a private network inside the laptop that connects only these two VMs.",
         "Each VM also has a NAT connection to the internet, used only to install software and to log in from Windows. No attack uses it."])
para("A diagram of the lab and the pipeline is in Appendix B.")

H2("2.2 Product Functions")
table(["#", "Function", "Short description"], [
    ["F1", "Live flow capture", "Reads packets from a network card and groups them into flows (conversations)."],
    ["F2", "Labelled dataset creation", "Runs scripted normal traffic and attacks, records the exact attack times, and labels every flow automatically."],
    ["F3", "Model training and testing", "Calculates 22 numbers per flow, trains an XGBoost model on one session, and tests it on another."],
    ["F4", "Live detection and alerts", "Classifies every live flow and prints \"ok\" or an alert with the attack type."],
], [1.2, 4.3, 10.5])

H2("2.3 User Classes and Characteristics")
table(["User class", "What they do", "Skill needed", "How often", "Permissions"], [
    ["Operator (security analyst)", "Starts the detector and reads the alerts.", "Basic Linux terminal use.", "Whenever the network is monitored; during every demo.", "Needs administrator (sudo) rights to capture packets."],
    ["Developer / researcher (our team)", "Collects new data, retrains the model and changes the code.", "Python, basic networking.", "When adding attacks or improving the model.", "Full access to both VMs."],
    ["Evaluator (project guide)", "Watches the demo and reviews the results.", "None required.", "At reviews.", "No access needed."],
], [3.3, 3.8, 2.8, 3.1, 3.0], font=10)

H2("2.4 Operating Environment")
table(["Item", "What we used (verified on our setup)"], [
    ["Host computer", "Windows 11 laptop, AMD Ryzen 7 7435HS processor (8 cores, 16 threads), 16 GB RAM"],
    ["Virtualisation", "Oracle VirtualBox 7.2.4"],
    ["Victim and detector VM", "Linux Mint 22.2 (based on Ubuntu 24.04), 4 GB RAM, 4 CPUs, two network cards: enp0s3 (NAT) and enp0s8 (labnet)"],
    ["Attacker VM", "Linked clone of the Mint VM, 2 GB RAM, hostname \"attacker\""],
    ["Detector software", "Python 3.12.3, NFStream 6.6.0, pandas, XGBoost (CPU version), scikit-learn"],
    ["Victim services", "OpenSSH server and Apache2 web server"],
    ["Attack and traffic tools", "nmap, hydra, hping3, curl, sshpass"],
    ["Browser", "Not needed. All results are shown in a terminal."],
], [4.3, 11.7])
para("Note: on our laptop, VirtualBox runs in a slower mode because Windows' own hypervisor (Hyper-V) is active. This makes the VMs slower but does not change the results.", italic=True)

H2("2.5 Design and Implementation Constraints")
bullets(["The detector shall be written in Python and run on Linux, because live capture with NFStream is reliable on Linux.",
         "Live capture needs administrator rights (sudo).",
         "Training and live detection shall use the same feature code (features.py) and the same capture settings.",
         "Data is stored in CSV files. Version 1.0 does not use a database.",
         "Attacks may only be run on the private network labnet, on machines we own.",
         "Everything must run on one laptop with 16 GB RAM, so the two VMs together use about 6 GB.",
         "A flow can only be judged after it ends (5 seconds without packets, or 30 seconds of continuous activity), so alerts can never be instant."])

H2("2.6 User Documentation")
table(["Document", "Purpose", "Status"], [
    ["DEMO_COMMANDS.md", "Step-by-step commands for the live demo, with what each command does and how to fix common problems", "Delivered"],
    ["PRESENTATION_SCRIPT.md", "A spoken explanation of the project in simple English, slide by slide", "Delivered"],
    ["Claude_sessions.md", "A dated log of the work done in each working session", "Delivered"],
    ["Lab 2 and Lab 3 documents", "Requirements engineering and architecture decisions (including ADR-001)", "Delivered"],
    ["Comments in capture.py, features.py, train.py, detect.py", "Explain what each part of the code does", "Delivered"],
    ["Installation guide", "How to build the lab from scratch on a new laptop", "Planned"],
], [5.0, 8.5, 2.5])

H2("2.7 Assumptions and Dependencies")
bullets(["The NFStream library and the system's packet capture support work correctly on Linux Mint.",
         "The clocks of the two VMs are synchronised (checked with timedatectl), so attack times written on the attacker match flow times recorded on the victim.",
         "The attacker always uses the IP address 10.10.10.1.",
         "Some other traffic is present on the network during live detection. Without it, finished flows may wait before they are reported.",
         "The SSH and web services on the victim are running.",
         "The normal traffic produced by our script (web page visits and SSH logins with pauses) represents normal use well enough for this version. Real users are more varied, which is a known limitation."])

# ---------------- 3. External interfaces ----------------
H1("3. External Interface Requirements")
H2("3.1 User Interfaces")
para("Version 1.0 has a text interface in a Linux terminal. There is no graphical screen.")
table(["Screen output", "Format (from detect.py)", "Example"], [
    ["Start message", "Network card being watched and the list of classes", "CyberSentinel live detector on enp0s8 | classes: ['bruteforce', 'normal', 'scan', 'synflood']"],
    ["Normal flow", "time, \"ok\", source -> destination:port, confidence", "10:12:49  ok  10.10.10.1 -> 10.10.10.2:80  (1.00)"],
    ["Attack alert", "time, [ALERT], attack type, source -> destination, number of flows since the last alert, confidence, different ports touched in the last 10 seconds", "10:16:39  [ALERT] SCAN from 10.10.10.1 -> 10.10.10.2 (+285 flows, confidence 1.00, ports in last 10 s: 285)"],
    ["Summary on stop (Ctrl+C)", "Number of flows predicted in each class", "{'bruteforce': 11, 'normal': 33, 'scan': 1002, 'synflood': 251}"],
], [3.3, 5.4, 7.3], font=10)
para("To keep the screen readable, an alert line is printed at most once every 3 seconds for the same attacker and attack type. The number of flows in between is shown in the line.")

H2("3.2 Hardware Interfaces")
bullets(["The detector reads packets from the virtual network card enp0s8, which VirtualBox connects to labnet.",
         "The second virtual card, enp0s3, is connected through NAT and is not monitored.",
         "VirtualBox emulates an Intel PRO/1000 (82540EM) network card for these interfaces. No physical hardware other than the laptop is used."])

H2("3.3 Software Interfaces")
table(["Software", "How CyberSentinel uses it"], [
    ["NFStream 6.6.0", "Reads packets from a network card and returns finished flows. Settings used: source = the network card name, statistical_analysis = on, idle_timeout = 5 seconds, active_timeout = 30 seconds."],
    ["pandas", "Reads and writes the CSV files of flows and attack logs."],
    ["XGBoost", "Trains the model and makes predictions. The trained model is saved as model.json and the class names as classes.json."],
    ["scikit-learn", "Calculates the test results (precision, recall, F1 score, confusion matrix) and balances the training data."],
    ["Linux operating system", "Gives access to the network card. Requires administrator rights (sudo)."],
], [3.6, 12.4])
para("Data files used between the programs:")
table(["File", "Content"], [
    ["roundN_flows.csv, normal_extra_flows.csv", "One row per flow with 27 columns: source and destination IP and port, protocol, start, end and duration times, packet and byte counts in both directions, packet size and gap statistics, TCP flag counts, and the application name."],
    ["roundN_attack_log.csv", "One row per attack: label, start_ms, end_ms (times in milliseconds)."],
    ["model.json, classes.json", "The trained model and the list of class names."],
], [5.4, 10.6])

H2("3.4 Communications Interfaces")
bullets(["The detector only listens. It reads copies of packets on enp0s8 and does not send any network traffic itself.",
         "The traffic it watches is IPv4 traffic on labnet (10.10.10.0/24), mainly TCP: SSH on port 22 and HTTP on port 80.",
         "Operators log in to the VMs from Windows over SSH, using VirtualBox port forwarding on 127.0.0.1 (port 2222 for the victim, port 2223 for the attacker). This only works from the laptop itself.",
         "Alerts are printed on the screen only. Version 1.0 does not send alerts by email or over the network."])

# ---------------- 4. Features ----------------
H1("4. System Features and Functional Requirements")


def feature(num, name, desc, prio, stim, frs):
    H2(f"4.{num} {name}")
    H3(f"4.{num}.1 Description and Priority")
    para(desc)
    para("Priority: " + prio, bold=True)
    H3(f"4.{num}.2 Stimulus/Response Sequences")
    table(["Stimulus (what happens)", "Response (what the system does)"], stim, [6.5, 9.5])
    H3(f"4.{num}.3 Functional Requirements")
    table(["ID", "Requirement"], frs, [1.8, 14.2])


feature(1, "Live Flow Capture",
        "The system reads live packets from a network card and groups the packets of each conversation into one flow. This is the base for both data collection and live detection.",
        "High",
        [["The operator starts capture.py with a network card name and an output file.", "The system prints \"Recording on <card>\" and starts reading packets."],
         ["A conversation has no packets for 5 seconds, or has been active for 30 seconds.", "The system closes the flow and writes it as one row in the CSV file."],
         ["Every 100 flows.", "The system prints the number of flows saved so far."],
         ["The operator presses Ctrl+C.", "The system stops and prints the total number of flows saved."]],
        [["FR-1", "The system shall capture live packets from a network card named on the command line."],
         ["FR-2", "The system shall group packets into two-way flows, closing a flow after 5 seconds without packets or after 30 seconds of activity."],
         ["FR-3", "The system shall save each flow as one row of a CSV file with the 27 columns listed in section 3.3, and save each row immediately so that data is not lost if capture stops."],
         ["FR-4", "The system shall print its progress every 100 flows and the total when it stops."]])

feature(2, "Labelled Dataset Creation",
        "The attacker VM runs a scripted session of normal traffic and attacks and records the exact time of every attack. Each recorded flow is then labelled automatically, without manual work.",
        "High",
        [["The developer runs run_round.sh on the attacker VM.", "The script runs 3 minutes of normal traffic, then a port scan, password guessing and a SYN flood, then 2 more minutes of normal traffic, with 20 seconds of silence between parts."],
         ["Each attack starts and ends.", "The script writes the attack name and its start and end time (in milliseconds) to the attack log."],
         ["The training program reads a session's flows and attack log.", "Every flow from the attacker that started inside an attack's time window (plus 5 seconds on each side) gets that attack's label. All other flows are labelled normal."]],
        [["FR-5", "The system shall produce normal traffic made of web page requests and SSH logins with the correct password, separated by random pauses of 1 to 3 seconds."],
         ["FR-6", "The system shall produce three attacks: a port scan of ports 1 to 1000 (nmap), password guessing on SSH (hydra) and a 20-second SYN flood on port 80 (hping3)."],
         ["FR-7", "The system shall record the label, start time and end time of every attack in an attack log."],
         ["FR-8", "The system shall label a flow with an attack's name only if it comes from the attacker's IP address and starts within 5 seconds of that attack's time window; otherwise it shall label it normal."]])

feature(3, "Model Training and Testing",
        "The system turns each flow into 22 numbers, trains a model on one session, and tests it on a different session that the model has never seen.",
        "High",
        [["The developer runs train.py.", "The system loads both rounds and the extra normal traffic, adds features and labels, and prints the number of flows per class."],
         ["Training finishes.", "The system prints precision, recall and F1 score for each class, the confusion matrix and the 8 most useful features."],
         ["Testing finishes.", "The system saves model.json and classes.json."]],
        [["FR-9", "The system shall calculate 22 features for every flow: 20 numbers that describe the flow itself, and 2 pattern numbers (how many flows, and how many different ports, the same source started in the last 10 seconds)."],
         ["FR-10", "The system shall not use IP addresses, port numbers or timestamps as features, so that the model learns behaviour and not addresses."],
         ["FR-11", "The system shall train on round 1 plus the first 70% of the extra normal traffic, and test on round 2 plus the last 30%, without shuffling."],
         ["FR-12", "The system shall print the test results and save the trained model."]])

feature(4, "Live Attack Detection and Alerts",
        "The system reads live traffic, calculates the same 22 features with the same code used in training, and prints \"ok\" or an alert for every finished flow.",
        "High",
        [["The operator starts detect.py with sudo and the network card name.", "The system loads the saved model and prints the start message."],
         ["A normal flow finishes.", "The system prints an \"ok\" line."],
         ["An attack flow finishes.", "The system prints an alert line (at most one every 3 seconds per attacker and attack type)."],
         ["The operator presses Ctrl+C.", "The system prints the number of flows predicted in each class."]],
        [["FR-13", "The system shall load the saved model and classify every finished live flow as normal, scan, bruteforce or synflood."],
         ["FR-14", "The system shall calculate live features with the same features.py code that was used in training."],
         ["FR-15", "The system shall print an alert with the time, attack type, source and destination address, number of flows, confidence and the number of different ports touched in the last 10 seconds."],
         ["FR-16", "The system shall print a summary of predictions per class when it is stopped."]])

H2("4.5 Use Cases")
table(["Item", "UC-1: Record a training session"], [
    ["Actor", "Developer"],
    ["Preconditions", "Both VMs are running; labnet works (the attacker can ping 10.10.10.2); the SSH and web services are running; the VM clocks are synchronised."],
    ["Main steps", ["1. On the victim, start capture.py on enp0s8 with an output file name.",
                    "2. On the attacker, run sudo -v and then run_round.sh with the round number.",
                    "3. Wait until the attacker prints \"ROUND N FINISHED\".",
                    "4. Wait 10 seconds and stop capture.py with Ctrl+C.",
                    "5. Copy the attack log from the attacker to the victim's data folder."]],
    ["Postconditions", "A flows CSV file and an attack log exist for the round."],
    ["Alternative paths", "If capture shows 0 flows, check that enp0s8 has the address 10.10.10.2. If the script stops to ask for a password, type it and the round continues."],
], [3.5, 12.5])
table(["Item", "UC-2: Train and test the model"], [
    ["Actor", "Developer"],
    ["Preconditions", "Round 1, round 2 and the extra normal recording exist in the data folder."],
    ["Main steps", ["1. Run train.py on the victim VM.", "2. Read the label counts, the results per class and the confusion matrix."]],
    ["Postconditions", "model.json and classes.json are saved."],
    ["Alternative paths", "If the xgboost library is missing, install it, then run train.py again."],
], [3.5, 12.5])
table(["Item", "UC-3: Run live detection (demo)"], [
    ["Actor", "Operator"],
    ["Preconditions", "The trained model exists; both VMs are running; the operator is logged in to both."],
    ["Main steps", ["1. On the victim, start detect.py with sudo on enp0s8.",
                    "2. On the attacker, start background normal traffic (run_normal.sh).",
                    "3. On the attacker, run the port scan, then password guessing, then the SYN flood, waiting 20 to 30 seconds between them.",
                    "4. Watch the \"ok\" lines and the alerts on the victim.",
                    "5. Stop the detector with Ctrl+C and read the summary."]],
    ["Postconditions", "Each attack has raised its alert and normal traffic has been marked ok."],
    ["Alternative paths", "If alerts are slow, make sure background normal traffic is running. If SSH from Windows is refused, wait until the VM has fully started."],
], [3.5, 12.5])

# ---------------- 5. NFRs ----------------
H1("5. Non-Functional Requirements")
H2("5.1 Performance Requirements")
table(["ID", "Requirement", "Measured result in our lab"], [
    ["NFR-1", "The system shall correctly classify at least 95% of the flows in a test session that was not used for training.", "Met: 99.8% (2,327 of 2,331 flows correct)."],
    ["NFR-2", "The system shall wrongly flag less than 2% of normal flows as attacks in the test session.", "Met: 3 of 296 normal flows (about 1.0%)."],
    ["NFR-3", "Each attack type shall be detected in at least 95% of its test flows.", "Met: scan 99.9%, SYN flood 100%, brute force 100%."],
    ["NFR-4", "When other traffic is present on the network, the system should print an alert within 10 seconds after an attack flow ends.", "Partly met: alerts came within seconds when background traffic was running. When the network was silent, one scan alert was delayed by about 4 minutes."],
    ["NFR-5", "The system should check each flow quickly enough to keep up with an attack.", "Not yet met in our slow VMs: about 60 ms per flow, so about 1,000 scan flows took about 1 minute to check."],
], [1.6, 8.2, 6.2], font=10)

H2("5.2 Safety Requirements")
bullets(["All attacks shall run only on labnet, which exists only inside the laptop. No attack traffic can reach the hostel, college or internet.",
         "The detector only reads copies of packets. If it crashes, network traffic is not affected.",
         "Captured flows shall be written to disk row by row, so that data recorded before a crash is kept.",
         "VMs should be shut down properly from inside, or their state saved, before the laptop sleeps or shuts down. (On our laptop, the VMs were once found in an \"aborted\" state after the laptop went to sleep.)",
         "Copies of the project scripts are kept on the Windows side (folder cybersentinel_code) as a backup."])

H2("5.3 Security Requirements")
bullets(["Live capture shall require administrator rights (sudo), so ordinary users cannot read network traffic.",
         "The system shall store only flow statistics and the detected application name. It shall not store the contents (payload) of packets.",
         "The test account \"victim\" has a deliberately weak password for the password-guessing attack. It shall exist only inside the lab VMs.",
         "SSH access from Windows to the VMs shall be bound to 127.0.0.1, so it is reachable only from the laptop itself.",
         "User roles, encryption of stored data and login protection such as OAuth2 or MFA are not part of version 1.0, because the system has no user accounts of its own and runs only inside a private lab."])

H2("5.4 Software Quality Attributes")
table(["Attribute", "How CyberSentinel meets it"], [
    ["Maintainability", "The code is split into four small files, each with one job (capture.py, features.py, train.py, detect.py). Features and labelling rules are written once in features.py."],
    ["Testability", "Each stage can be run on its own with sample data. The model is always tested on a separate session."],
    ["Usability", "The detector starts with one command and prints plain text lines. A demo guide lists every command."],
    ["Portability", "Runs on any Linux system that supports NFStream and Python 3.12. Live capture on Windows is not supported in version 1.0."],
    ["Scalability", "Limited. Version 1.0 runs on one machine and checks flows one by one, which is suitable for a lab but not for a busy network."],
    ["Internationalisation", "Not required. All output is in English."],
], [3.6, 12.4])

H2("5.5 Business Rules and Compliance")
bullets(["Information Technology Act, 2000 (India), Sections 43 and 66: accessing or attacking a computer or network without permission is an offence. Rule: we only attack machines we own, on a private network.",
         "Digital Personal Data Protection Act, 2023 (India): network traffic can contain personal data. Rule: we capture only our own lab traffic and store only flow statistics, not packet contents.",
         "GDPR, HIPAA and PCI-DSS do not apply, because the system does not handle personal data of EU residents, health records or card payments.",
         "Labelling rule: a flow is an attack only if it comes from the attacker's IP (10.10.10.1) inside a logged attack window (with 5 seconds of margin).",
         "Data collection rule: 20 seconds of silence between the parts of a session, so labels never overlap."])

# ---------------- 6. Appendix ----------------
H1("6. Appendix")
H2("Appendix A: Glossary")
table(["Term", "Simple explanation"], [
    ["Packet", "A small piece of data sent over a network. One web page needs dozens of packets."],
    ["Flow", "All packets of one conversation between two computers, summarised in one row: who talked to whom, on which port, for how long, and how many packets and bytes."],
    ["Network card (interface)", "The connection between a computer and a network. Our victim VM has enp0s3 (internet) and enp0s8 (lab network)."],
    ["Normal traffic", "Legitimate use: opening web pages and logging in over SSH with the correct password, at a human pace."],
    ["Port scan", "An attacker sends a \"hello\" to many ports (doors) to find which ones are open. It is usually the first step of an attack."],
    ["Brute force (password guessing)", "Trying many passwords one after another until one works."],
    ["SYN flood", "Sending many \"hello\" (SYN) messages without ever finishing the conversation, so the server keeps waiting and real users cannot get through. A type of denial-of-service attack."],
    ["Label", "The correct answer for a flow: normal, scan, bruteforce or synflood."],
    ["Feature", "A number that describes a flow, such as the number of bytes sent. The model makes its decision from 22 features."],
    ["Pattern feature", "A feature that looks across flows: how many flows, and how many different ports, one computer touched in the last 10 seconds."],
    ["Idle timeout", "The time without packets after which a flow is treated as finished (5 seconds in our system)."],
    ["Precision", "Of all flows the model called an attack type, the share that really were that type."],
    ["Recall", "Of all real flows of a type, the share the model found."],
    ["Confusion matrix", "A table where rows are the real labels and columns are the model's guesses. Correct guesses lie on the diagonal."],
    ["False alarm", "A normal flow wrongly flagged as an attack."],
    ["CIC-IDS2017", "A public dataset of labelled network traffic recorded at the University of New Brunswick in 2017."],
], [4.2, 11.8])

H2("Appendix B: Analysis Models")
H3("B.1 Lab and architecture sketch")
code(r'''
One laptop (Windows 11 + VirtualBox)

Attacker VM (10.10.10.1)              Victim + detector VM (10.10.10.2)
normal traffic, nmap,     labnet      SSH server (port 22), Apache (port 80)
hydra, hping3          ------------>          |
                                              v
          Capture    ->   Features     ->   Model     ->   Alert
         (NFStream)     (features.py)     (XGBoost)     ("ok" / "ALERT")
''')
H3("B.2 Data flow")
code(r'''
Training path:
  packets -> capture.py -> roundN_flows.csv --+
  attack times -> roundN_attack_log.csv ------+-> train.py -> model.json
                                                (features.py adds
                                                 labels + 22 features)
Live path:
  packets -> detect.py -> features.py (22 features) -> model.json -> ok / ALERT
''')
H3("B.3 Dataset recorded in our lab (measured)")
table(["Recording", "Flows", "Used for"], [
    ["Round 1", "2,281", "Training"],
    ["Round 2", "2,126", "Testing"],
    ["Extra normal traffic (10 minutes)", "681", "First 70% for training, last 30% for testing"],
], [7.0, 3.0, 6.0])
table(["Class", "Training flows", "Test flows", "Test recall"], [
    ["normal", "571", "296", "99.0%"],
    ["scan", "1,002", "1,002", "99.9%"],
    ["synflood", "1,151", "1,000", "100%"],
    ["bruteforce", "33", "33", "100%"],
    ["Total", "2,757", "2,331", "99.8% overall accuracy"],
], [4.0, 4.0, 4.0, 4.0])

H2("Appendix C: Requirements Traceability Matrix (RTM)")
table(["Requirement", "Source", "Design component", "How it was verified", "Status"], [
    ["FR-1, FR-2", "Guide: test on live data", "capture.py, detect.py (NFStream)", "Live flows printed while browsing and during attacks", "Done"],
    ["FR-3, FR-4", "Need for our own training data", "capture.py", "round1, round2 and extra normal CSV files created (2,281 / 2,126 / 681 flows)", "Done"],
    ["FR-5, FR-6, FR-7", "No labels in live traffic; attacks only in a safe lab", "run_round.sh, run_normal.sh (attacker VM)", "Attack logs created; per-attack flow counts checked (scan 1,002, brute force 33, SYN flood 1,151 in round 1)", "Done"],
    ["FR-8", "No labels in live traffic", "features.py label_flows()", "Label counts printed by train.py", "Done"],
    ["FR-9, FR-10", "Own data: one flow can look normal", "features.py (WindowTracker)", "Pattern feature ranked 4th most useful", "Done"],
    ["FR-11, FR-12", "Honest testing", "train.py", "99.8% on unseen round 2; confusion matrix printed", "Done"],
    ["FR-13 to FR-16", "Guide: predict on live data", "detect.py", "Live demo: SCAN, BRUTEFORCE and SYNFLOOD alerts raised; normal flows printed as ok", "Done"],
    ["NFR-1 to NFR-3", "Measurable accuracy", "train.py", "Test results in 5.1", "Met"],
    ["NFR-4, NFR-5", "Live use", "detect.py", "Live test timings in 5.1", "Partly met"],
    ["Safety and compliance (5.2, 5.5)", "IT Act 2000, DPDP Act 2023", "labnet private network", "All attacks run only between 10.10.10.1 and 10.10.10.2", "Done"],
], [2.6, 3.4, 3.3, 4.8, 1.9], font=9.5)

d.save("SRS_CyberSentinel_AI_Team10.docx")
print("SRS written")
