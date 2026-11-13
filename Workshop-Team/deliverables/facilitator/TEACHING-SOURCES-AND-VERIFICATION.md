---
title: Teaching sources and verification — Round 1
status: locally-checked-awaiting-cross-review
---

# Sources and verification

Prepared 2026-11-10. This record covers the teaching proposal only. It does not sign off the final workshop, agent installations, a scanner, or PowerPoint rendering.

## Repository evidence read

Read `Workshop-Team/TEAM-BRIEF.md` first, then `CLAUDE.md` and the actual notes: [[Intro]], [[Examples]], [[Guardrails]], [[Guardrails Checklist]], [[Application Builds]], [[Close]], [[Talk Outline]], [[Getting Started]], [[Setup Walkthrough]], relevant setup sections in [[Setup Guide]], [[Skills Agents Plugins]], [[Sources]], [[Resource Index]]. Inspected relevant source in `scripts/build_workshop.py`, the drawing/build structure in `scripts/build_cite_deck.py`, and the opening/structure of `Cite Talk Guide.src.html` without executing builds. No installers or archives were executed. No source incident evidence was uploaded.

Read-only ZIP/XML inspection found 55 slides in each of `Cite-AI-Talk.pptx` and `scripts/CITE-Slides/CITE-AI-Talk-High-Contrast.pptx`; inspected opening/closing text for voice and narrative continuity. This is structural/text inspection only, not a visual review or timing rehearsal. Existing decks/builds are source context and have not been modified.

`scripts/build_workshop.py` includes prior-user-clarification comments about building a functioning Nmap front end. TEAM-BRIEF asks for realistic scoped exercises and does not explicitly repeat that requirement. The local-report alternative is a **proposal for lead resolution**, not an assertion that the scanner requirement was revoked. The source script's claims about supplied scan data provenance were not adopted.

## Official documentation checked

All URLs below were successfully opened through web browsing on **2026-11-10**. No install/login commands were executed. Documentation may differ from versions installed at the event; Linux SME owns final OS-specific preflight and command verification.

| ID | Primary source | Claim used / location |
| --- | --- | --- |
| S1 | [Claude Code overview](https://code.claude.com/docs/en/overview) | Agent can read code, edit files and run commands; existing-install `claude --version` and `claude` readiness commands; narrative slides 3/7 and workbook. No plan/tier claims retained. |
| S2 | [Claude Code permissions](https://code.claude.com/docs/en/permissions) | Permission modes/rules control access; approval behavior depends on configuration. Use `/permissions` to inspect. Narrative slide 5 and workbook readiness. No promise every action prompts or a folder is a security boundary. |
| S3 | [Python CSV module](https://docs.python.org/3/library/csv.html) | Standard-library dictionary CSV readers/writers and explicit newline handling ground local reference implementation; lab 2. |
| S4 | [Claude Code skills](https://code.claude.com/docs/en/skills) | `SKILL.md` instructions for reusable procedures; conceptual slide 16. No skill installation/invocation needed in core. |
| S5 | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | Specialized helper with its own context and defined tools; conceptual slide 16. Shell access is not read-only merely because Edit is absent. |
| S6 | [Claude Code plugins](https://code.claude.com/docs/en/plugins) | Components packaged and loaded as a unit; conceptual slide 16. No marketplace recommendation/count/version or plugin installation in core. |

Workshop data boundaries are explicit classroom rules, not legal advice or assertions about provider terms. No pricing, specific model availability, free-provider retention policy, legal interpretation, framework-control mapping, external breach lookup, or current adversary report is needed to complete the proposed exercises. Those topics are deferred rather than guessed.

## Round 1 local execution evidence

Executed from repository root:

```bash
python3 Workshop-Team/teaching/validate_teaching.py
```

Actual stdout:

```text
PASS: 120 minutes; 21 matching narrative slides; 18 local checks; 6 CLI checks
```

See `verification.json` for host/Python version, exact subprocess commands, exit codes and captured stdout/stderr. Host was macOS arm64 with Python **3.9.6**. That describes the test environment, not a runtime-version recommendation. Temporary test directories were created inside teaching/ and cleaned after execution; recorded commands include their then-current paths and can be reproduced by rerunning the validator.

- Summed `agenda.json` integers to 120; checked sequential slide numbers and every narrative start/end/title against computed cumulative timing; generated [[Workshop-Team/teaching/AGENDA]].
- Ran reference triage on twelve purpose-created training rows; independent hand-key checker accepted exactly E06/E07/E10/E11 and correct source values/reasons.
- Ran separate boundary cases: before/at 07:00, end of 18:59, at 19:00, inclusive ten-minute failure window, expired window, unrelated user, equal/future timestamps, unsorted input, three simultaneous reasons and success-only gating.
- Verified generated reference HTML contains four event rows and three distinct categories, header-only data renders zero, harmless markup is escaped, and parsed reference markup has no scripts/external asset attributes.
- Exercised deliberate failures: reference triage rejects replacing existing output; rejects input/output collision; independent checker rejects a wrong four-row set. Nonzero exits for these three cases were expected and recorded, not workshop failures.
- Confirmed the source CSV SHA-256 before/after was identical. Checker key is hand specified separately from the triage function, avoiding a success claim based only on code agreeing with itself.

These checks cover provided references and contracts. They do **not** run or certify participant-generated programs. Reference error messages are basic; report-builder missing-column handling is not polished UI. Browser rendering/accessibility, network isolation enforcement and managed-device behavior were not tested.

## What still requires evidence after lead decisions

1. Peer cross-review, final scanner/report decision, and a timed rehearsal with representative beginners. Exact arithmetic is proven; practical pacing remains a hypothesis.
2. Linux/WSL and native-Windows runtime paths, actual agent login/approval controls under district policy and tested stopping/recovery instructions. No successful installation is claimed here.
3. Live agent generation latency, quota/access availability and venue network behavior. Full offline review route exists; do not disguise it as tool execution.
4. Final editable 16:9 deck integration, speaker-note transfer, real renderer output, visual/accessibility inspection and distribution URL. No final deck/PDF is produced in Round 1 teaching work.
5. If a functioning scanner is selected: revise agenda/workbook/checkpoints, choose a rehearsed stack and authorized disposable lab target, and prove the browser→backend→scan path with real results. A report mockup or imported fixture does not meet that requirement.

All authored preparation artifacts are under `Workshop-Team/teaching/`. Existing staged/unstaged content was left in place. Round 1 pauses here for the coordinator to relay peer artifact paths; lead makes final decisions.


## Round 2 peer-review execution evidence — current

Read all seven requested peer/lead files and the Linux preflight/design checker sources. Current lead decision resolves the historical scanner question in favor of the local report; no scanner validation is needed for this core. See [PEER-REVIEW.md](PEER-REVIEW.md) for concrete agreements/conflicts, implemented fixes and remaining integration tasks.

Used the coordinator’s prepared interpreter (no dependency installation):

```bash
/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python Workshop-Team/teaching/validate_teaching.py
```

Current result:

```text
PASS: 120 minutes; 21 matching narrative slides; 4 zero-time support views; 25 local checks; 10 CLI checks; design lint PASS
```

`verification.json` now records this interpreter/environment and the added actual subprocess results. The validator also runs `design/check_tokens.py --slides teaching/projection-content.json` using the same interpreter; this is a maintainer cross-folder check, not a participant prerequisite. Participant run checks remain inside labs/ and need no design files. The prepared participant layout is teaching/ plus sibling linux/; the single no-account Markdown packet embeds all sources/answers and needs neither folder at reading time.

Added executed cases: header-only and harmless-markup report inputs, wrong-column/short-row rejection with no output created. The separately hand-authored expected CSV passes the independent checker; reference HTML is generated from that checked fixture, not a fabricated AI result. Supplied reference renderer validates columns/row shape and returns a basic CLI error. Validator regenerates the packet from actual fixtures and checks delayed answer placement. Four support-view windows stay within parent work time and add zero minutes; screen content passes the current design density contract including elapsed/provenance fields. Initial lint failed missing metadata; adding those fields and phases resolved the failure before this PASS.

Tests run on the local host; Linux/WSL, native Windows, live agent behavior, browser rendering and classroom pacing remain NOT RUN. PDF export/native PowerPoint behavior remains unverified per coordinator; design's historical export assertion does not establish a current export. This is teaching cross-review evidence, not final workshop sign-off.
