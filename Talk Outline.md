---
title: Talk Outline
status: draft
tags: [cite-talk-2026, outline]
---

# Talk Outline

Working outline for CITE 2026: AI for Cyber Security. The attendee entry point, `Cite Talk Guide.html`, governs the teaching sequence. The deck follows the same progression. All examples remain available and all slides remain visible; the presenter may skip views when needed.

1. [[Intro]] — 8 minutes. What AI-assisted coding is, how it applies to security work, and why it matters for small teams.
2. [[Guardrails]] — 7 minutes. Read before you run, work in an appropriate environment, protect data, limit permissions, and verify output. These habits apply throughout the workshop.
3. Hands-on setup — 25 minutes. [[Setup Walkthrough]] is the presenter guide and [[Setup Guide]] the attendee handout. Installations and approved AI access are prework. In the room, create or sign into a GitHub account, create a workshop folder, and run `git init` to create its local repository. Email-verification delays do not block local Git. SSH, GitHub CLI, remote repositories, commits, and pushing are optional follow-up, not completion gates.
4. [[Examples]] — 20 minutes of examples and practice, followed by a 5-minute break. Include all thirteen existing prompts in an increasing-context/tool-use sequence: policy to procedure; awareness scenarios; tabletop; alert explanation; detection-rule draft; policy gap analysis; vendor vetting; scan-report review; vendor-script review; cleanup-script review; log triage; public organization profile; authorized breach check. These are brief walkthroughs and selected practice, not a promise to execute thirteen separate labs. State required and missing inputs honestly. The existing scan report and teaching sign-in CSV provide local inputs without adding new data.
5. [[Application Builds]] — 30 minutes. Plan, design, code, run/fix, and verify a functioning local nmap web application. Compare the app's result with nmap for the same authorized target and options. Default to localhost and the participant's own machine; keep approvals on. Completion is an observable goal, not a guaranteed or previously rehearsed result.
6. [[Skills Agents Plugins]] — 15 minutes. Use the complete provided `Skills/cisco-ios-config-audit/` skill against `Files/CISCO-Core-Switch-BLDG1-DIST-SW01-running-config.txt`. Inspect the skill and its dependencies, generate a report, and verify evidence while preserving the input. Review redaction before projecting anything; do not apply remediation or connect to a switch. Retain the generic skill-creation example, agent tutorial, plugin tutorial, and existing plugin references as supporting material.
7. [[Getting Started]] — 4 minutes. Choose one checkable task, add tools gradually, and document a small team pilot.
8. Close and questions — 6 minutes. Recap, one action, existing guide/handout/cheat-sheet pointers, and Q&A. Thank-you is the final slide.

The scheduled blocks total 120 minutes, including the five-minute break. Reference views are used inside their parent exercise's allocation, not counted as additional time. The timings are proposed pacing, not a classroom rehearsal; if execution runs long, skip example views rather than claiming an unfinished app works.

Supporting materials:
- [[Guardrails Checklist]]: one-page tick-off handout of the five guardrails.
- [[Resource Index]]: repositories worth knowing, grouped by category with a description each.
- `Cheat Sheets/`: existing optional-tool cheat sheets.
- `Skills/cisco-ios-config-audit/`: complete provided Cisco audit skill, copied without changing its original.
- [[Sources]]: source references for the talk's claims.
