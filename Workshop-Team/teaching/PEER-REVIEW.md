---
title: Teaching peer review — Round 2
status: fixes-implemented-awaiting-lead-integration
date: 2026-11-10
owner: cite-teacher
---

# Teaching peer review — Round 2

Read the actual `linux/PROPOSAL.md`, `linux/SETUP-PREFLIGHT.md`, `linux/COMMAND-VERIFICATION.md`, `design/PROPOSAL.md`, `design/tokens.json`, `DECISIONS.md` and `COORDINATOR-NOTES.md`. Also inspected Linux's offline `preflight.sh` and design's density checker to resolve concrete integration details. No peer files were changed. Lead retains final scope, integration and sign-off.

## Agreements, conflicts and implemented fixes

| Peer recommendation / issue | Teaching judgment | Fix implemented in teaching/ |
| --- | --- | --- |
| Lead selects local HTML report; historical comments do not require scanner | Agree; this resolves Round 1's largest scope question | Proposal marked with supersession note; narrative/workbook now follow report scope. No scanner preparation needed for core. |
| Linux: prework, one approved primary agent, normal permissions, no host installs | Agree; Claude is the default live path, Python/local and paper are independent routes | Workbook links the specific Linux guide and command matrix. Removed casual native-Windows command substitution; do not imply Bash, Git Bash and PowerShell are interchangeable. |
| Linux: readiness stops after five minutes; teaching originally allocated eight ambiguously | Conflict was wording and phase allocation, not total duration | Core slide 7 remains eight minutes: 20–25 readiness/recovery, 25–28 source evidence and transition. No troubleshooting past 25. Agenda, narrative, workbook and projected phases agree. The READY response is inference evidence only. |
| Linux: run `bash preflight.sh` from linux/; teaching commands assume teaching/ | Working-directory mismatch could strand attendees | Prepared distribution contract: `~/cite-workshop/teaching` with sibling `linux`. Workbook sets exact cwd; optional discovery is `bash ../linux/preflight.sh`. Missing prepared folders → packet, not improvised clone/install. Lead packages these folders; no public distribution is claimed. |
| Design: short projected text; full prompts in workbook; DONE WHEN/STUCK cues | Agree. Original narrative screen lines alone lack consistent work instructions | `projection-content.json` provides structured, density-checked C07/C09/C14/C18 with four short steps, readable result/fallback, stable section IDs, elapsed ranges and provenance. Important stops are instructional content, not only tiny clocks. |
| Design: three concept points maximum; teaching shows five guardrails | Five rules remain essential, but need not be five dense points | Slide 5 screen groups five habits into three short lines. Notes still teach all five. No reduced font size needed. |
| Design: excerpts, 64-character command lines, explicit context | Agree; never show an invented alias to hide a command | Support views project only short invocation/check commands, breaking lines with Bash continuation where needed. Shell context says Linux/WSL Bash terminal; Claude slash commands are separately labeled session input. Full long inspection commands stay in workbook. |
| Linux: real no-account packet, not an assumed partner login | Agree; Round 1 had ingredients spread across files and answers too close to tasks | `NO-ACCOUNT-PACKET.md` is a single self-contained printable/offline source+task+worksheet+answer file. It contains all 12 rows and policy/snippet verbatim, three flawed authored specimens, planning/permission/injection exercises and answers at the end. No account, partner, runtime or fetch is required once supplied. |
| Linux: saved response and reference output must be explicit | Agree, with provenance distinction | Flawed specimens are labeled authored examples, not recorded AI responses. Added actual expected CSV and locally generated reference HTML; neither is claimed as participant execution. No screenshot/demo recording is fabricated. |
| Lead: independent answers and meaningful runnable checks | Agree; exact IDs/reasons must be checked, not just four rows | Hand-authored expected CSV is checked separately; main triage still returns E06/E07/E10/E11. Added supplied empty/markup/wrong-column report fixtures and real CLI checks; wrong-column/short-row failures must create no report. |
| Design suggests native PowerPoint export already worked; coordinator says unexercised | Follow coordinator's current evidence boundary | No native render/export claim introduced. Density/source checks are not slide visual verification. Integration/rendering remains lead work. |

## Duration and cognitive load

The computed agenda remains **120 minutes** with 21 positive contiguous blocks. Five-minute break and five-minute Q&A are protected. There is no extra setup period before the timed start. Readiness now follows Linux's 1+2+1+1 plan inside minutes 20–25; the remaining three minutes have an explicit learning task.

Lab 1 has 10 minutes work and six minutes briefing/checkpoint, then a four-minute debrief. This is credible for a five-line policy and four-system table if formatting is optional. At minute 36 move blocked people to packet P1. Require a source-supported row, not polished prose.

Lab 2 has 18 minutes work, four briefing and seven validation/debrief. Requiring each beginner to generate a parser, design a test framework, debug the output and inspect a snippet was too much. The prompt now prioritizes the main fixture and a boundary explanation; authored extra boundary tests are stretch work. The reference validator supplies those tests without pretending participant code passed them. Offer reviewed reference or P2 at minute 68, stop generation at 75.

Lab 3 has five minutes plan, 13 build and five verification. It is still an unrehearsed estimate, not a completion guarantee. At minute 98 switch blocked participants to reference or P3. Supplied report test files avoid spending check time making fixtures. Static HTML, source trace and safe text are required; filters/style are after-session work. A partial generated program is reported as partial. Packet participants correct a screen and specify tests; that is review, not a completed build.

## Are 21 core slides sufficient?

**For the narrative, yes; for projected support during long work periods, the original text was insufficient.** Added four zero-time support views, described in `SUPPORT-SLIDES.md`: S07A routes/cwd, S14A run/check commands, S14B troubleshooting cues without answer reveal, S18A report checks. Each view has a parent slide and bounded display window inside existing time. The validator rejects added minutes or windows outside the parent. Lead can use hidden slides or alternate states; neither format should create four new lecture slots.

Lab 1 needs no extra slide: C09 work instructions and C10 checkpoint suffice for ten minutes. C15 remains the log answer reveal after work. Workbook IDs R0/L1/L2/U1/L3/M1 and packet P0–P4/A avoid premature page numbers. Recommend both digital and print workbook delivery. Physical colored status cards are optional; words/glyphs, hands or spoken response must suffice. No recording is needed for the paper route; a real later capture must carry its actual date/environment.

## Genuine expected answers and equivalence

- **Policy:** 24 hours from effective separation; four named systems; role/verification/evidence; missing retention/ownership/coverage/exception decisions. No 30-day deletion invented. A real adopted workflow requires district approval.
- **Logs:** exactly E06 failure_burst, E07 outside_baseline, E10/E11 outside_hours. E03 is inside E06's inclusive ten-minute window. E08 is a failure, E09 and E12 are within hours. Distinguish training rule from compromise verdict.
- **Report:** four events, three categories, E06 staff-c/full source UTC timestamp; header-only = zero; harmless markup literal; wrong columns = error/no report. No automatic actions or external resources.
- **Review route:** same source-based decisions, error correction, uncertainty and scope reasoning. It does not meet an execution outcome; the evidence record explicitly separates paper review, source inspection, CLI execution, live generation and browser render.

`build_packet.py` assembles the standalone packet from actual source fixtures and the facilitator key. Validator checks the embedded source and delayed answer section, expected CSV, support timing, CLI results, input preservation and design density. The reference report now emits basic clear input errors rather than an unexplained traceback for the supplied malformed cases.

## Validation and remaining lead work

Ran `validate_teaching.py` using the coordinator's prepared document interpreter. Result: **120 minutes; 21 matching core slides; four zero-time support views; 25 local checks; ten CLI checks; design lint PASS**. Full evidence is `verification.json`. The first design lint identified missing elapsed/provenance fields after the design checker evolved; those fields and phase breakdowns are now supplied and the rerun passes.

No Linux/WSL VM, actual agent login/generation, participant-generated app or live browser rendering was tested. No final slides were built or rendered. Lead still freezes the content manifest, packages teaching+linux with the documented folder layout, runs representative rehearsal/OS checks, transfers full prompts into notes, verifies all slide layouts and confirms distribution. Only a later execution can establish those results. No scope decision is blocked by the historical scanner request.

Round 2 teaching work pauses here for lead/coordinator review.
