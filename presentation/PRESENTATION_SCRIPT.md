# CyberSentinel AI: Presentation Script

Read each block when that slide is on screen. Every technical word is explained the first time it appears. About 15 minutes of speaking plus about 5 minutes of live demo.

---

## Slide 1: Title

"Good morning, sir. We are Team 10: Jaideep, Nilaksha, Sunayana and Prathamesh.

Our project is called CyberSentinel AI. It is a network intrusion detection system. An intrusion detection system is a program that watches the traffic going in and out of a computer and raises an alarm when it sees an attack.

What makes our project different is two things. First, it works on live traffic, meaning traffic that is happening right now, not a file recorded earlier. Second, the model was trained on traffic that we captured ourselves, in a safe lab that we built."

---

## Slide 2: The problem we were asked to solve

"Sir, you asked us to test our project on real, live data, the way Wireshark shows live traffic, and to predict whether that traffic is an attack. Wireshark is a well-known tool that shows every packet passing through a network card, but it only shows them. It does not tell you whether something is an attack.

When we started working on this, we found that it is hard for three reasons.

First, live means the system must read traffic while it is flowing through a real network card. It cannot use a ready-made CSV file that someone else prepared.

Second, capturing is not enough. For every connection, the system has to decide: is this normal, or is this an attack?

Third, live traffic has no answer key. No packet comes with a tag saying 'I am an attack'. So we also needed a way to prove that our predictions are correct."

---

## Slide 3: Dot 1, look at conversations, not single packets

"Before going further, a few basic terms.

Every computer on a network has an IP address. It is like the address of a house. Every computer also has ports, which are like numbered doors. Each service waits behind its own door. For example, door 80 is for web pages, and door 53 is for DNS. DNS is the service that turns a name like google.com into an IP address.

When two computers talk, the data is broken into small pieces called packets. Even opening one web page takes dozens of packets.

Our first finding was that a single packet is too small to tell us anything about an attack. So instead, we group packets into flows. A flow is one complete conversation between two computers. It tells us who talked to whom, on which door, for how long, and how many packets and bytes were sent.

To build these flows, we used a free Python tool called NFStream. NFStream sits on the network card, sees every packet, and groups the packets of the same conversation into one row. When a conversation goes quiet for five seconds, NFStream decides it has ended and outputs that row.

On the right is real output from our own Linux virtual machine while we were browsing. Watching a YouTube video created one flow with more than three thousand packets. A DNS lookup created a tiny flow of only two packets: one question and one answer."

---

## Slide 4: Dot 2, downloaded datasets fail on live traffic

"Our second finding is about how most projects train their model.

Many intrusion detection projects download a public dataset called CIC-IDS2017. It is a big file of network traffic that a university recorded in 2017, with every flow already labelled as normal or attack. They train their model on this file and then hope it works on live traffic.

When we checked the research, we found three problems with this.

One: researchers later found that more than twenty percent of that dataset had errors and had to be rebuilt or relabelled.

Two: when a model is trained on one public dataset and tested on a different dataset, its accuracy drops to almost random guessing.

Three: even the same traffic gives different results if a different tool is used to turn packets into flows.

So a model trained on someone else's file learns a different world from the one it will see live. That is why we decided not to rely on a downloaded dataset."

---

## Slide 5: Dot 3, one flow alone can look normal

"Our third finding came from our own data, while we were testing the capture.

We compared a normal DNS lookup with a port scan. A port scan is what an attacker usually does first. It is like a thief walking around a building and trying every door handle to find which doors are open. The attacker sends a 'hello' to door 1, door 2, door 3, all the way to door 1000. Closed doors reply 'nobody here', and open doors reply 'yes'. Now the attacker knows which services to attack.

Here is the surprise. A normal DNS lookup has only two packets: one question and one answer. One flow of a port scan also has only two packets: one knock and one refusal. If you look at a single flow, they look almost the same.

The difference is the pattern. A DNS lookup always goes to the same door, door 53. A port scan touches a thousand different doors in less than half a second.

So we added two pattern features. For every flow, we also count how many conversations the same computer started in the last ten seconds, and to how many different doors. A normal user touches one or two doors. A scanner touches hundreds."

---

## Slide 6: Dot 4, live traffic has no answer key

"Our fourth finding is about labels. A label is the correct answer written next to each flow, such as 'normal' or 'attack'. A machine learning model needs these answers to learn, and we need them to measure accuracy.

Live traffic has no labels. A live packet never says that it is an attack.

We also cannot create attacks on a real network. Attacking the hostel or college network without permission is illegal under the IT Act 2000, Sections 43 and 66, and it could harm other people.

So we needed our own controlled place, where we launch every attack ourselves and therefore know exactly which traffic is an attack and when it happened."

---

## Slide 7: Connecting the dots, and our main idea

"Let us put the four findings together.

One: we should judge flows, not single packets.
Two: we should not borrow someone else's dataset.
Three: we should look at patterns across flows, not one flow alone.
Four: we need a safe, controlled place where we know the answers.

Together, these gave us our main idea: instead of borrowing someone else's traffic, we create our own labelled live traffic in a safe lab, using the same code that will later watch the live network.

We attack our own virtual machine inside a private network that never leaves the laptop. We record the exact start and end time of every attack, so every flow gets its label automatically. And because the same NFStream code builds the training data and also runs live, the model sees the same kind of data in training and in real use."

---

## Slide 8: Our setup, two virtual machines on one laptop

"This is how we built the lab.

A virtual machine is a complete computer that runs as a program inside another computer. On one laptop, using a free program called VirtualBox, we run two virtual machines, both running Linux Mint.

On the left is the attacker machine, with the address 10.10.10.1. It plays two roles. Sometimes it behaves like an honest user, and sometimes like an attacker.

In the middle is labnet. This is a private network that VirtualBox creates only inside the laptop. Think of it as a virtual cable between the two machines. It is not connected to the hostel Wi-Fi or to the internet, so no attack can ever leave the laptop. This is what makes our experiments safe and legal.

On the right is the Linux Mint machine, with the address 10.10.10.2. This is the victim. It runs two real services that an attacker would target.

The first is an SSH server on door 22. SSH, which stands for Secure Shell, lets a person log in to a computer from another computer by typing a username and password, and then run commands on it remotely. System administrators use it every day.

The second is the Apache web server on door 80. It sends a web page to anyone who asks for it, just like any website.

The same Mint machine also runs our detector, which is written in Python. NFStream reads the live packets and builds flows. Our file features.py calculates 22 numbers for each flow. A trained XGBoost model looks at those numbers and decides normal or attack, and finally we print either 'ok' or an alert."

---

## Slide 9: How we built and tested the model

"Our method has six steps.

Step 1, capture. NFStream on the Mint machine recorded every flow on the lab network and saved it in a CSV file.

Step 2, label. The attacker's script wrote down the exact start and end time of every attack. Afterwards, every flow that came from the attacker's address during an attack's time window got that attack's name. Every other flow was labelled normal. Nobody labelled anything by hand. We knew the answers because we launched the attacks ourselves.

Step 3, features. For each flow we use 22 numbers. Twenty describe the conversation itself: how many packets and bytes in each direction, how long it lasted, the smallest, average and largest packet size, the gaps between packets, and how many special control packets appeared, such as the 'hello', 'goodbye' and 'refuse' packets. The other two are the pattern numbers I explained earlier.

Step 4, train. We used XGBoost, which is a machine learning method that builds many small decision trees and combines them. It works very well on table-like data such as our flow numbers. It learned from round 1 of our data.

Step 5, test. We tested it on round 2, a separate recording session that the model had never seen.

Step 6, detect live. The same code reads live traffic and prints alerts.

The bar at the bottom shows what happened in one recording round. First, three minutes of normal use. Normal use means what an honest user does: the attacker machine opened web pages on the victim's web server and logged in over SSH with the correct password, ran harmless commands such as listing files, and logged out, with short random pauses like a real person.

Then came three attacks, one after another.

First, the port scan, which I explained: knocking on a thousand doors to see which are open. We used a tool called nmap.

Second, password guessing, also called a brute-force attack. The attacker stands at the SSH door and tries password after password for a user account until one works. We used a tool called hydra, with a list of 151 passwords where the correct one was last.

Third, a SYN flood. To explain this, I need to explain how two computers start a conversation. It works like a phone call. The caller says 'hello', which is called a SYN packet. The receiver answers 'yes, I hear you'. Then the caller confirms, and the conversation starts. In a SYN flood, the attacker sends about a hundred 'hello' packets every second and never confirms. The server keeps waiting on each half-open call, and if this continues, real users cannot get through. It is a kind of denial-of-service attack. We used a tool called hping3.

Then two more minutes of normal use. We left twenty seconds of silence between the parts, so that no normal flow could accidentally fall inside an attack's time window. We recorded two rounds this way: round 1 for training and round 2 for testing. We also recorded ten extra minutes of normal traffic, because normal traffic was too small in number."

---

## Slide 10: Results on data the model had never seen

"Here are the results on the test data, which is round 2 plus the last part of the extra normal recording. The model had never seen any of it.

The test data had 2,331 flows, which means 2,331 separate conversations. 1,002 of them were port scan flows, because every door the scanner knocked on is a separate conversation. 1,000 were SYN flood flows, because every fake 'hello' counts as its own conversation. 296 were normal flows, and 33 were password-guessing flows, because hydra tries about four or five passwords in each connection.

The model labelled 2,327 of these 2,331 flows correctly. That is 99.8 percent.

The table on the right is called a confusion matrix. Each row is the real answer, and each column is the model's guess. The numbers on the diagonal are correct guesses. Only four were wrong. Three normal SSH logins were wrongly flagged as password guessing, which are false alarms. And one flow of the port scan was missed, but the other 1,001 flows of the same scan were caught, so the scan itself was still detected.

We also checked which numbers the model relied on most. Our own pattern feature, the number of different doors touched in ten seconds, was the fourth most useful out of 22."

---

## Slide 11: Live detection, what the detector prints

"This is real output from our live detector. Each line is one conversation that just finished. Normal web and SSH traffic is printed as 'ok'. When an attack happens, the detector prints an alert with the attack's name, the attacker's address, and how many flows it saw. In this run, all three attacks raised the correct alert, and no normal traffic was flagged.

One point to note: a flow is judged only after the conversation has finished, so an alert appears a few seconds after the attack.

Now we will show this working live."

**→ Now run the live demo. Follow DEMO_COMMANDS.md, section B. What to say during each step is below.**

---

## During the live demo

**Step 1, start the detector on Mint:**
"On the victim machine, I am starting our detector. It is now watching the lab network card."

**Step 2, start normal traffic on the attacker:**
"Now the attacker machine is acting as an honest user: opening web pages and logging in over SSH with the correct password. As you can see, the detector prints 'ok' for these conversations."

**Step 3, port scan (nmap):**
"Now I am running a port scan. The attacker is knocking on a thousand doors of the victim in less than a second. In a few seconds, you will see 'ALERT SCAN'. The number at the end shows how many different doors were touched in the last ten seconds."

**Step 4, password guessing (hydra):**
"Now a password-guessing attack on the SSH login. The attacker is trying one password after another for the user 'victim'. This takes about a minute. You will see 'ALERT BRUTEFORCE'."

**Step 5, SYN flood (hping3):**
"Now a SYN flood on the web server for ten seconds: about a hundred 'hello' packets every second that never complete the conversation. You will see 'ALERT SYNFLOOD'."

**Step 6, stop the detector:**
"When I stop the detector, it shows how many conversations it put into each group."

---

## Slide 12: What is still limited, and what we will do next

"We want to be honest about the limits.

First, lab traffic is cleaner and simpler than a real network, so the accuracy on a real network will be lower than 99.8 percent. Our result proves that the whole system works from capture to live alert. It does not yet prove real-world accuracy.

Second, we have only 33 password-guessing flows per round, which is a small number to learn from.

Third, our virtual machines run slowly on this laptop, so some alerts were delayed until new traffic arrived.

Fourth, one alert showed the wrong direction, because of leftover SSH packets after the attack ended.

Next, we plan to add more attack types, such as slow denial-of-service and web attacks. We will run the detector on our own real browsing traffic to count how many false alarms it raises. We will add explanations that show why each alert fired. And we will build a simple dashboard and compare our results with Suricata, which is a popular rule-based detection tool."

---

## Slide 13: Thank you

"Thank you, sir. We are happy to take your questions."

---

## If sir asks

**"What is normal traffic in your project?"**
"Normal traffic is legitimate use of the server: opening its web pages and logging in over SSH with the correct password, at a human pace with pauses in between. Our attacker machine plays an honest user to create it."

**"How did you label the data?"**
"We launched every attack ourselves and logged its exact start and end time. Every flow from the attacker's address inside an attack's time window got that attack's name. Everything else is normal. We left twenty seconds of silence between parts so nothing overlaps."

**"Why not use CIC-IDS2017?"**
"Research shows that more than twenty percent of it had errors, and models trained on one dataset perform almost randomly on another. Training on our own traffic means the model learns from exactly the kind of data it sees live."

**"Is 99.8 percent realistic?"**
"It is realistic for our lab, where attacks are very clear. It proves that the whole pipeline works. Real networks are messier, which is why our next step is testing on real browsing traffic."

**"What is NFStream?"**
"It is a free Python tool that reads packets from a network card and groups the packets of each conversation into one row of statistics, which is called a flow."

**"Why XGBoost?"**
"It works very well on table-like data such as our flow numbers, it is fast, and it is widely used for this kind of problem."

**"What is the private network?"**
"It is a virtual network that VirtualBox creates only inside the laptop. It connects our two virtual machines and nothing else, so attack traffic can never reach the hostel or college network."

**"What is NAT?" (only if asked)**
"NAT is how the virtual machines reach the internet, for example to install software. VirtualBox sends their internet traffic out using the laptop's own address, like a receptionist forwarding calls. We never used it for attacks. All attacks stay on the private network."
