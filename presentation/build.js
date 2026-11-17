const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("C:/Users/Asus/.claude/skills/synced/920c95f9-1dac-49d7-ad78-9795476d3e59_32e28b00-15e9-4766-9086-9d386fb0ad43/pptx/scripts/apply_theme.js");

const THEME = {
  name: "CyberSentinel",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0F172A", lt1: "FFFFFF", dk2: "0B1F33", lt2: "EEF3F8",
    accent1: "0096B7", accent2: "D62839", accent3: "2A9D8F", accent4: "F4A261",
    accent5: "5C6B7A", accent6: "BFE6EF", hlink: "0096B7", folHlink: "5C6B7A",
  },
};
const H = THEME.colors; // hex values for hex-only options

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "CyberSentinel AI - Live Network Intrusion Detection";
pres.author = "Team 10";
const C = pres.SchemeColor;

const W = 13.333, M = 0.6, CW = W - 2 * M; // content width 12.133

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: H.lt1 },
  objects: [
    { text: { text: "CyberSentinel AI  |  Team 10", options: { x: M, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: C.accent5, margin: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: CW, h: 0.85, fontSize: 34, bold: true, color: C.text1, valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.23, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK",
  background: { color: H.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: CW, h: 0.85, fontSize: 34, bold: true, color: C.background1, valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.23, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

// ---------- helpers ----------
const shadow = () => ({ type: "outer", color: "000000", opacity: 0.12, blur: 6, offset: 2, angle: 90 });
function card(s, x, y, w, h, fill, name, withShadow = true) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill }, shadow: withShadow ? shadow() : undefined, objectName: name });
}
function text(s, t, o) { s.addText(t, Object.assign({ isTextBox: true, margin: 0, valign: "top", fontSize: 16, color: C.text1 }, o)); }
function numCircle(s, n, x, y, d, fill, color) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: "num" + n });
  s.addText(String(n), { isTextBox: true, x, y, w: d, h: d, align: "center", valign: "middle", fontSize: 18, bold: true, color, margin: 0 });
}
const bullets = (arr, extra = {}) => arr.map((t, i) => ({ text: t, options: Object.assign({ bullet: true, paraSpaceAfter: 8, breakLine: i < arr.length - 1 }, extra) }));

// ===== 1. Title =====
let s = pres.addSlide({ masterName: "DARK" });
text(s, "AISD Project Review  |  Team 10", { x: M, y: 1.2, w: CW, h: 0.4, fontSize: 16, color: C.accent6 });
text(s, "CyberSentinel AI", { x: M, y: 1.75, w: CW, h: 1.1, fontSize: 54, bold: true, color: C.background1, fontFace: "Cambria" });
text(s, "Detecting network attacks live, using a model trained on traffic we captured ourselves", { x: M, y: 2.9, w: 10.5, h: 0.9, fontSize: 22, color: C.accent6 });
const team = [
  ["Bachu Venkata Siva Jaideep", "01fe24bci084"],
  ["Nilaksha Nath", "01fe24bci087"],
  ["Sunayana Kamath", "01fe24bci073"],
  ["Prathamesh Eedigi", "01fe24bci006"],
];
team.forEach(([n, srn], i) => {
  const x = M + i * 3.08;
  card(s, x, 4.75, 2.9, 1.25, "16304A", "team" + i, false);
  text(s, n, { x: x + 0.2, y: 4.92, w: 2.5, h: 0.6, fontSize: 15, bold: true, color: C.background1 });
  text(s, srn, { x: x + 0.2, y: 5.55, w: 2.5, h: 0.3, fontSize: 13, color: C.accent6 });
});
s.addNotes("Introduce the team and the one-line idea: we detect attacks live, and the model is trained on traffic we captured ourselves in a safe lab.");

// ===== 2. The problem =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("The problem we were asked to solve", { placeholder: "title" });
card(s, M, 1.45, CW, 1.35, H.lt2, "quote", false);
text(s, "Our guide asked us to test the project on real, live data, the way Wireshark shows live traffic, and to predict whether that traffic is an attack.", { x: M + 0.35, y: 1.62, w: CW - 0.7, h: 1.0, fontSize: 20, italic: true, valign: "middle" });
const probs = [
  ["Live, not a ready-made file", "The system has to read traffic while it is flowing through a real network card, not a CSV file that someone else prepared earlier."],
  ["Predict, not only capture", "Wireshark only shows us the packets. Our system has to decide, for every connection, whether it is normal traffic or an attack."],
  ["No answer key", "Live traffic does not come with labels. So we also need a way to prove that our predictions are actually correct."],
];
probs.forEach(([h, b], i) => {
  const x = M + i * 4.14;
  card(s, x, 3.15, 3.84, 3.45, H.lt1, "prob" + i);
  numCircle(s, i + 1, x + 0.3, 3.4, 0.6, C.accent1, C.background1);
  text(s, h, { x: x + 0.3, y: 4.15, w: 3.24, h: 0.45, fontSize: 19, bold: true });
  text(s, b, { x: x + 0.3, y: 4.65, w: 3.24, h: 1.8, fontSize: 15, color: C.text2 });
});
s.addNotes("Read the guide's requirement. Then explain the three things that make it hard: it must be live, it must predict, and live traffic has no labels to check against.");

// ===== 3. Dot 1: flows =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Dot 1: Look at conversations, not single packets", { placeholder: "title" });
text(s, bullets([
  "A single packet is too small to tell us anything useful about an attack.",
  "So we group packets into flows. A flow is one full conversation between two computers: who talked to whom, for how long, and how many packets and bytes were sent.",
  "We used a tool called NFStream, which builds these flows live from the network card. For every flow we keep 20 numbers that describe it.",
]), { x: M, y: 1.5, w: 5.3, h: 4.6, fontSize: 16, color: C.text1 });
card(s, 6.2, 1.5, 6.53, 3.9, "0B1F33", "terminal1");
const flowLines = [
  ["Live flows from our Linux VM while browsing", "8ED1E0"],
  ["destination        port  app            packets", "8ED1E0"],
  ["216.239.38.120     443   QUIC              3048", "FFFFFF"],
  ["142.251.152.4      443   QUIC.YouTube      1044", "FFFFFF"],
  ["172.64.155.209     443   TLS                996", "FFFFFF"],
  ["142.251.155.120    443   QUIC.Google        394", "FFFFFF"],
  ["1.0.0.3             53   DNS.YouTube          2", "FFFFFF"],
  ["1.0.0.3             53   DNS.WhatsApp         2", "FFFFFF"],
  ["1.0.0.3             53   DNS.Google           2", "FFFFFF"],
];
s.addText(flowLines.map(([t, c], i) => ({ text: t, options: { color: c, bold: i < 2, breakLine: i < flowLines.length - 1 } })),
  { isTextBox: true, x: 6.5, y: 1.75, w: 6.0, h: 3.5, fontFace: "Courier New", fontSize: 14, valign: "top", margin: 0, paraSpaceAfter: 6 });
text(s, "This is real output from our own capture. A YouTube video is one big flow, while a DNS lookup is a tiny flow of only 2 packets.", { x: 6.2, y: 5.55, w: 6.53, h: 0.6, fontSize: 13, color: C.accent5 });
s.addNotes("Explain what a flow is. Point at the terminal: these are real flows from our VM. A YouTube stream has thousands of packets, a DNS lookup only 2.");

// ===== 4. Dot 2: public datasets =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Dot 2: Downloaded datasets fail on live traffic", { placeholder: "title" });
text(s, "Many intrusion detection projects train their model on a public dataset such as CIC-IDS2017 and then hope it works on live traffic. When we checked the research, we found three problems with this.", { x: M, y: 1.45, w: CW, h: 0.9, fontSize: 17 });
const dots2 = [
  [">20%", "of the traffic in CIC-IDS2017 had errors and had to be rebuilt or relabelled by later researchers.", "Engelen et al., IEEE SPW 2021"],
  ["Near random", "is how a model performs when it is trained on one public dataset and tested on a different one.", "Cantone et al., arXiv 2402.10974, 2024"],
  ["Different", "results come out when the same traffic is turned into flows by a different tool.", "arXiv 2412.14021, 2024"],
];
dots2.forEach(([big, body, src], i) => {
  const x = M + i * 4.14;
  card(s, x, 2.6, 3.84, 3.0, H.lt2, "d2_" + i, false);
  text(s, big, { x: x + 0.3, y: 2.8, w: 3.24, h: 0.8, fontSize: 36, bold: true, color: C.accent2 });
  text(s, body, { x: x + 0.3, y: 3.65, w: 3.24, h: 1.3, fontSize: 15 });
  text(s, src, { x: x + 0.3, y: 5.1, w: 3.24, h: 0.35, fontSize: 11, italic: true, color: C.accent5 });
});
text(s, "So a model trained on someone else's file learns a different world from the one it will see live.", { x: M, y: 5.95, w: CW, h: 0.5, fontSize: 17, bold: true, color: C.accent1 });
s.addNotes("These three findings come from published papers that we checked. The point: the downloaded data and the live traffic do not match, so accuracy on the file says little about live use.");

// ===== 5. Dot 3: one flow can lie =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Dot 3: One flow alone can look normal", { placeholder: "title" });
text(s, "While testing our capture, we noticed that a normal DNS lookup and a port scan look almost the same if you look at only one flow.", { x: M, y: 1.45, w: CW, h: 0.8, fontSize: 17 });
const cmp = [
  ["A normal DNS lookup", C.accent3, ["Each flow has only 2 packets: one question and one answer.", "The app is recognised, for example DNS.Google.", "It always goes to the same port, port 53."]],
  ["A port scan (attack)", C.accent2, ["Each flow also has only 2 packets: one knock and one refusal.", "The app is Unknown, because nothing real is talking.", "It touches 1000 different ports in less than half a second."]],
];
cmp.forEach(([h, col, items], i) => {
  const x = M + i * 6.27;
  card(s, x, 2.4, 5.86, 2.75, H.lt1, "cmp" + i);
  text(s, h, { x: x + 0.3, y: 2.6, w: 5.26, h: 0.45, fontSize: 20, bold: true, color: col });
  text(s, bullets(items), { x: x + 0.3, y: 3.15, w: 5.26, h: 1.9, fontSize: 15 });
});
card(s, M, 5.45, CW, 1.15, H.dk2, "insight", false);
text(s, "The difference is in the pattern. So we added two pattern features: how many flows, and how many different ports, one computer has touched in the last 10 seconds.", { x: M + 0.35, y: 5.55, w: CW - 0.7, h: 0.95, fontSize: 17, color: C.background1, valign: "middle" });
s.addNotes("This came from our own data, not from a book. One scan flow looks harmless, but hundreds of ports in seconds is clearly an attack. That is why we added the two pattern features.");

// ===== 6. Dot 4: no answer key =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Dot 4: Live traffic has no answer key", { placeholder: "title" });
const rows4 = [
  ["Live packets have no labels", "A live packet never says that it is an attack. Without labels, we cannot train a model and we cannot measure how accurate it is."],
  ["We cannot attack a real network", "Attacking the hostel or college network without permission is illegal under the IT Act 2000 (Sections 43 and 66), and it could also harm other people."],
  ["So we need our own controlled place", "We need a place where we launch every attack ourselves, so that we know exactly which traffic is an attack and when it happened."],
];
rows4.forEach(([h, b], i) => {
  const y = 1.55 + i * 1.75;
  card(s, M, y, CW, 1.5, i === 2 ? H.lt2 : H.lt1, "r4_" + i);
  numCircle(s, i + 1, M + 0.3, y + 0.42, 0.66, i === 2 ? C.accent1 : C.accent5, C.background1);
  text(s, h, { x: M + 1.25, y: y + 0.2, w: CW - 1.55, h: 0.45, fontSize: 19, bold: true });
  text(s, b, { x: M + 1.25, y: y + 0.68, w: CW - 1.55, h: 0.75, fontSize: 15, color: C.text2 });
});
s.addNotes("Explain why we could not simply capture hostel traffic and use it: there are no labels, and attacking real networks is illegal. This leads to the idea of a lab.");

// ===== 7. Eureka =====
s = pres.addSlide({ masterName: "DARK" });
s.addText("Connecting the dots", { placeholder: "title" });
const dotsSum = ["Use flows", "Don't borrow foreign data", "Use patterns, not one flow", "Work in a safe lab"];
dotsSum.forEach((t, i) => {
  const x = M + i * 3.08;
  card(s, x, 1.45, 2.9, 0.9, "16304A", "ds" + i, false);
  text(s, "Dot " + (i + 1) + ": " + t, { x: x + 0.2, y: 1.45, w: 2.5, h: 0.9, fontSize: 15, bold: true, color: C.accent6, valign: "middle" });
});
text(s, "EUREKA", { x: M, y: 2.75, w: CW, h: 0.45, fontSize: 18, bold: true, color: C.accent4 });
text(s, "Instead of borrowing someone else's traffic, we create our own labelled live traffic in a safe lab, using the same code that will later watch the live network.", { x: M, y: 3.25, w: CW, h: 1.5, fontSize: 28, bold: true, color: C.background1, fontFace: "Cambria" });
const eu = [
  "We attack our own virtual machine inside a private network that never leaves the laptop.",
  "We record the exact start and end time of every attack, so every flow gets its label automatically.",
  "The same capture code builds the training data and runs live, so the model sees the same kind of data in both.",
];
eu.forEach((t, i) => {
  const x = M + i * 4.14;
  numCircle(s, i + 1, x, 5.1, 0.55, C.accent1, C.background1);
  text(s, t, { x: x + 0.75, y: 5.05, w: 3.1, h: 1.6, fontSize: 15, color: C.background1 });
});
s.addNotes("This is the key idea of the project. Put the four dots together: we make our own ground truth in a lab, and the same code is used for training and for live detection.");

// ===== 8. Architecture =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Our setup: two virtual machines on one laptop", { placeholder: "title" });
card(s, M, 1.4, CW, 5.35, H.lt2, "laptop", false);
text(s, "One laptop running Windows 11 and VirtualBox", { x: M + 0.25, y: 1.5, w: 6, h: 0.35, fontSize: 13, bold: true, color: C.accent5 });
// attacker
card(s, 0.9, 2.0, 3.45, 4.5, H.lt1, "attackerVM");
text(s, "Attacker VM", { x: 1.15, y: 2.15, w: 3.0, h: 0.45, fontSize: 20, bold: true, color: C.accent2 });
text(s, "IP 10.10.10.1", { x: 1.15, y: 2.6, w: 3.0, h: 0.35, fontSize: 14, color: C.accent5 });
text(s, bullets(["nmap: port scan", "hydra: password guessing", "hping3: SYN flood", "curl and ssh: normal traffic"]), { x: 1.15, y: 3.1, w: 3.0, h: 3.2, fontSize: 15 });
// network
s.addShape(pres.shapes.LEFT_RIGHT_ARROW, { x: 4.5, y: 3.95, w: 1.15, h: 0.55, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "labnet" });
text(s, "labnet", { x: 4.4, y: 3.45, w: 1.35, h: 0.4, fontSize: 15, bold: true, align: "center", color: C.accent1 });
text(s, "private network inside the laptop", { x: 4.4, y: 4.6, w: 1.35, h: 0.9, fontSize: 11, align: "center", color: C.accent5 });
// mint
card(s, 5.8, 2.0, 6.63, 4.5, H.lt1, "mintVM");
text(s, "Linux Mint VM: victim and detector", { x: 6.05, y: 2.15, w: 6.1, h: 0.45, fontSize: 20, bold: true, color: C.accent1 });
text(s, "IP 10.10.10.2", { x: 6.05, y: 2.6, w: 6.1, h: 0.35, fontSize: 14, color: C.accent5 });
card(s, 6.05, 3.05, 6.13, 0.7, H.lt2, "services", false);
text(s, "Victim services: SSH server (port 22) and Apache web server (port 80)", { x: 6.2, y: 3.05, w: 5.9, h: 0.7, fontSize: 14, valign: "middle" });
text(s, "Detector, written in Python, watching the lab network live:", { x: 6.05, y: 3.95, w: 6.13, h: 0.35, fontSize: 13, color: C.accent5 });
const pipe = [["NFStream", "packets to flows"], ["features.py", "22 numbers"], ["XGBoost", "trained model"], ["ALERT", "or ok"]];
pipe.forEach(([a, b], i) => {
  const x = 6.05 + i * 1.626;
  const red = i === 3;
  card(s, x, 4.4, 1.25, 1.05, red ? H.accent2 : H.dk2, "pipe" + i, false);
  text(s, [{ text: a, options: { bold: true, fontSize: 14, breakLine: true } }, { text: b, options: { fontSize: 11 } }], { x: x + 0.05, y: 4.4, w: 1.15, h: 1.05, align: "center", valign: "middle", color: C.background1 });
  if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 1.29, y: 4.78, w: 0.3, h: 0.3, fill: { color: C.accent5 }, line: { color: C.accent5 }, objectName: "pa" + i });
});
text(s, "The same NFStream and features.py code was used to build the training data.", { x: 6.05, y: 5.65, w: 6.13, h: 0.6, fontSize: 13, italic: true, color: C.accent5 });
s.addNotes("Walk from left to right: the attacker VM sends normal traffic and attacks over a private network. The Mint VM is the victim, and it also runs our detector: NFStream makes flows, features.py computes 22 numbers, XGBoost predicts, and we print an alert.");

// ===== 9. Methodology =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("How we built and tested the model", { placeholder: "title" });
const steps = [
  ["Capture", "NFStream records every flow on the lab network into a CSV file."],
  ["Label", "A flow from the attacker during a logged attack time gets that attack's name."],
  ["Features", "20 numbers per flow, plus the 2 pattern features."],
  ["Train", "XGBoost learns from round 1 of our data."],
  ["Test", "We test on round 2, a session the model never saw."],
  ["Detect live", "The same code reads live traffic and prints alerts."],
];
steps.forEach(([h, b], i) => {
  const x = M + i * 2.056;
  card(s, x, 1.45, 1.85, 2.75, i === 5 ? H.lt2 : H.lt1, "st" + i);
  numCircle(s, i + 1, x + 0.2, 1.62, 0.5, C.accent1, C.background1);
  text(s, h, { x: x + 0.2, y: 2.22, w: 1.5, h: 0.4, fontSize: 17, bold: true });
  text(s, b, { x: x + 0.2, y: 2.65, w: 1.5, h: 1.5, fontSize: 13, color: C.text2 });
});
text(s, "What happens in one data collection round", { x: M, y: 4.5, w: CW, h: 0.4, fontSize: 17, bold: true });
const seg = [["Normal use, 3 min", 3.3, H.accent3], ["Scan", 1.2, H.accent2], ["Password guessing", 2.7, H.accent2], ["SYN flood", 1.5, H.accent2], ["Normal use, 2 min", 2.43, H.accent3]];
let sx = M;
seg.forEach(([t, w, col], i) => {
  s.addShape(pres.shapes.RECTANGLE, { x: sx, y: 5.0, w, h: 0.65, fill: { color: col }, line: { color: col }, objectName: "seg" + i });
  text(s, t, { x: sx, y: 5.0, w, h: 0.65, fontSize: 13, bold: true, align: "center", valign: "middle", color: C.background1 });
  sx += w + 0.25;
});
text(s, "We left 20 seconds of silence between the parts so the labels stay clean. We ran two rounds (round 1 for training, round 2 for testing) plus 10 extra minutes of normal traffic.", { x: M, y: 5.85, w: CW, h: 0.8, fontSize: 15, color: C.text2 });
s.addNotes("Six steps from capture to live detection. Explain labelling simply: we know the attacker's IP and the exact time of each attack, so labels are automatic. Training and testing use different sessions.");

// ===== 10. Results =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Results on data the model had never seen", { placeholder: "title" });
text(s, "99.8%", { x: M, y: 1.45, w: 4.6, h: 1.1, fontSize: 64, bold: true, color: C.accent1 });
text(s, "of the 2,331 flows in round 2 were classified correctly. Only 4 flows were wrong.", { x: M, y: 2.6, w: 4.6, h: 0.8, fontSize: 16 });
const hdr = (t) => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } });
const perClass = [
  [hdr("Class"), hdr("Test flows"), hdr("Caught")],
  ["Normal", "296", "99.0%"],
  ["Port scan", "1,002", "99.9%"],
  ["SYN flood", "1,000", "100%"],
  ["Password guessing", "33", "100%"],
];
s.addTable(perClass, { x: M, y: 3.6, w: 4.6, colW: [2.0, 1.3, 1.3], fontSize: 14, fontFace: "Calibri", color: H.dk1, border: { type: "solid", pt: 0.75, color: "C9D3DD" }, rowH: 0.42, align: "left", valign: "middle" });
text(s, "Confusion matrix: rows are the real label, columns are the model's guess", { x: 5.7, y: 1.5, w: 7.03, h: 0.4, fontSize: 14, bold: true });
const diag = (v) => ({ text: v, options: { bold: true, fill: { color: H.accent6 } } });
const miss = (v) => ({ text: v, options: { bold: true, color: H.accent2, fill: { color: "FBE3E6" } } });
const cm = [
  [hdr(""), hdr("Guess: brute"), hdr("Guess: normal"), hdr("Guess: scan"), hdr("Guess: SYN")],
  [hdr("Real: brute"), diag("33"), "0", "0", "0"],
  [hdr("Real: normal"), miss("3"), diag("293"), "0", "0"],
  [hdr("Real: scan"), "0", miss("1"), diag("1001"), "0"],
  [hdr("Real: SYN"), "0", "0", "0", diag("1000")],
];
s.addTable(cm, { x: 5.7, y: 2.0, w: 7.03, colW: [1.55, 1.37, 1.37, 1.37, 1.37], fontSize: 14, fontFace: "Calibri", color: H.dk1, border: { type: "solid", pt: 0.75, color: "C9D3DD" }, rowH: 0.45, align: "center", valign: "middle" });
text(s, bullets([
  "3 normal SSH logins were wrongly flagged as password guessing. These are false alarms.",
  "1 scan flow was missed, but the other 1,001 flows of the same scan were caught.",
  "The pattern feature we added (different ports in 10 seconds) was the 4th most useful feature.",
]), { x: 5.7, y: 4.5, w: 7.03, h: 2.1, fontSize: 14 });
s.addNotes("The model was trained on round 1 and tested on round 2. 99.8 percent correct. Be honest: lab attacks are very clear, so this proves the pipeline works, not real-world accuracy.");

// ===== 11. Live detection =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Live detection: what the detector prints", { placeholder: "title" });
card(s, M, 1.45, CW, 3.25, "0B1F33", "terminal2");
const live = [
  ["10:12:49  ok       10.10.10.1 -> 10.10.10.2:80  (confidence 1.00)", "7FD8B0"],
  ["10:12:50  ok       10.10.10.1 -> 10.10.10.2:22  (confidence 1.00)", "7FD8B0"],
  ["10:16:39  [ALERT]  SCAN        from 10.10.10.1  (+285 flows, ports in last 10 s: 285)", "FF8A93"],
  ["10:17:33  [ALERT]  SCAN        from 10.10.10.1  (+282 flows, ports in last 10 s: 868)", "FF8A93"],
  ["10:18:15  [ALERT]  BRUTEFORCE  from 10.10.10.1  (+2 flows, confidence 1.00)", "FF8A93"],
  ["10:18:56  [ALERT]  SYNFLOOD    from 10.10.10.1  (+137 flows, confidence 1.00)", "FF8A93"],
  ["Stopped. normal: 33   scan: 1002   bruteforce: 11   synflood: 251", "FFFFFF"],
];
s.addText(live.map(([t, c], i) => ({ text: t, options: { color: c, breakLine: i < live.length - 1 } })),
  { isTextBox: true, x: M + 0.35, y: 1.7, w: CW - 0.7, h: 2.85, fontFace: "Courier New", fontSize: 15, valign: "top", margin: 0, paraSpaceAfter: 8 });
text(s, bullets([
  "Normal web and SSH traffic is printed as ok. In this run there were no false alarms on normal traffic.",
  "All three attacks raised the correct alert: the port scan, the password guessing and the SYN flood.",
  "A flow is judged only after it has finished, so an alert comes a few seconds after the attack when other traffic is flowing.",
  "Next, we will show this working live on our lab.",
]), { x: M, y: 4.95, w: CW, h: 1.9, fontSize: 15 });
s.addNotes("This is real output from our detector. Then switch to the live demo: start the detector on Mint, then run the scan, the password guessing and the SYN flood from the attacker.");

// ===== 12. Limits & next =====
s = pres.addSlide({ masterName: "CONTENT" });
s.addText("What is still limited, and what we will do next", { placeholder: "title" });
const cols = [
  ["Current limits", C.accent2, [
    "Lab traffic is cleaner and simpler than a real network, so real-world accuracy will be lower.",
    "We have only 33 password-guessing flows per round, which is a small number to learn from.",
    "Our VMs run slowly on this laptop, so some alerts were delayed until new traffic arrived.",
    "One alert showed the wrong direction because of leftover SSH packets after the attack.",
  ]],
  ["Next steps", C.accent3, [
    "Add more attack types, such as slow DoS and web attacks.",
    "Run the detector on our own real browsing traffic to count false alarms.",
    "Show why each alert fired, using SHAP explanations.",
    "Build a simple dashboard and compare our results with Suricata, a rule-based tool.",
  ]],
];
cols.forEach(([h, col, items], i) => {
  const x = M + i * 6.27;
  card(s, x, 1.45, 5.86, 4.3, i === 0 ? H.lt1 : H.lt2, "col" + i);
  text(s, h, { x: x + 0.35, y: 1.65, w: 5.16, h: 0.5, fontSize: 21, bold: true, color: col });
  text(s, bullets(items, { paraSpaceAfter: 12 }), { x: x + 0.35, y: 2.3, w: 5.16, h: 3.3, fontSize: 15 });
});
s.addNotes("Be honest about the limits; it shows we understand our own results. Then list the next steps.");

// ===== 13. Thank you =====
s = pres.addSlide({ masterName: "DARK" });
text(s, "Thank you", { x: M, y: 2.3, w: CW, h: 1.2, fontSize: 54, bold: true, color: C.background1, align: "center", fontFace: "Cambria" });
text(s, "We are happy to take your questions.", { x: M, y: 3.6, w: CW, h: 0.6, fontSize: 22, color: C.accent6, align: "center" });
text(s, team.map((t) => t[0]).join("   |   "), { x: M, y: 5.2, w: CW, h: 0.5, fontSize: 15, color: C.accent6, align: "center" });

(async () => {
  const out = path.join(__dirname, "CyberSentinel_AI_Team10.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("written", out);
})();
