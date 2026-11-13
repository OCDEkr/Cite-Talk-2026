"""Build the CITE workshop deck, PDF, facilitator notes, and synthetic lab inputs.

Requires python-pptx, Pillow, and PyMuPDF. No source documents are modified.
"""
from pathlib import Path
import csv
import json
import subprocess
import xml.etree.ElementTree as ET
import zipfile

import fitz
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent / 'workshop-deck'
KIT = OUT / 'attendee-kit'
OUT.mkdir(exist_ok=True)
KIT.mkdir(exist_ok=True)
FONTDIR = Path('/System/Library/Fonts/Supplemental')
FONTS = {'regular': FONTDIR/'Arial.ttf', 'bold': FONTDIR/'Arial Bold.ttf',
         'mono': FONTDIR/'Andale Mono.ttf'}

ORIGINAL_PROMPT = 'I would like to build a user friendly interface to nmap similar to zenmap but a web app. Do your own research while planning and ask me any clarifying questions.'
APP_BRIEF = '''Build a working local web-based Nmap scanner inspired by Zenmap. It must execute the installed Nmap binary through a backend, and also import saved Nmap XML. Use a simple local stack with minimal dependencies. Ask me the important questions and show your plan before coding.

For today's first version:
- Bind the web server to 127.0.0.1. One local user; no deployment or accounts.
- Include a target box, a fixed TCP connect scan profile, a Scan button, running/completed/error states, raw Nmap output, a host list, and a ports/services detail panel.
- Start with one authorized target: 127.0.0.1. Keep the backend's target allowlist limited to that address until the instructor explicitly supplies another authorized lab target.
- Use a fixed modest TCP port list and -sT, with no OS detection, UDP scanning, NSE scripts, or elevated privileges for the first version. Live UDP scanning is outside this exercise; importing saved UDP results must still work.
- Invoke Nmap using an argument array, never a shell command assembled from user input. Validate the target and profile on the backend. Reject extra flags and targets outside the allowlist. Add a timeout, prevent overlapping scans, and show a useful message if Nmap is absent or fails.
- Capture XML using Nmap's XML output and use the same result model for imported and live scans. Treat XML as untrusted data: reject DTD/entity declarations, handle malformed files, and render strings as text.
- Import fictitious-50-hosts.xml. Show total/up/down host counts and open-port counts. Let me search by hostname/IP/service and select a host to inspect its ports, states, protocols, and services. Clearly label imported data as a saved scan.
- Explain how to start the app and run meaningful checks. Do not add a database, cloud services, topology graph, arbitrary command editor, or production features yet.

Acceptance: fixture import shows 50 hosts, 45 up, 5 down, and 125 open port records (115 TCP and 10 UDP). Closed port records must not be counted as open. The app must also run a real loopback scan and display the actual results; imported results alone do not finish the exercise.'''
TASK_PROMPT = '''Read offboarding-policy.txt. Draft an offboarding checklist for our fictional district using Entra ID, Google Workspace, Aeries, and the VPN. Include columns for action, responsible role, verification, and evidence. Use only the policy for deadlines. Mark missing details as "decision needed". Draft the checklist only; do not connect to any system or disable accounts. Save it as offboarding-checklist.md.'''
LOG_PROMPT = '''Inspect the schema of signins.csv. These are synthetic training events, not a native Entra export. Write a reusable Python script using the standard library, then run it on the file. Do not modify the source.
Use the explicit workshop rules: flag a successful sign-in outside 07:00 through 18:59 UTC, or outside the training baseline of US; also flag a success preceded by at least three failures for the same user in the previous ten minutes, including the ten-minute boundary. A row can have multiple reasons. Sort chronologically and write flagged-events.csv with the event ID, user, timestamp, and reasons. These are review signals, not proof of compromise.
Create small tests for the time boundaries and the failure-then-success rule, run them, and explain any ambiguous assumptions. Do not infer impossible travel; this file has no coordinates or user history.'''


def make_inputs():
    (KIT/'offboarding-policy.txt').write_text('''FICTITIOUS TRAINING POLICY — Riverbend Workshop District
1. Disable departing staff accounts within 24 hours of the effective separation time.
2. HR notifies IT of the effective separation time by email.
3. IT records completion and verification evidence in the offboarding ticket.
4. Our systems are Entra ID, Google Workspace, Aeries, and the VPN.
5. Retention, delegated ownership, after-hours coverage, and exception approval are not specified in this policy.
''')
    rows = [
      ('E01','staff-a','2026-10-26T08:00:00Z','US','success'),
      ('E02','staff-b','2026-10-26T09:00:00Z','US','success'),
      ('E03','staff-c','2026-10-26T09:10:00Z','US','failure'),
      ('E04','staff-c','2026-10-26T09:12:00Z','US','failure'),
      ('E05','staff-c','2026-10-26T09:14:00Z','US','failure'),
      ('E06','staff-c','2026-10-26T09:20:00Z','US','success'),
      ('E07','staff-a','2026-10-26T12:00:00Z','CA','success'),
      ('E08','staff-d','2026-10-26T12:15:00Z','CA','failure'),
      ('E09','staff-e','2026-10-26T18:59:00Z','US','success'),
      ('E10','staff-f','2026-10-26T19:00:00Z','US','success'),
      ('E11','staff-g','2026-10-27T06:59:00Z','US','success'),
      ('E12','staff-h','2026-10-27T07:00:00Z','US','success'),
    ]
    with (KIT/'signins.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['event_id','user','timestamp_utc','country','result']); w.writerows(rows)
    # Nmap-shaped XML: invented results only; no network requests are made.
    root=ET.Element('nmaprun', scanner='nmap', args='SYNTHETIC FIXTURE - not an executed command',
      start='1793116800', startstr='Tue Oct 27 16:00:00 2026 UTC', version='7.95', xmloutputversion='1.05')
    root.append(ET.Comment('FICTITIOUS TRAINING DATA. Documentation addresses. Do not scan these addresses.'))
    ET.SubElement(root,'scaninfo',type='connect',protocol='tcp',numservices='9',services='22,80,135,443,445,3389,8080,9100,65000')
    ET.SubElement(root,'scaninfo',type='udp',protocol='udp',numservices='1',services='161')
    ET.SubElement(root,'verbose',level='0'); ET.SubElement(root,'debugging',level='0')
    profiles={0:[(22,'tcp','ssh'),(80,'tcp','http'),(443,'tcp','https')],
              1:[(135,'tcp','msrpc'),(445,'tcp','microsoft-ds'),(3389,'tcp','ms-wbt-server')],
              2:[(80,'tcp','http'),(443,'tcp','https'),(9100,'tcp','jetdirect')],
              3:[(22,'tcp','ssh'),(443,'tcp','https'),(161,'udp','snmp')],
              4:[(22,'tcp','ssh'),(8080,'tcp','http-proxy')]}
    inventory=[]
    for i in range(1,51):
        up=i%10!=0; address=f'192.0.2.{i}'; hostname=f'lab-{i:02d}.example.test'
        host=ET.SubElement(root,'host',starttime='1793116800',endtime='1793116860')
        ET.SubElement(host,'status',state='up' if up else 'down',reason='echo-reply' if up else 'no-response',reason_ttl='0')
        ET.SubElement(host,'address',addr=address,addrtype='ipv4')
        names=ET.SubElement(host,'hostnames'); ET.SubElement(names,'hostname',name=hostname,type='PTR')
        if up:
            ports=ET.SubElement(host,'ports')
            for port,protocol,service in profiles[i%5]:
                p=ET.SubElement(ports,'port',protocol=protocol,portid=str(port))
                ET.SubElement(p,'state',state='open',reason='syn-ack' if protocol=='tcp' else 'udp-response',reason_ttl='0')
                ET.SubElement(p,'service',name=service,method='table',conf='3')
            p=ET.SubElement(ports,'port',protocol='tcp',portid='65000')
            ET.SubElement(p,'state',state='closed',reason='conn-refused',reason_ttl='0')
        inventory.append({'ip':address,'hostname':hostname,'state':'up' if up else 'down',
                          'open_ports':len(profiles[i%5]) if up else 0})
    stats=ET.SubElement(root,'runstats')
    ET.SubElement(stats,'finished',time='1793116860',timestr='Tue Oct 27 16:01:00 2026 UTC',elapsed='60.00',summary='Synthetic fixture: 50 addresses, 45 hosts up',exit='success')
    ET.SubElement(stats,'hosts',up='45',down='5',total='50')
    ET.indent(root,space='  ')
    ET.ElementTree(root).write(KIT/'fictitious-50-hosts.xml',encoding='utf-8',xml_declaration=True)
    (KIT/'malformed-scan.xml').write_text('<nmaprun><host>')
    empty=ET.Element('nmaprun',scanner='nmap',version='7.95',xmloutputversion='1.05')
    ET.SubElement(empty,'verbose',level='0'); ET.SubElement(empty,'debugging',level='0')
    runstats=ET.SubElement(empty,'runstats')
    ET.SubElement(runstats,'finished',time='1793116860',elapsed='0.00',exit='success')
    ET.SubElement(runstats,'hosts',up='0',down='0',total='0')
    ET.ElementTree(empty).write(KIT/'empty-scan.xml',encoding='utf-8',xml_declaration=True)
    (OUT/'answer-key.json').write_text(json.dumps({'scan':{'hosts':50,'up':45,'down':5,'open_ports':125,
       'open_tcp':115,'open_udp':10,'closed_port_records':45,'hosts_with_tcp_3389':10,
       'hosts_with_udp_161':10,'lab_01_open_ports':[135,445,3389]},
       'signins':{'rows':12,'flagged_event_ids':['E06','E07','E10','E11'],
       'reasons':{'E06':'3 preceding failures within 10 minutes, inclusive', 'E07':'outside US baseline',
                  'E10':'outside hours: 19:00 UTC','E11':'outside hours: 06:59 UTC'}},
       'inventory':inventory},indent=2))


SLIDES=[]
def add(time,kind,section,title,items=(),notes='',source='',prompt=None):
    SLIDES.append(dict(time=time,kind=kind,section=section,title=title,items=list(items),notes=notes,source=source,prompt=prompt))

add('00–01','hero','CITE 2026 · TWO-HOUR WORKSHOP','AI for Cyber Security',
    ['From the task you keep postponing to an app you can run.', 'Kevin Riley · kriley@ocde.us'],
    'Welcome. Audience from Intro: K–12 district and county-office IT staff, often teams of one to five. Ask who owns both help desk and security. Promise practice and a working slice, not mastery of every tool.', 'Intro; Close')
add('01–03','cards','THE OUTCOME','Leave with four things',
    [('A working environment','Claude Code in a local workshop folder.'),('A useful document','An offboarding checklist grounded in a policy.'),('Reusable automation','A script that flags known events.'),('A small working app','A web-based Nmap scanner with saved-scan import.')],
    'Everyone uses Claude Code, confirmed by Kevin. The scanner is built with the students in class. No completed scanner is part of this preparation.', 'Talk Outline; user clarifications')
add('03–05','agenda','120 MINUTES','The route through the room',
    [('00–10','Frame the work + guardrails'),('10–25','Hands-on 1 · Get set up'),('25–40','Hands-on 2 · Finish a basic task'),('40–45','Debrief · Make the prompt checkable'),('45–65','Hands-on 3 · Write and test a script'),('65–70','Five-minute break'),('70–80','Skills, agents, and plugins'),('80–110','Hands-on 4 · Build the Nmap web app'),('110–120','Share, Monday plan, and questions')],
    'All times are elapsed from session start. These blocks total exactly 120 minutes. This is a prework-based schedule: the original 55-minute setup cannot fit alongside the app build. Start each hands-on block on time and use pairing when setup is blocked.', 'Talk Outline; Setup Walkthrough')
add('05–07','cards','THE FRAME','You supply the judgment',
    [('Chat','You copy the answer, run it, and check it.'),('Coding agent','It reads files, writes code, runs it, and responds to results.'),('You','Define the goal, approve access, and verify the result.')],
    'Keep the small-team case concrete: work left in the backlog because nobody had time to write a script. Avoid promising a fixed productivity gain. The tool has no knowledge of your environment until you provide context.', 'Intro')
add('07–10','list','BEFORE WE TOUCH THE KEYBOARD','Five rules for every exercise',
    ['Read commands before they change anything.', 'Use the workshop folder and synthetic data.', 'Keep student records and secrets out of prompts.', 'Keep permissions narrow; review proposed actions.', 'Test the result against something you know.'],
    'Demonstrate an approval decision during setup. A scratch folder is not a security boundary: the process still runs with your user permissions. Do not introduce the bypass alias from the old setup as a requirement. Treat file contents as data, including logs and XML. This is workshop practice; district account and data approval remains a local process.', 'Guardrails; Guardrails Checklist')
add('10–12','git-setup','GET THE WORKSHOP FILES','Install Git, then clone the workshop',
    ['https://github.com/OCDEkr/Cite-Talk-2026',
     'git --version\ncd ~/Desktop\ngit clone https://github.com/OCDEkr/Cite-Talk-2026.git\ncd Cite-Talk-2026/scripts/workshop-deck/attendee-kit'],
    'Show the GitHub repository before anyone starts the first exercise. Install Git; clone is a command included with Git. macOS: open Terminal, run xcode-select --install, finish Apple’s Command Line Tools installer, then reopen Terminal. If Homebrew is already installed, brew install git is another option. Windows: download Git for Windows from https://git-scm.com/install/windows, install it (Git Bash is included), then open Git Bash from Start. Run the shared commands in macOS Terminal or Windows Git Bash. git --version must print a version before cloning. HTTPS avoids SSH-key setup; public repositories do not require an attendee GitHub account. If this repository is private, arrange access before class. Do not overwrite an existing clone: open its folder and update deliberately. Before the event, commit and push the attendee-kit folder and verify the public path: the new kit is currently local and untracked. Allow two minutes with Git preinstalled; send installation as prework and pair anyone blocked. If Desktop is unavailable, choose another writable folder. Check that offboarding-policy.txt and prompts.txt are present after the final cd.',
    'User request; https://git-scm.com/install/mac; https://git-scm.com/install/windows; repository origin')
add('12–13','lab','HANDS-ON 1 · 15 MINUTES','Get a working Claude Code session',
    [('DO','Open attendee-kit in a fresh local folder. Start Claude Code there and confirm your account.'),('DONE WHEN','Claude can read the training policy and create a harmless file in this folder.'),('IF BLOCKED','Pair with someone who has a working setup. One drives; one reviews.')],
    'Setup block includes the GitHub/clone introduction, readiness briefing, command checks, work, and checkpoint. Prework must cover Git installation, account access, Nmap, and one runtime. Clone the workshop repository first; no personal repository creation, SSH key, plugin bundle, or editor extension is required.', 'Setup Guide; Setup Walkthrough')
add('13–14','code','SETUP · TERMINAL COMMANDS','Check the minimum, then start',
    ['claude --version\nclaude doctor\nnmap --version\nclaude', '/status\n/permissions'],
    'The first block is terminal commands; the second block is inside Claude Code. Run from the copied attendee-kit folder. Use the existing approved account and confirm the active permission mode rather than assuming defaults. Use /help if a command differs on the installed version. The first two labs need no Python or Node; the script lab uses Python, and the app lab needs Nmap plus the selected runtime.', 'Setup Guide; https://code.claude.com/docs/en/setup; https://code.claude.com/docs/en/permissions')
add('14–23','lab','HANDS-ON 1 · WORK TIME','Create one harmless file',
    [('PROMPT','Read offboarding-policy.txt. Tell me its deadline. Create ready.txt containing only “Ready for the CITE workshop”. Do not change other files.'),('CHECK','Open ready.txt. Confirm that the deadline is 24 hours from the effective separation time.'),('STRETCH','Find how to stop a running response and inspect the permission settings.')],
    'Walk the room. At elapsed 18 minutes ask who is blocked on sign-in, PATH, or permissions. Pair them now. Switch driver after this exercise. Do not let an installation problem become a 30-minute side session.', 'Setup Walkthrough')
add('23–25','checkpoint','CHECKPOINT 1','Ready means you can show it',
    ['A live Claude Code session in the correct folder.', 'A policy read correctly and a file you inspected.', 'An active reviewer if you are working in a pair.'],
    'Ask for hands: ready, paired, blocked. If still blocked, pair before the next lab. No paid account available: review a partner’s session, rather than configuring an untested provider live. Continue at minute 25.', 'Setup Walkthrough')
add('25–28','code','BASIC TASK · PRESENTER DEMO','Turn a policy into a procedure',
    ['Outcome + input + constraints + a checkable output'],
    'Spend three minutes showing the prompt and the file, not waiting for a polished document. Point to a verification/evidence column and a missing policy decision. Do not silently invent retention periods. The short prompt is copied in attendee-kit/prompts.txt.', 'Examples · GRC: policy to procedure', TASK_PROMPT)
add('28–37','lab','HANDS-ON 2 · 9 MINUTES','Make the checklist useful',
    [('DO','Run the policy-to-procedure prompt. Ask one follow-up that improves the result.'),('DONE WHEN','The checklist covers all four systems, roles, verification, and evidence.'),('REVIEW','The 24-hour deadline is preserved. Missing retention and exception rules are marked “decision needed”.')],
    'Goal is a completed basic task before writing code. A good follow-up is “separate policy requirements from suggested operating steps.” Fast finishers ask for a ticket-friendly version. No systems are connected and no messages are sent.', 'Examples; Getting Started')
add('37–40','checkpoint','CHECKPOINT 2','What did you have to correct?',
    ['Show one row you would actually use.', 'Point to one assumption the model made.', 'Keep a suggestion separate from a policy requirement.'],
    'Take two quick responses. If an output invented a retention period, fix it with a follow-up while the room watches. Correctness is more valuable than a polished table.', 'Guardrails · Verify the output')
add('40–43','cards','THE PROMPT PATTERN','Make “done” observable',
    [('Outcome','What should be different when this finishes?'),('Context','Which file and which columns matter?'),('Boundaries','What may it read, write, or run?'),('Acceptance','What result can you independently check?')],
    'Use the checklist task to explain this pattern. Then apply it to the log script: name a schema, set explicit rules, restrict changes, and compare known event IDs. No need for a magic prompt formula.', 'Examples; Guardrails')
add('43–45','list','OTHER TASKS · OPTIONAL PATHS','The same pattern travels',
    ['GRC: compare provided evidence with a vetting form.', 'Blue team: explain an alert and list investigation steps.', 'Code review: inspect a vendor script before running it.', 'Exposure review: turn a scan into a remediation draft.', 'OSINT: assess your own organization’s public information.'],
    'This preserves the breadth of Examples without running every demo. Refer to the existing synthetic scan-report.pdf, the switch config, and the Resource Index. The packet capture is an advanced follow-up; do not unpack or analyze it during the core workshop.', 'Examples; Resource Index; Files/scan-report.pdf; Files/cisco-config.txt.md')
add('45–48','code','SCRIPT LAB · PRESENTER DEMO','From an answer to reusable code',
    ['Inspect schema → write a script → run it → check known results'],
    'Show signins.csv: only 12 synthetic events, in a simplified training schema. These deterministic rules teach validation, not production anomaly detection. UTC is intentional and unrelated to a real district’s workday. Show one source row and an output row.', 'Examples · Blue team: log triage', LOG_PROMPT)
add('48–60','lab','HANDS-ON 3 · 12 MINUTES','Build and test the triage script',
    [('DO','Run the script prompt from prompts.txt. Review the generated code and its run command.'),('DONE WHEN','A reusable Python script produces flagged-events.csv without modifying signins.csv.'),('TEST','Boundary cases: 06:59 / 07:00, 18:59 / 19:00, and a failure exactly ten minutes before success.')],
    'Allow 12 minutes to build and run. Use the Python standard library to avoid package-install friction. If Python is blocked, pair and inspect the code/output with your partner. Fast finishers add a command-line input path and test unsorted input.', 'Examples; Guardrails')
add('60–63','checkpoint','CHECKPOINT 3 · REVEAL AFTER THE RUN','Four events deserve review',
    [('E06','Success after three failures within ten minutes.'),('E07','Success outside the US training baseline.'),('E10','19:00 UTC: outside the training window.'),('E11','06:59 UTC: outside the training window.')],
    'Expected unique flagged IDs: E06, E07, E10, E11. E09 at 18:59 and E12 at 07:00 must not be flagged. E08 is a failure outside the US; the country rule applies only to successes. Compare exact IDs, not only a count of four. Use answer-key.json for the complete check.', 'Synthetic signins.csv; answer-key.json')
add('63–65','list','DEBRIEF','A flag is a question to investigate',
    ['What evidence caused each flag?', 'Which normal behaviors could trigger it?', 'What would you need before using this on real logs?'],
    'Discuss VPNs, travel, timezone and work schedules, real export schemas, approved data handling, and historical baselines. This exercise does not establish compromise and cannot detect impossible travel. Reuse the code after adapting and verifying its rules, not by assuming the training rules are operationally valid.', 'Guardrails; Examples')
add('65–70','hero','FIVE-MINUTE BREAK','Stand up. Come back at minute 70.',
    ['Save your work.', 'After the break: make the workflow reusable, then build the app.'],
    'Hold the full break. Display a return time based on the actual session start. If earlier tasks ran long, cut optional demos and stretch features before cutting this break or the app exercise.', 'Workshop timing')
add('70–73','cards','SKILLS, AGENTS, AND PLUGINS','Three ways to extend the workflow',
    [('Skill','Instructions for a task you repeat.'),('Agent','A delegated job with its own context and tools.'),('Plugin','A package of skills, agents, hooks, or connectors.')],
    'Keep the teaching order from the original notes. The GRC zip is an existing real example of packaging: .claude-plugin/plugin.json plus skills/grc-assessment/SKILL.md. Mention it without installing it in every student environment.', 'Skills Agents Plugins; Skills/Grc assessment-v4.zip')
add('73–76','code','MINI PRACTICE · 3 MINUTES','Write the review habit down',
    ['.claude/skills/verify-output/SKILL.md', '---\nname: verify-output\ndescription: Verify workshop output against known evidence.\n---\nRead the source and the proposed result.\nIdentify the assumptions and check the totals.\nReturn evidence, discrepancies, and the next check.\nDo not change source data.'],
    'Optional three-minute pair practice within the ten-minute extension block: create this project skill, then try /verify-output on the log task. Use the description and source files as context. A skill is instructions, not a security boundary. If the room needs recovery time, demonstrate this once and let attendees copy it later.', 'https://code.claude.com/docs/en/skills; Skills Agents Plugins')
add('76–78','cards','PERMISSIONS MATTER','A narrow brief needs narrow tools',
    [('Read-only review','Use Read, Glob, and Grep for a reviewer that does not need a shell.'),('Code execution','Bash can write and delete files. Removing Edit does not make Bash read-only.'),('Plugins','Review the code and permissions before adding a package.')],
    'Corrects a concrete error in the existing agent slide and notes, which claim that tools: Read, Bash, Grep cannot edit or delete files. Shell commands can do both. Do not repeat this claim. A tool allowlist also does not replace operating-system isolation.', 'https://code.claude.com/docs/en/sub-agents; https://code.claude.com/docs/en/permissions')
add('78–80','list','EXTENSIONS · WHAT TO DO NEXT','One useful extension at a time',
    ['Repeat a task? Write a small skill.', 'Need a separate reviewer? Define a narrow agent.', 'Ready to share? Package what works.', 'Browse the Resource Index after the workshop.'],
    'No mass plugin installation in the core 120 minutes. Keep ECC, Humanizer, design plugins, Hermes, and herdr in optional resources. Exact marketplace names, model names, limits, and pricing change; use their current official documentation when choosing them.', 'Skills Agents Plugins; Resource Index; Cheat Sheets')
add('80–82','hero','HANDS-ON 4 · 30 MINUTES','Build a web-based Zenmap clone',
    ['A working scanner: browser → local backend → Nmap.', 'Import the 50-machine scan to test the interface.'],
    'Kevin clarified that this is a working scanner, built together with students in class. Saved scans are a test fixture, not a replacement for scanning. Bound the first version; reproducing all Zenmap features is beyond a 30-minute exercise.', 'Application Builds; user clarifications; https://nmap.org/book/zenmap.html')
add('82–84','code','APP BUILD · YOUR ORIGINAL PROMPT','Let it plan and ask questions',
    [],
    'Use the existing prompt exactly as written in Application Builds. Send it in a fresh app project and let students watch research and questions happen. Have the scope answers on the next slide ready. Use a model available to the class rather than relying on a hardcoded version number. Full prompts are in attendee-kit/prompts.txt.', 'Application Builds · Demo 1', ORIGINAL_PROMPT)
add('84–86','cards','ANSWER THE QUESTIONS · THEN BUILD','Agree on the first working slice',
    [('Interface','Target, fixed profile, Scan button, status, raw output, hosts, ports, services.'),('Engine','A local backend invokes the installed Nmap executable.'),('Live target','Start with 127.0.0.1 only; instructor authorizes any wider lab scope.'),('Saved data','Import Nmap XML with 50 fictitious hosts through the same result model.')],
    'Paste the app scope follow-up from prompts.txt after the initial planning questions. Use a simple local stack. Validate target and fixed profile on the backend, use an argument array, set a timeout, and bind to 127.0.0.1. No shell command concatenation, arbitrary flags, NSE, database, or deployment. A loopback TCP connect scan needs no OS detection or root. Browser-only code cannot execute Nmap: the backend is essential.', 'Application Builds; attendee-kit/prompts.txt')
add('86–100','lab','HANDS-ON 4 · BUILD TIME','Plan → build → launch → inspect',
    [('FIRST','Approve a small plan. Build the backend, scan action, and result views.'),('THEN','Import fictitious-50-hosts.xml and inspect host details.'),('CHECK IN','At minute 93: app starts. At minute 97: import works. At minute 100: scan action is wired.')],
    '14 minutes of focused build time. Students drive; presenter circulates or builds in parallel on screen. The scanner is not prebuilt for them. Aim for the smallest usable version and accept basic styling. If model latency is high, pair at one machine; if needed demonstrate the incomplete step and carry finishing instructions into take-home work. Do not pretend a saved-data-only app is complete.', 'Application Builds; user clarifications')
add('100–103','checkpoint','FIXTURE CHECK · 50 MACHINES','Does the import tell the truth?',
    [('50 total','45 up · 5 down'),('125 open ports','115 TCP · 10 UDP'),('45 closed records','Keep them out of the open count.'),('Spot checks','lab-01: 135, 445, 3389 TCP. Ten hosts expose 3389; ten expose 161 UDP.')],
    'Counts refer to port records across hosts, not distinct port numbers or vulnerabilities. Check 50 unique IPv4 addresses. Documentation addresses 192.0.2.1–50 are fixture data only; do not use them as scan targets. Missing OS or version data should be unknown, not invented. Do not label an open port as a verified vulnerability. Optional error checks: empty-scan.xml imports as zero hosts; malformed-scan.xml gives an error.', 'attendee-kit/fictitious-50-hosts.xml; answer-key.json')
add('103–107','list','LIVE CHECK · THE APP REALLY SCANS','Run Nmap from the web interface',
    ['Confirm Nmap is installed on the backend machine.', 'Use target 127.0.0.1 with the fixed TCP connect profile.', 'Click Scan; watch the real running and completed states.', 'Compare the displayed result with the captured Nmap output.', 'Confirm another target or injected flag is rejected.'],
    'A loopback scan may find no open ports, which is a valid result. To see a known open port, use an instructor-prepared loopback listener on a port in the fixed list; do not assume a service exists. A command-line Nmap run alone does not prove the web scan path works. Missing executable, nonzero exit, and timeout should produce a useful error. Broader scanning requires an explicitly authorized target and a deliberate backend allowlist change.', 'Application Builds; Guardrails')
add('107–110','checkpoint','CHECKPOINT 4','Show the whole path working',
    ['The browser launches a real Nmap scan through the backend.', 'Saved-scan import matches the 50-host answer key.', 'A host selection shows correct ports and services.', 'You can explain one validation rule and one limitation.'],
    'Ask for a 30-second show-and-tell from one pair. If a team has only import working, name the remaining backend scan work clearly. Stretch goals after the session: another fixed profile, scan history, comparison, topology, and improved layout. Do not burn verification time polishing the screen.', 'Application Builds; Guardrails')
add('110–113','cards','SHARE BACK','What changed in your approach?',
    [('Show','One useful output or one bug you caught.'),('Explain','Which evidence convinced you it worked?'),('Transfer','Which district task could use the same workflow?')],
    'Three minutes, two or three brief shares. Praise checking the work rather than the number of lines generated. Keep an unanswered-question list so the final Q&A stays useful.', 'Getting Started; Close')
add('113–115','hero','MONDAY','One task. One hour.',
    ['Low stakes. Repetitive. Easy to check.', 'Record the time spent and what you had to correct.'],
    'Use a scratch folder or an approved copy of data. Repeat before making a time-savings claim. For team adoption, use the evidence from a small pilot, approved account/data rules, and a shared review habit.', 'Getting Started; Close')
add('115–116','list','TAKE THE MATERIAL WITH YOU','Keep the prompts and the checks',
    ['attendee-kit.zip · sample inputs + all exercise prompts', 'Facilitator Guide.txt · timing, source analysis, and recovery paths', 'Existing notes · Setup Guide, Guardrails Checklist, Resource Index', 'github.com/OCDEkr/Cite-Talk-2026'],
    'The local attendee zip is prepared but has not been published to the repository. Verify the handout distribution link before the session; the repository URL comes from the existing materials. Bring an offline copy for file sharing if conference Wi-Fi fails.', 'Close; Resource Index; existing repository URL')
add('116–120','hero','QUESTIONS','What would you want it to do first?',
    ['Kevin Riley · kriley@ocde.us', 'A fast junior analyst: capable, tireless, and never trusted blind.'],
    'Reserve four minutes for Q&A. If no hands go up, ask which unfinished backlog item feels small enough to try Monday. Finish at elapsed 120 minutes.', 'Close')

CORE=len(SLIDES)
add('APPENDIX','list','PREWORK · SEND ONE WEEK AHEAD','Arrive ready to build',
    ['Install Git and Claude Code; confirm approved account access.', 'Install Nmap separately; verify nmap --version.', 'Have Python 3 for the script lab and the selected app runtime.', 'Clone the workshop repository; locate the attendee-kit folder.', 'Bring a laptop permitted to run these tools, or plan to pair.'],
    'Presenter preflight: choose and rehearse one simple app stack so dependency installation is not improvised. Check current OS-specific Nmap install instructions from nmap.org/download; do not distribute Nmap binaries. Test on the Windows and macOS paths expected in the room. Check model/account availability, venue network rules, and permission modes. Runtime downloads, GitHub setup, and drivers can exceed the setup window. Ask registrants to complete the prework; pair anyone blocked.', 'Setup Walkthrough; Setup Guide; https://nmap.org/download')
add('APPENDIX','code','INSTALL REFERENCE · IF NEEDED','Use the current official installer',
    ['macOS / Linux / WSL\ncurl -fsSL https://claude.ai/install.sh | bash', 'Windows PowerShell\nirm https://claude.ai/install.ps1 | iex'],
    'These are current official Claude Code install commands, verified while preparing the deck. They execute a downloaded installer: use the official documentation and your organization’s software policy. Reopen the terminal afterward, then run claude --version and claude doctor. Nmap and Python are separate prerequisites. This is a reference slide, not a requirement to install everything live.', 'https://code.claude.com/docs/en/setup')
add('APPENDIX','list','IF YOU HAVE MORE TIME','Optional demos from your materials',
    ['GRC: inspect the packaged grc-assessment skill.', 'Exposure review: use the fictitious PDF or Nessus report.', 'Config review: inspect the supplied Cisco config.', 'Advanced follow-up: packet capture analysis.', 'Workflow tools: Claude Code, Hermes, and herdr cheat sheets.'],
    'The existing Nessus file has 57 ReportHost records and 215 ReportItem records; it is not Nmap XML and is not the new 50-machine fixture. Do not expect it to import into the first app version. The PCAP archive was inventoried only, not executed or analyzed. These are optional material, not extra core exercises.', 'Files; Skills/Grc assessment-v4.zip; Cheat Sheets')
add('APPENDIX','list','RECOVERY PLAN','Keep the room moving',
    ['Blocked install or login → pair; switch driver next lab.', 'Slow model → narrow the request and share one session.', 'Broken script → compare one event and one boundary.', 'Broken app → inspect the failing layer: browser, backend, Nmap.', 'Short on time → drop stretch features; keep the checks.'],
    'If behind by five minutes, demonstrate the skill mini practice and omit optional breadth discussion. Protect the break, the real scan verification, and the finish. If the build cannot complete in the slot, show exactly what works and what remains; do not claim a finished scanner. Presenter should rehearse a known working reference build before the event as a contingency, but no scanner is built or delivered as part of this task.', 'Setup Walkthrough; workshop design')
add('APPENDIX','list','APP EXTENSIONS · AFTER THE WORKSHOP','Earn the next feature',
    ['Add one fixed profile and validate its result.', 'Save and compare scans; show what changed.', 'Add topology only when host relationships are available.', 'Plan access controls before any shared deployment.', 'Review dependencies, scope, and resource limits before wider use.'],
    'This is a classroom prototype. A useful scanner requires a backend; a local binding alone does not validate requests or replace target authorization. Future distribution of Nmap-related software needs an appropriate license review using the project’s current terms. Do not put a public unauthenticated scanner on a network. No production deployment is part of this workshop.', 'Application Builds; https://nmap.org/book/zenmap.html')
add('APPENDIX','list','REFERENCES','Start with the source material',
    ['Workshop notes: Intro, Guardrails, Setup, Examples, Skills, Application Builds, Getting Started, Close.', 'Claude Code: setup, skills, subagents, permissions.', 'Nmap: XML output and Zenmap GUI user guide.', 'Detailed links and source decisions are in the facilitator guide.'],
    'Official links: https://code.claude.com/docs/en/setup ; https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/permissions ; https://nmap.org/book/output-formats-xml-output.html ; https://nmap.org/book/zenmap.html . No hardcoded pricing, named model version, unverified September threat report, or quantified time-savings claim is carried into this deck.', 'Sources; official documentation')


# A shared drawing layer creates editable PowerPoint and a matched PDF proof.
BG='#FFFFFF'; FG='#111111'; MUTED='#454B53'; ACCENT='#155191'; PANEL='#EFF4FA'
LOGO=Path(__file__).resolve().parent.parent/'Files'/'Mark-Title-COLOR-ForLightBG.png'
DECK_NAME='CITE-AI-Workshop-High-Contrast'
# Section openings use black; all remaining slides use white.
SECTION_STARTS={1,5,6,10,13,15,19,20,24,31,35}
SLIDE_ICONS={2:['terminal','file','code','scan'],4:['chat','code','person'],
    5:['eye','folder','lock','shield','check'],9:['terminal','file','person'],
    12:['eye','chat','check'],13:['target','file','shield','check'],
    14:['file','shield','eye','scan','globe'],18:['eye','chat','check'],
    20:['file','person','package'],22:['eye','code','package'],
    23:['file','person','package','book'],26:['window','code','target','folder'],
    29:['terminal','target','scan','eye','shield'],30:['scan','folder','eye','shield'],
    31:['eye','chat','target'],33:['folder','book','file','globe'],
    35:['terminal','scan','code','folder','person'],37:['file','scan','eye','code','book'],
    38:['person','chat','code','scan','check'],39:['scan','folder','globe','shield','check'],
    40:['book','terminal','scan','file']}
# Account for the new repository/download slide before the first lab.
SECTION_STARTS={n+1 if n>=6 else n for n in SECTION_STARTS}
SLIDE_ICONS={n+1 if n>=6 else n:icons for n,icons in SLIDE_ICONS.items()}
prs=Presentation(); prs.slide_width=Inches(13.333333); prs.slide_height=Inches(7.5)
prs.core_properties.title='AI for Cyber Security — CITE hands-on workshop'
prs.core_properties.author='Kevin Riley'
pdf=fitz.open()
class Canvas:
    def __init__(self,dark=False):
        self.slide=prs.slides.add_slide(prs.slide_layouts[6]); self.page=pdf.new_page(width=960,height=540)
        self.dark=dark
        self.slide.background.fill.solid()
        self.slide.background.fill.fore_color.rgb=RGBColor.from_string('000000' if dark else 'FFFFFF')
        self.rect(0,0,960,540,'#000000' if dark else BG)
    def color(self,color):
        if self.dark:
            return {FG:'#FFFFFF',MUTED:'#D3D7DD',PANEL:'#151515'}.get(color,color)
        return color
    def rect(self,x,y,w,h,color):
        color=self.color(color)
        from pptx.enum.shapes import MSO_SHAPE
        s=self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x/72), Inches(y/72), Inches(w/72), Inches(h/72))
        s.fill.solid(); s.fill.fore_color.rgb=RGBColor.from_string(color[1:]); s.line.fill.background()
        self.page.draw_rect(fitz.Rect(x,y,x+w,y+h),color=None,fill=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)))
    def text(self,text,x,y,w,h,size=22,color=FG,style='regular'):
        color=self.color(color)
        # Keep the logo blue as a graphic accent on black while using white text.
        if self.dark and color==ACCENT: color='#FFFFFF'
        font=ImageFont.truetype(str(FONTS[style]),size*4)
        lines=[]
        for para in text.split('\n'):
            if not para: lines.append(''); continue
            line=''
            for word in para.split(' '):
                candidate=(line+' '+word).lstrip()
                if font.getlength(candidate)/4>w and line:
                    lines.append(line); line=word
                else: line=candidate
            lines.append(line)
        lh=size*1.22
        if len(lines)*lh>h+1:
            raise ValueError(f'Text overflow: {text[:60]!r}: {len(lines)*lh:.1f} > {h}')
        for j,line in enumerate(lines):
            if not line: continue
            box=self.slide.shapes.add_textbox(Inches(x/72),Inches((y+j*lh)/72),Inches(w/72),Inches(lh/72))
            tf=box.text_frame; tf.clear(); tf.word_wrap=False
            tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
            p=tf.paragraphs[0]; p.text=line
            p.font.name='Andale Mono' if style=='mono' else 'Arial'
            p.font.size=Pt(size); p.font.bold=style=='bold'; p.font.color.rgb=RGBColor.from_string(color[1:])
            p.space_before=Pt(0); p.space_after=Pt(0)
            name={'regular':'WorkshopRegular','bold':'WorkshopBold','mono':'WorkshopMono'}[style]
            self.page.insert_font(fontname=name,fontfile=str(FONTS[style]))
            self.page.insert_text((x,y+j*lh+size*.94),line,fontsize=size,fontname=name,
                color=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)))
    def line(self,x1,y1,x2,y2,color=ACCENT,width=1.8):
        from pptx.enum.shapes import MSO_CONNECTOR
        shape=self.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
            Inches(x1/72),Inches(y1/72),Inches(x2/72),Inches(y2/72))
        shape.line.color.rgb=RGBColor.from_string(color[1:]); shape.line.width=Pt(width)
        self.page.draw_line((x1,y1),(x2,y2),color=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)),width=width)
    def outline(self,x,y,w,h,oval=False,color=ACCENT,width=1.8):
        from pptx.enum.shapes import MSO_SHAPE
        shape=self.slide.shapes.add_shape(MSO_SHAPE.OVAL if oval else MSO_SHAPE.RECTANGLE,
            Inches(x/72),Inches(y/72),Inches(w/72),Inches(h/72))
        shape.fill.background(); shape.line.color.rgb=RGBColor.from_string(color[1:]); shape.line.width=Pt(width)
        rgb=tuple(int(color[i:i+2],16)/255 for i in (1,3,5))
        if oval: self.page.draw_oval(fitz.Rect(x,y,x+w,y+h),color=rgb,width=width)
        else: self.page.draw_rect(fitz.Rect(x,y,x+w,y+h),color=rgb,width=width)
    def icon(self,name,x,y,size=29):
        """Small original line icons, kept as editable PowerPoint geometry."""
        color='#FFFFFF' if self.dark else ACCENT
        # Icon paths use a 24-unit grid.
        def line(a,b,c,d): self.line(x+a*size/24,y+b*size/24,x+c*size/24,y+d*size/24,color)
        def box(a,b,w,h,oval=False): self.outline(x+a*size/24,y+b*size/24,w*size/24,h*size/24,oval,color)
        if name=='terminal':
            box(2,3,20,17); line(6,8,10,11); line(10,11,6,14); line(13,15,18,15)
        elif name=='code':
            line(8,6,2,12); line(2,12,8,18); line(16,6,22,12); line(22,12,16,18); line(14,3,10,21)
        elif name=='check':
            box(2,2,20,20,True); line(6,12,10,16); line(10,16,18,8)
        elif name=='eye':
            for a,b,c,d in [(1,12,7,6),(7,6,17,6),(17,6,23,12),(23,12,17,18),(17,18,7,18),(7,18,1,12)]: line(a,b,c,d)
            box(9,9,6,6,True)
        elif name=='folder':
            for a,b,c,d in [(2,5,10,5),(10,5,13,8),(13,8,22,8),(22,8,22,20),(22,20,2,20),(2,20,2,5)]: line(a,b,c,d)
        elif name=='file' or name=='book':
            box(4,2,16,20); line(8,8,16,8); line(8,12,16,12); line(8,16,14,16)
            if name=='book': line(7,2,7,22)
        elif name=='shield':
            for a,b,c,d in [(3,4,12,1),(12,1,21,4),(21,4,20,15),(20,15,12,22),(12,22,4,15),(4,15,3,4)]: line(a,b,c,d)
            line(7,11,11,15); line(11,15,17,8)
        elif name=='lock':
            box(4,10,16,12); box(7,2,10,12,True); line(12,15,12,18)
        elif name=='target' or name=='scan' or name=='globe':
            box(2,2,20,20,True)
            if name=='target': box(7,7,10,10,True); line(12,12,21,3)
            elif name=='scan':
                line(12,12,19,5); line(12,2,12,22); line(2,12,22,12); box(7,7,10,10,True)
            else: box(7,2,10,20,True); line(2,12,22,12)
        elif name=='person':
            box(8,1,8,8,True); line(3,22,3,17); line(3,17,8,12); line(8,12,16,12); line(16,12,21,17); line(21,17,21,22)
        elif name=='chat':
            box(2,3,20,15); line(6,18,6,23); line(6,23,12,18); line(7,8,17,8); line(7,12,14,12)
        elif name=='package':
            box(3,4,18,17); line(3,9,21,9); line(10,4,10,13); line(14,4,14,13)
        elif name=='window':
            box(2,3,20,18); line(2,8,22,8); line(5,5.5,6,5.5); line(8,5.5,9,5.5)
    def branding(self,num):
        if num==1: return
        # Use the new light-background logo everywhere. White slides need no box;
        # black section slides get a white backing to preserve wordmark contrast.
        if self.dark: self.rect(679,490,243,48,'#FFFFFF')
        shape=self.slide.shapes.add_picture(str(LOGO),Inches(690/72),Inches(497/72),width=Inches(220/72))
        shape.name='OCDE logo watermark'
        self.page.insert_image(fitz.Rect(690,497,910,497+220*369/2000),filename=str(LOGO))

def render():
    for num,s in enumerate(SLIDES,1):
        c=Canvas(num in SECTION_STARTS); kind=s['kind']; items=s['items']
        c.text(s['section'],48,30,760,26,12,ACCENT,'bold')
        c.text(s['time'],810,30,104,26,12,MUTED)
        c.rect(48,506,608,1,'#7F8792' if c.dark else '#CCD2DA')
        c.text('CITE 2026  /  AI FOR CYBER SECURITY',48,516,650,18,9,MUTED)
        c.text(f'{num:02d}' + ('  /  EXTRA' if num>CORE else ''),572,516,95,18,9,MUTED)
        c.rect(48,62,56,4,ACCENT)
        icons=SLIDE_ICONS.get(num,[])
        if kind=='hero':
            c.rect(48,110,6,190,ACCENT)
            c.text(s['title'],76,130,810,145,45,FG,'bold')
            for j,item in enumerate(items): c.text(item,76,310+j*62,800,62,23 if j==0 else 19,MUTED)
        else:
            c.text(s['title'],48,77,864,101,33,FG,'bold')
            if kind=='git-setup':
                c.text(items[0],48,153,864,32,23,ACCENT,'bold')
                for x,title,body in [
                    (48,'MAC · TERMINAL','xcode-select --install\nFinish the installer; reopen Terminal.\nAlready have Homebrew? brew install git'),
                    (489,'PC · GIT BASH','git-scm.com/install/windows\nInstall Git for Windows (includes Git Bash).\nOpen Git Bash from the Start menu.')]:
                    c.rect(x,201,423,130,PANEL)
                    c.text(title,x+16,213,391,29,17,ACCENT,'bold')
                    c.text(body,x+16,249,391,77,15)
                c.text('BOTH · CHECK GIT, THEN RUN THESE COMMANDS',48,342,864,23,12,ACCENT,'bold')
                c.rect(48,369,864,112,PANEL)
                c.text(items[1],64,376,832,102,16,FG,'mono')
            elif kind=='cards':
                n=len(items); gap=18; width=(864-gap*(n-1))/n
                for j,(head,body) in enumerate(items):
                    x=48+j*(width+gap); c.rect(x,204,width,251,PANEL)
                    if icons: c.icon(icons[j%len(icons)],x+17,219,29)
                    c.text(head,x+17,261 if icons else 225,width-34,76,22 if icons else 23,ACCENT,'bold')
                    c.text(body,x+17,337 if icons else 306,width-34,112 if icons else 135,18 if icons else 19)
            elif kind=='agenda':
                for j,(clock,label) in enumerate(items):
                    y=184+j*33; c.text(clock,48,y,110,31,17,ACCENT,'bold'); c.text(label,174,y,735,31,18)
            elif kind=='lab':
                for j,(head,body) in enumerate(items):
                    y=192+j*99
                    c.icon(['code','check','eye'][j],48,y,25)
                    c.text(head,86,y,105,30,12,ACCENT,'bold'); c.text(body,203,y-3,700,92,23)
            elif kind=='checkpoint' and items and isinstance(items[0],tuple):
                for j,(head,body) in enumerate(items):
                    y=190+j*76; c.text(head,48,y,230,67,23,ACCENT,'bold'); c.text(body,296,y,615,69,21)
            elif kind=='code':
                if s['prompt']:
                    p=s['prompt']
                    # Keep long lab prompts in handout and notes; slides show an excerpt.
                    if p==LOG_PROMPT:
                        p='Read signins.csv. Write and run a reusable Python script.\n\nFlag successful sign-ins outside the training hours, outside the US baseline, or after three failures in ten minutes.\n\nPreserve the input. Save event IDs and reasons. Test the boundaries.'
                    c.rect(48,191,864,246,PANEL); c.text(p,68,209,824,212,21 if p==ORIGINAL_PROMPT else 19)
                    c.text(items[0] if items else 'Copy the original prompt from attendee-kit/prompts.txt.',48,456,860,42,15,MUTED)
                else:
                    y=188
                    for item in items:
                        size=17 if len(item)>180 else 20
                        h=210 if len(item)>180 else 127 if '\n' in item else 47
                        c.rect(48,y,864,h,PANEL); c.text(item,65,y+12,830,h-16,size,FG,'mono'); y+=h+16
            else:
                size=24 if len(items)<=4 else 22
                step=76 if len(items)<=4 else 60
                for j,item in enumerate(items):
                    y=191+j*step
                    if icons: c.icon(icons[j%len(icons)],51,y-3,29)
                    else: c.text(f'{j+1:02d}',48,y,45,32,14,ACCENT,'bold')
                    c.text(item,115,y-4,793,step-5,size)
        c.branding(num)
        # Full prompts and sources are accessible in the editable deck's speaker notes.
        c.slide.notes_slide.notes_text_frame.text=(f"ELAPSED: {s['time']}\n\n{s['notes']}\n\n"+
            (f"FULL PROMPT\n{s['prompt']}\n\n" if s['prompt'] else '')+f"SOURCE: {s['source']}")
    prs.save(OUT/f'{DECK_NAME}.pptx')
    pdf.save(OUT/f'{DECK_NAME}.pdf',garbage=4,deflate=True)


def supporting_files():
    prompts=f'''CITE 2026 — EXERCISE PROMPTS
All data in this kit is invented. Everyone uses Claude Code.
The web-based scanner will be built together in class; no finished scanner is included.

LAB 1 — SETUP CHECK
Read offboarding-policy.txt. Tell me its deadline. Create ready.txt containing only "Ready for the CITE workshop". Do not change other files.

LAB 2 — BASIC TASK
{TASK_PROMPT}

LAB 3 — REUSABLE SCRIPT
{LOG_PROMPT}

LAB 4 — START WITH KEVIN'S EXISTING PROMPT
{ORIGINAL_PROMPT}

LAB 4 — SCOPE ANSWERS / FOLLOW-UP AFTER PLANNING QUESTIONS
{APP_BRIEF}

LAB 4 — VERIFY IT
Import fictitious-50-hosts.xml. Check 50 unique hosts: 45 up, 5 down. Check 125 open port records: 115 TCP, 10 UDP. Do not count the 45 closed records as open.
Select lab-01.example.test: 135/tcp, 445/tcp, 3389/tcp must be open. Search for port 3389: ten hosts. Search for UDP 161: ten hosts. Inspect one down host, such as 192.0.2.10. Do not invent service versions or OS values.
Import malformed-scan.xml: show a useful error. Import empty-scan.xml: zero hosts without crashing.
Run a REAL scan through the web interface against the instructor-authorized target, initially 127.0.0.1. Compare the actual result and raw Nmap output. Try an invalid target or extra flag: the backend must reject it. Test missing Nmap and a timeout if time permits.
Saved-scan import alone does not complete the scanner exercise. Do not scan the documentation addresses in the fixture.
'''
    (KIT/'prompts.txt').write_text(prompts)
    (KIT/'START-HERE.txt').write_text('''CITE 2026 — ATTENDEE KIT

1. Install Git and clone https://github.com/OCDEkr/Cite-Talk-2026.git. Open scripts/workshop-deck/attendee-kit inside the clone and start Claude Code there. Use this zip as a fallback if cloning is blocked.
2. Follow prompts.txt alongside the slides. Keep approval decisions visible and inspect the result.
3. All provided inputs are synthetic. Do not substitute student records, real credentials, or district data.
4. Prework: working Claude Code/account; Python 3 for the script lab; Nmap and the instructor-selected runtime for the app lab. Verify claude --version and nmap --version.
5. Blocked by installation or login? Pair with a classmate and switch driver between exercises.

FILES
offboarding-policy.txt — policy for the basic task.
signins.csv — 12 events in a simplified training schema; UTC is used for explicit workshop rules.
fictitious-50-hosts.xml — Nmap-shaped XML with 50 invented machines; five are down. Includes TCP, UDP, and closed ports to test the app's import logic. No scan was run to produce this file.
empty-scan.xml / malformed-scan.xml — import-error test inputs.
prompts.txt — prompts and the app acceptance checks.

The app is a WORKING web-based Zenmap-style Nmap scanner, built together in class. Saved-scan import is one feature. The kit contains no finished scanner. Real scanning starts with an explicitly authorized target, 127.0.0.1. Fixture addresses are data, not scan targets. Do not scan the conference network.
''')
    source_analysis='''CITE WORKSHOP — FACILITATOR GUIDE
Prepared from the existing folder and Kevin's clarifications on 2026-11-10.

DELIVERABLE AND SCOPE
An editable PowerPoint plus a matched PDF proof, presenter notes on every slide, and an attendee kit. Everyone uses Claude Code. The app is a working web-based Zenmap clone that invokes Nmap, built together with students during class. The new 50-machine XML file tests saved-scan import and display alongside live scanning. No scanner is built or supplied here.

ANALYSIS OF THE EXISTING MATERIAL
- Talk Outline.md: strong eight-part narrative, with guardrails correctly ahead of demos. Kept the arc and replaced long presentation stretches with explicit work/checkpoint cycles.
- Existing Cite-AI-Talk.pptx: 55 slides. Useful lecture baseline, but the setup slide itself allocates about 55 minutes, too much for the requested two-hour workshop with app-building time. Replaced in a new file, leaving the original untouched.
- Intro.md: clear audience (K–12 district/county IT teams of one to five) and useful junior-analyst frame. Condensed to avoid delaying practice. Omitted unsupported order-of-magnitude productivity claims and the dated threat-report claim.
- Guardrails.md / Guardrails Checklist.md: retained all five habits, expressed as choices students practice. The bypass-permissions alias and passphrase-free SSH-key setup are not dependencies of this workshop.
- Setup Guide.md / Setup Walkthrough.md: valuable full install reference. Converted most installs to prework. Added a GitHub/install/clone slide before the first lab. In-session minimum is a cloned attendee-kit folder, account, Claude Code, and a visible file check. Personal repository creation, SSH, gh, editor extensions, and provider-routing setup are optional follow-up.
- Examples.md: retained policy-to-procedure and log triage as core exercises. GRC, exposure review, code review, detection queries, and OSINT remain a brief menu. The original anomaly prompt needs history/coordinates and operational definitions; the lab uses explicit, checkable training rules instead.
- Skills Agents Plugins.md: retained smallest-to-largest explanation and a three-minute skill practice. Corrected the claim that an agent with Bash but no Edit tool cannot write/delete files. Moved plugin installs and marketplace comparisons out of the timed core.
- Application Builds.md: preserved Kevin's original Nmap/Zenmap prompt verbatim. Use it first, then answer the generated questions with the scope brief. Requires BOTH real backend scanning and saved XML import. Target/profile controls are part of the build and review, not an unrelated feature.
- Getting Started.md / Close.md: compressed the action into one task, one hour, a small pilot, and evidence. Removed hardcoded pricing and model names so the deck does not depend on them.
- Cite Talk Guide.html / Cite Talk Guide.src.html: existing broader handout; index, setup, examples, and resources overlap the notes. Left intact. The new prompts.txt is the exact workshop companion and overrides conflicting workshop setup assumptions.
- Sources.md / Resource Index.md: retained as longer reading. Rechecked the technical points used in this deck against official Claude Code and Nmap documentation. Did not promote every listed tool into a recommendation.
- Files/cisco-config.txt.md: useful short config-review follow-up, not another core lab.
- Files/scan-report.pdf: 15-page fictitious Nessus vulnerability report, useful exposure-report demo.
- Files/scan-report.nessus: 57 ReportHost records and 215 ReportItem records; a different format from Nmap. The app exercise does not require Nessus import.
- Skills/Grc assessment-v4.zip: manifest plus grc-assessment skill. Evidence-focused real-world example for extensions; inspected as source material, not installed or executed.
- Files/2026-09-29-Macfinger-ClickFix-activity.pcap.zip: inventoried as an advanced artifact only. Not unpacked, executed, or packet-analyzed; packet analysis is outside the core session.
- Cheat Sheets: Claude Code, Hermes Agent, and herdr PDFs inspected. Claude Code is the class tool; the others are optional takeaways. Avoid teaching all toolchains in one slot.
- Existing scripts: cheat-sheet generators, not workshop requirements. Preserved.

TIMING AND TEACHING PLAN
00–10   Opening, outcomes, agenda, and five guardrails (10 minutes)
10–25   GitHub, Git installation/clone instructions, hands-on 1 setup + readiness check (15)
25–40   Hands-on 2: policy → checklist + debrief (15)
40–45   Prompt pattern and examples menu (5)
45–65   Hands-on 3: reusable log script + tests + debrief (20)
65–70   Break (5)
70–80   Skills, agents, plugins; brief skill practice (10)
80–110  Hands-on 4: plan/build/import/real scan/verify (30)
110–120 Share-back, Monday action, handouts, Q&A (10)
TOTAL   120 minutes. Appendix slides have no allocated session time.

App block: 80–86 brief + original prompt + plan/questions; 86–100 build; 100–103 import test; 103–107 live scanner test; 107–110 completion and debrief. This is an aggressive first-slice build, not full Zenmap feature parity. Have the environment ready, choose a simple stack, and rehearse the workflow before the event. Cut topology, arbitrary profiles, database/history, polish, and deployment first. Never call import-only output a finished scanner.

PREWORK / PRESENTER PREFLIGHT
Send the kit and setup instructions one week ahead. Require Git, a working approved Claude Code account, installed Nmap, Python 3, and the selected app runtime. Rehearse the Windows/macOS paths expected in the room. Pick a simple backend stack beforehand and pre-cache its dependencies. Do not spend class time installing multiple language toolchains. The attendee kit must be committed and pushed before presenting the clone path; it is currently local and untracked.
Verify claude --version, claude doctor, nmap --version, and the account with /status. Confirm the active permission settings; defaults may vary by version/admin policy. Leave review decisions visible. Validate that the backend can find the Nmap executable on each platform.
Preselect a fixed TCP port list and confirm a loopback-only live test. If you want a known open port, prepare an authorized loopback listener on one of those ports. No open ports is still a valid scan result. Never silently broaden targets to the venue network or use the fixture's documentation addresses.
Bring a hotspot and an offline copy of the deck, prompts, kit, and answer key. Test the handout download route. The existing GitHub URL appears in the deck, but these new files have NOT been published there. No messages or invitations have been sent.
For a stage fallback, rehearse your own reference app before the event; this preparation intentionally contains no scanner code. Have a captured real scan result available to explain the expected output if a machine fails, while clearly distinguishing that fallback from a completed live scan.

RECOVERY / TIME CONTROLS
At minute 18, identify setup failures and pair. At minute 25, move on.
For each lab, one person drives and one reviews; switch after the lab.
Five minutes behind: demonstrate the skill practice once and skip the examples menu. Protect the break and scanner verification.
Ten minutes behind: pair builds, use one simple fixed profile, and drop stretch goals. Record incomplete work honestly. Do not claim every participant will complete if accounts, dependencies, or inference latency block progress.
No live provider migration, plugin shopping, GitHub SSH setup, or broad network scans in the timed core.

ANSWER KEY
Policy: 24 hours after effective separation; Entra ID, Google Workspace, Aeries, VPN; HR notice; IT ticket evidence. Retention, ownership, after-hours cover, and exception decisions are unspecified. Suggestions must be labeled.
Logs: exact flagged IDs E06, E07, E10, E11. E06 includes a failure exactly ten minutes earlier. E09 at 18:59 and E12 at 07:00 are not flagged. E08 is a failure and is not flagged by the success-only country rule. Explicit UTC rules are training rules, not production detection logic.
Nmap fixture: 50 unique hosts, 45 up, 5 down, 125 open port records (115 TCP / 10 UDP), and 45 closed TCP records. lab-01 has 135/445/3389 TCP. Ten hosts have 3389 TCP; ten have 161 UDP. Down hosts: .10, .20, .30, .40, .50. No inferred CVEs, OS versions, or actual live assets. Counts refer to host-port records, not unique ports or vulnerabilities. Full inventory in answer-key.json.
The fixture deliberately combines TCP and UDP results to test imports; the first LIVE profile is TCP connect only. The app should use one result model for both sources.

OFFICIAL REFERENCES USED
https://code.claude.com/docs/en/setup — installation, diagnostics, authentication.
https://code.claude.com/docs/en/skills — skill format and project location.
https://code.claude.com/docs/en/sub-agents — delegated context and restricted tools.
https://code.claude.com/docs/en/permissions — permissions and shell access.
https://nmap.org/book/output-formats-xml-output.html — XML interface for machine-readable scan output.
https://nmap.org/book/zenmap.html — scan profiles, result views, and saved scans.
https://nmap.org/download — prework installation reference.
https://git-scm.com/install/mac — Git via Apple Command Line Tools or Homebrew.
https://git-scm.com/install/windows — Git for Windows installer, including Git Bash.
Recheck account access, commands, and installed Nmap behavior close to the event. Pricing and precise model versions are intentionally omitted.

SLIDE-BY-SLIDE FACILITATOR NOTES
'''
    note_parts=[]
    for i,s in enumerate(SLIDES,1):
        note_parts.append(f"\n{i:02d}. [{s['time']}] {s['title']}\n{s['notes']}\nSource: {s['source']}\n")
    (OUT/'Facilitator Guide.txt').write_text(source_analysis+'\n'.join(note_parts))
    (OUT/'slide-content.json').write_text(json.dumps({'core_slides':CORE,'slides':SLIDES},indent=2,ensure_ascii=False))
    with zipfile.ZipFile(OUT/'attendee-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KIT.iterdir()): z.write(p,'attendee-kit/'+p.name)


def verify():
    p=Presentation(OUT/f'{DECK_NAME}.pptx')
    assert len(p.slides)==len(SLIDES)
    assert all(s.notes_slide.notes_text_frame.text.strip() for s in p.slides)
    end=0
    for slide in SLIDES[:CORE]:
        start,finish=map(int,slide['time'].split('–'))
        assert start==end and finish>start
        end=finish
    assert end==120
    for i,s in enumerate(p.slides,1):
        expected='000000' if i in SECTION_STARTS else 'FFFFFF'
        assert str(s.background.fill.fore_color.rgb)==expected
        assert sum(shape.name=='OCDE logo watermark' for shape in s.shapes)==(0 if i==1 else 1)
        for shape in s.shapes:
            assert shape.left>=0 and shape.top>=0, (i,shape.name)
            assert shape.left+shape.width<=p.slide_width+10, (i,shape.name)
            assert shape.top+shape.height<=p.slide_height+10, (i,shape.name)
    root=ET.parse(KIT/'fictitious-50-hosts.xml').getroot(); hosts=root.findall('host')
    assert len(hosts)==50 and len({h.find('address').get('addr') for h in hosts})==50
    assert sum(h.find('status').get('state')=='up' for h in hosts)==45
    ports=root.findall('./host/ports/port'); opened=[p for p in ports if p.find('state').get('state')=='open']
    assert len(opened)==125 and sum(p.get('protocol')=='udp' for p in opened)==10
    assert sum(p.find('state').get('state')=='closed' for p in ports)==45
    dtd=Path('/opt/homebrew/share/nmap/nmap.dtd')
    dtd_result='not checked (local Nmap DTD unavailable)'
    if dtd.exists() and Path('/usr/bin/xmllint').exists():
        for filename in ['fictitious-50-hosts.xml','empty-scan.xml']:
            subprocess.run(['/usr/bin/xmllint','--noout','--dtdvalid',str(dtd),str(KIT/filename)],check=True)
        dtd_result='both well-formed fixtures validate against the installed Nmap DTD'
    from datetime import datetime,timedelta
    with (KIT/'signins.csv').open() as f: rows=list(csv.DictReader(f))
    flags=[]
    for row in rows:
        t=datetime.fromisoformat(row['timestamp_utc'].replace('Z','+00:00'))
        if row['result']!='success': continue
        failures=sum(r['user']==row['user'] and r['result']=='failure' and
           t-timedelta(minutes=10)<=datetime.fromisoformat(r['timestamp_utc'].replace('Z','+00:00'))<t for r in rows)
        if t.hour<7 or t.hour>=19 or row['country']!='US' or failures>=3: flags.append(row['event_id'])
    assert flags==['E06','E07','E10','E11']
    doc=fitz.open(OUT/f'{DECK_NAME}.pdf'); assert len(doc)==len(SLIDES)
    # Contact sheets are rendered from the PDF proof for visual review.
    for start in range(0,len(doc),12):
        sheet=Image.new('RGB',(1200,4*190),'#D9DEDD')
        draw=ImageDraw.Draw(sheet)
        for offset in range(min(12,len(doc)-start)):
            page=doc[start+offset]; pix=page.get_pixmap(matrix=fitz.Matrix(.4,.4),alpha=False)
            im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); im.thumbnail((384,216))
            # 3 columns, four rows, scaled to fit.
            im.thumbnail((384,164)); x=(offset%3)*400+8; y=(offset//3)*190+19
            sheet.paste(im,(x,y)); draw.text((x,y-15),str(start+offset+1),fill='black')
        sheet.save(OUT/f'high-contrast-contact-sheet-{start//12+1}.png')
    result=f'PASS: {CORE} timed slides + {len(SLIDES)-CORE} appendix slides; continuous 120-minute schedule; all shapes within slide bounds; all speaker notes populated; PDF pages match; 50-host XML counts and exact log answer key verified; {dtd_result}. PDF is generated from the same drawing instructions as the PPTX; PowerPoint-native rendering was not available for comparison.'
    result+=f' Brand checks: logo on all {len(SLIDES)-1} non-opening slides; exact logo blue #155191; black section backgrounds and white remaining backgrounds.'
    (OUT/'high-contrast-verification.txt').write_text(result+'\n')
    print(result)


if __name__=='__main__':
    render(); supporting_files(); verify()
