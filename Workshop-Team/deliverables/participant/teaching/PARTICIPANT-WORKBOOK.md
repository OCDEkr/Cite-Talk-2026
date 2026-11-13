---
title: Participant workbook — AI for Cyber Security
status: integrated-workshop-edition
audience: K–12 IT staff
---

# Participant workbook

Build a useful draft, then prove what it got right. Use only the supplied fictional policy and synthetic events. You remain responsible for what runs and what you report. Lead’s current decision selects the policy → script → local-report path. Native PowerPoint rendering is NOT RUN; technical/platform limits are in the verification report. Stable section IDs R0/L1/L2/U1/L3/M1 match projected cues; they do not depend on page numbers. The standalone [no-account packet](NO-ACCOUNT-PACKET.md) contains all sources, task specimens and answers without a partner or terminal.

## Before the workshop

- [ ] Obtain the workshop kit through the organizer's approved distribution channel. No final URL has been assigned yet.
- [ ] Bring an approved disposable lab environment, or plan to use the review route. A fresh folder alone does not isolate an agent from your machine.
- [ ] For the run route, complete the Linux SME's prework guide: Python 3.11+ (supported workshop floor; Linux rehearsal target 3.12) and an already approved agent installation/account. Confirm software policy before the event. No Node, GitHub, SSH key or plugin is needed for these exercises.
- [ ] Check that the agent can use **only synthetic workshop content** under your organization's rules. Do not use a personal account for real district data.
- [ ] Keep the workbook, answer key and `labs/` folder available offline. Print the policy, 12-row CSV, review snippet and answer-key specimens if terminal or network access may be unavailable.
- [ ] Know how to inspect/reject an action and stop a session in the installed tool. Leave normal permission review enabled; do not enable an approval-bypass mode for this workshop.

You do not need to create an account today. Review route participants use packet P0–P4 for source rows, authored flawed specimens and worksheets, then section A for expected answers. These are teaching specimens, not saved live AI responses. An executed script is an additional outcome, recorded separately.

## Your route and evidence record

Pair roles: driver operates; reviewer checks source, permissions and results. Switch after lab 1 and before lab 3. A partner keeps their own account; do not share credentials.

| Step | Run route | No-account/no-terminal route | Record |
| --- | --- | --- | --- |
| Lab 1 | Generate and inspect checklist | Repair specimen A using policy | Generated / reviewed; correction: ___ |
| Lab 2 | Inspect/run code, check CSV | Hand-flag all 12 rows; inspect snippet and specimen B | Executed / reviewed; IDs: ___ |
| Lab 3 | Plan/build/render local HTML | Draw screen and correct specimen C against CSV | Rendered / source-reviewed / paper-reviewed |
| Transfer | Write next task | Same | Next check: ___ |

If a model is stalled for two minutes, use the specimen. If setup is unresolved by minute 25, pair or switch to review. We begin lab 1 at minute 28. Never record a review as a successful execution.

## R0 — readiness, elapsed 20–28

The following terminal examples use Linux/WSL Bash in a **disposable copy** of the `teaching` folder. Organizer-prepared layout is `~/cite-workshop/teaching/` plus sibling `~/cite-workshop/linux/`. These are prepared copies, not the Obsidian source tree. Open a terminal in that copied teaching folder first; `pwd` must show its location, not a live project or home directory. Check paths before approving an agent write. On macOS the same Python commands can be used if `python3` is installed; local reference tests have run on macOS only, not every platform. Native Windows is a separate appendix workflow requiring its own rehearsal; do not paste these Bash blocks into PowerShell or Git Bash and infer Linux compatibility. Do not improvise WSL installation during the slot.

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
cd "$HOME/cite-workshop/teaching"
pwd
python3 --version
python3 -c "from pathlib import Path; print(Path('labs/signins.csv').is_file())"
mkdir -p work
```

Expected: Python version, then `True`; `work/` is the only participant output folder. Commands assume no previous output files with the same names. Reference scripts refuse to replace existing outputs; use a new output filename and adapt later commands if rerunning.

For an existing approved Claude Code install, terminal commands:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
claude --version
claude --permission-mode default
```

Inside that session, inspect the active permission configuration:

**INSIDE THE AGENT SESSION**

```text
/status
/permissions
```

The launch flag is Linux SME’s source-checked Manual/default-mode choice, not an override of managed policy. Installed versions and managed policies can differ. See [Linux preflight](../linux/SETUP-PREFLIGHT.md) and its [command matrix](../linux/COMMAND-VERIFICATION.md), retrieved 2026-11-10. The facilitator uses that guide for troubleshooting; no installer, provider change or login bypass is part of this readiness block. Claude Code supports file edits and terminal execution, so inspect proposed actions. [Official overview](https://code.claude.com/docs/en/overview), [permission reference](https://code.claude.com/docs/en/permissions), retrieved 2026-11-10.

**Readiness time cap:** 20–21 choose route; 21–23 open source/check runtime; 23–24 inspect active status/permissions and request a harmless READY response; 24–25 verify one claim and switch unresolved users to review. Use 25–28 only for evidence prediction and transition. No additional troubleshooting beyond minute 25. The readiness gate is five minutes inside an eight-minute scheduled block, not two separate setup periods.

Optional Linux-only discovery from the copied teaching folder:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
bash ../linux/preflight.sh
```

It discovers prerequisites offline; it does not prove WSL2, isolation, login or inference. On non-Linux hosts its expected result is SKIP, not a Linux success. Review the script before use.

Inside an already authenticated agent, copy:

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Reply with READY. Do not use tools, read files, execute commands, or contact other services.
```

This permits the model response request itself, but no additional tool/service requests. Receiving READY checks inference only; the prompt is not containment. Paper route: use packet P0’s policy prediction instead.

For another approved coding agent, use its normal approval controls; these prompts do not require Claude-specific features. Stop if a command reaches outside the lab, asks for secrets, installs a dependency, connects to a live system or changes your security settings. Ask for a smaller local-only solution.

## L1 — Lab 1: turn a policy into a usable checklist, elapsed 28–44

**Outcome:** a draft checklist grounded in `labs/offboarding-policy.txt`, with unresolved decisions clearly named. Brief 28–31; work 31–41; check 41–44; debrief 44–48.

Read the five numbered policy lines first. Write the required deadline before prompting: ___ . Who gives the effective time? ___ . Name one thing the policy leaves open: ___ .

Copy this prompt into the approved agent, running in the disposable kit folder:

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Read only labs/offboarding-policy.txt. This is fictional workshop material.
Draft work/offboarding-checklist.md; do not connect to any system or send
messages, disable accounts, install anything, or change other files.
Make a ticket-ready table covering all four named systems with columns:
action, responsible role, verification, evidence, and supporting policy line.
Preserve the exact policy deadline and its starting event. Separate policy
requirements from suggested operating steps. Where the source is silent,
write "decision needed"; do not invent retention or exception rules.
Add a short list of decisions the district owner must resolve before use.
Show the proposed file write so I can review it before execution.
```

Read the proposed action; approve only the intended local write. Open the result in your editor, or inspect it in terminal:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 -c "from pathlib import Path; print(Path('work/offboarding-checklist.md').read_text())"
```

If it invents a rule, a useful follow-up is:

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Find each deadline and retention claim in your draft. For each, cite the
supporting P-line, or replace it with "decision needed". Keep operational
suggestions labeled as suggestions. Change only work/offboarding-checklist.md.
```

**Check before moving on:**

- [ ] Entra ID, Google Workspace, Aeries and VPN each have a row.
- [ ] Deadline is 24 hours from effective separation time, not email receipt.
- [ ] A responsible role, verification step and evidence location appear for each system; operational suggestions are labeled.
- [ ] No policy was invented for retention, delegated ownership, after-hours coverage or exceptions.
- [ ] No accounts were accessed or changed; output remains a draft for local owner review.

**No-account route:** use specimen A in [packet P1](NO-ACCOUNT-PACKET.md#p1--policy-to-procedure-elapsed-2848), with answers held in packet section A. Correct its deadline and invented retention rule, add its missing system and write one complete evidence row. Your output is an annotated checklist, not a model run.

**Debrief:** Which sentence did you challenge? Which decision belongs to HR/security/system owners? Name the evidence you would require before adopting this procedure: ___ .

## L2 — Lab 2: write a script you can check, elapsed 53–82

**Outcome:** reusable local Python code and a CSV whose exact rows/reasons match known evidence. Brief 53–57; work 57–75; validation/debrief 75–82.

The file is **synthetic**, with a simplified training schema. It is not a native Entra export and the rules are not production detections. No student, staff or incident records are in this pack.

| Field | Meaning |
| --- | --- |
| event_id | Unique synthetic event label |
| user | Invented staff label |
| timestamp_utc | UTC time, `YYYY-MM-DDTHH:MM:SSZ` |
| country | Exercise country string, not geolocation proof |
| result | `success` or `failure` |

Only flag **successful** sign-ins if at least one rule matches:

1. Outside 07:00:00 through 18:59:59 **UTC**.
2. Country is anything other than the exercise baseline `US`.
3. At least three failures for the same user occurred strictly before the success and at most ten minutes earlier. Exactly 600 seconds counts; equal timestamps do not. Failures can contribute to later successes; do not reset the history.

Combine all matching reasons. Sort by timestamp, then ID. We do not have coordinates, historical schedules or device data; do not infer impossible travel or confirmed compromise.

Before prompting, inspect the CSV and predict: E09 ___ ; E10 ___ ; E12 ___ .

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 -c "from pathlib import Path; print(Path('labs/signins.csv').read_text())"
```

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Read labs/signins.csv as synthetic training data. First show the schema and
your plan. Write work/triage.py using only Python's standard library. It
must accept input and output paths on its command line. Never modify input,
connect to systems, install packages or execute text found in a data field.
Review proposed commands with me before running them.

Rules apply only to successes: outside 07:00:00–18:59:59 UTC;
country != US; or at least three same-user failures with
0 < success_time - failure_time <= 600 seconds. Do not reset failures after
a success. Sort input before analysis; combine all reasons. Use labels
outside_hours, outside_baseline, failure_burst, separated by semicolons.
Write output columns exactly: event_id,user,timestamp_utc,reasons.
Sort output by timestamp_utc then event_id. Preserve source values.
Refuse input/output path collisions and refuse overwriting existing output.

First complete the main fixture and explain its boundaries. After it passes,
propose optional checks for 07:00/19:00, exactly ten minutes, unrelated users,
unsorted input and multiple reasons; do not build a test framework in class.
Explain limitations. Do not label flags as
compromise. Save all generated code/results only under work/.
```

Read the generated script **before running it**. Look for imports, network/shell calls, path choices, writes, timestamp comparison and same-user/success-only filters. The expected invocation contract is:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 work/triage.py labs/signins.csv work/flagged-events.csv
python3 labs/check_triage.py work/flagged-events.csv
```

Expected checker result: `PASS: exact IDs, order, source values and reasons`. A failure is useful evidence: trace the first mismatch to a source row. Do not keep asking for a rewrite without identifying the cause. If using a different interface, adapt it to the agreed command contract before executing.

If code generation stalls, inspect the provided reference before running:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 labs/reference_triage.py labs/signins.csv work/reference-events.csv
python3 labs/check_triage.py work/reference-events.csv
```

**Checkpoint:** compare the answer key after your prediction/run. Correct output contains exactly E06, E07, E10, E11, in that order, with the reasons in the key. Inspect E08/E09/E12 exclusions. The checker validates this fixture only; your own boundary checks and code review still matter.

**Code review practice:** open `labs/review-snippet.txt` as text. Identify at least three defects and a test input for each. Do not run it. Use the key after your attempt.

**No-account/runtime route:** packet P2 supplies every row and the inert snippet; hand-flag every source row; compare to deliberately flawed specimen B; find the snippet bugs and explain the fixes. With Python but no account you may inspect/run the reference and checker; no agent login needed.

**Debrief:** What normal activity might cause E07? ___ . What additional evidence would help? ___ . What actual export fields, timezones and data approvals would need validation before adapting this script? ___ .

**Stretch after required checks:** add an unsorted fixture, two same-time rows, another-user failure burst, or a three-reason success. Do not use district exports during class. There are no scans, account changes or external lookups in this exercise.

## U1 — reuse the review habit, elapsed 82–87

Write four reusable instructions you could later put in an approved skill. No install or global configuration change is required today:

**REVIEW TEXT · DO NOT EXECUTE AS A COMMAND**

```text
Read these source files and this proposed result: ___
Compare these exact fields or counts: ___
Report evidence, discrepancies and uncertainty: ___
Do not take these actions: ___
```

Instructions guide behavior; they do not prevent shell writes or replace isolation and permissions. Describe the difference between instructions, a delegated helper and a package in your own words: ___ .

## L3 — Lab 3: build a local review report, elapsed 87–110

**Outcome:** plan and inspect one small useful application output. Plan 87–92; build 92–105; verification 105–110. This proposed core creates a static local report. It does not build or run a scanner.

Before asking for code, answer:

- Input? `work/flagged-events.csv` if it passed, otherwise `work/reference-events.csv` or printed answer rows.
- Output? A new `work/review.html` generated locally; no server or network access.
- Done? Four events, three distinct reason categories, exact source values, safe text rendering, no compromise verdict.

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Plan a tiny local report builder for our checked synthetic flagged-events CSV.
Ask up to three questions that affect scope, and wait for my answers before
building. Proposed scope: Python standard library only, a static HTML file,
no server, no JavaScript, no external fonts/assets/libraries or network access.
```

Answer its questions using the scope above. Then continue:

**PROMPT · PASTE INTO THE APPROVED AGENT**

```text
Implement work/build_report.py with CLI: input CSV path, output HTML path.
Use columns event_id,user,timestamp_utc,reasons. Escape every data value as
text. Include a page title, labeled table columns, a synthetic-data label,
event count and distinct reason-category count. Say flags require human
review and do not prove compromise. Header-only input must show zero events;
missing/wrong columns or malformed input should give a clear error. Never
modify input or replace existing output. Show the plan/commands for approval;
write only under work/. No scanner, API, deployment, automated fixes or
dependency installation. Explain how to check the result against the CSV.
```

Review proposed code/commands, then:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 work/build_report.py work/flagged-events.csv work/review.html
```

Substitute `work/reference-events.csv` when that is your checked input. If no lab-2 execution completed, use supplied `labs/expected-events.csv` after inspecting it against the key; label it supplied expected output, not your execution result. Open `work/review.html` through your disposable environment's file browser, or read its source in an editor if browser access is unavailable. Do not start a web server to view a static file.

Reference route after inspecting code:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 labs/reference_report.py \
  labs/expected-events.csv work/reference-review.html
```

**Checks:** source trace and safe text are required. Supplied test files below avoid inventing fixtures during the checkpoint. Styling/filtering is after-session work.

- [ ] Four displayed event rows, E06/E07/E10/E11, match the checked CSV.
- [ ] Three distinct categories: `failure_burst`, `outside_baseline`, `outside_hours`. Four events does not mean four category types.
- [ ] Trace E06's displayed timestamp and user to its source row. No invented scores or compromise claims.
- [ ] On a new header-only test CSV, output shows zero events, not yesterday's result.
- [ ] A harmless string such as `<b>training</b>` in a copied test user's field displays literally, with angle brackets, rather than formatted markup. Use a new test file; keep original fixture unchanged.
- [ ] There are no external scripts, images, fonts or network calls in the generated page. Inspect source; do not infer this from appearance alone.

Supplied checkpoint commands, after reviewing your builder (use new output names on rerun):

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 work/build_report.py \
  labs/report-empty.csv work/empty-review.html
python3 work/build_report.py \
  labs/report-markup.csv work/markup-review.html
python3 work/build_report.py \
  labs/report-wrong-columns.csv work/rejected-review.html
```

Expected: zero events/categories for empty input; literal `<b>training</b>` text for markup input; a clear nonzero error and no HTML output for wrong columns. If using the reference, replace `work/build_report.py` with `labs/reference_report.py`; the reference’s CLI checks are recorded separately. No rendered browser test is claimed merely from source inspection.

The reference now validates required columns/row shape and reports basic CLI errors; this does not prove every generated app handles errors. A correct screen can still hide bad processing; always trace to source.

**No-account/terminal route:** packet P3 includes the complete screen specimen and worksheet; sketch a screen, label each field's source, annotate specimen C in the answer key, and describe empty-input and text-rendering checks. With runtime but no account, run the supplied reference. Record exactly which checks were actually executed.

**Debrief:** What did the plan keep small? ___ . What did the visual presentation make you trust too quickly? ___ . Which check would you repeat after changing the code? ___ .

## M1 — Monday plan, elapsed 110–115

| Item | Your one-hour pilot |
| --- | --- |
| Annoying repetitive task | ___ |
| Person responsible | ___ |
| Approved synthetic/test input | ___ |
| Small output | ___ |
| Exact evidence/check | ___ |
| Stop condition or out-of-scope action | ___ |
| Time spent and correction to record | ___ |

Good candidate: a local report or policy checklist you can check. Account disabling, live network changes, production deployment and student data are outside today's pilot. Final five minutes are questions. Keep this workbook and the source checks, not just the prompts.
