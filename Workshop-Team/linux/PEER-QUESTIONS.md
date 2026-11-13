---
title: Linux SME questions for Round 2
date: 2026-11-10
status: for-coordinator-relay
---

# Questions for peers

**Round 2 disposition:** historical questions below are superseded where answered in [PEER-REVIEW.md](PEER-REVIEW.md). Adopt the teacher's 20–28 readiness block with minute-25 route cutoff; lead selected the local HTML report core. No scanner decision is outstanding for that core. Keep source history below for traceability.

These questions are for the coordinated proposal review. No peer panes were controlled or messaged. Suggested defaults are included so the lead has a concrete decision to review.

## Lead

1. Approve a five-minute readiness gate with all host installs/logins in prework? Default: yes, switch blocked participants to offline materials immediately.
2. Does “build an Nmap app” require a real scan in the two-hour core? The existing build script does; my minimal path proposes saved synthetic results. Default: saved-result analysis in core; real backend scanning only in a prepared optional lab. Record an explicit decision rather than call an import-only app a finished scanner.
3. Confirm one primary live agent (Claude), Codex alternative, Hermes optional comparison? Default: no requirement to install all three.
4. Approve Ubuntu 24.04 LTS/WSL2 as the rehearsed Linux baseline and a native-platform appendix? Which attendee architectures actually need testing?
5. Confirm that publishing, SSH key creation, gh, editor extensions, plugins, and herdr are optional follow-up? Default: absent from readiness gate.

## Teaching

1. Which exercise truly needs executable code, and can its core use Python's standard library? Default: no pip/npm downloads during class.
2. Can each lab ship one common task with three routes: live agent, reviewed local script, saved-response/paper review? Keep the same evidence check on all routes.
3. Please own the offline bundle: input, prompt, deliberately imperfect response, corrected/reference output, answer key, and provenance label. A saved response must not be presented as a live model result. What are the exact filenames for the final guide?
4. Is every existing scan/report/config/PCAP source classified accurately? Default: purpose-created synthetic fixtures only in core; source incident material stays optional and retains its real provenance.
5. For the saved-response route, can the outcome be “find and correct an unsupported claim, then verify one known record,” independent of account access? How will facilitator debrief compare live and offline groups?

## Design

1. Use conspicuous command context labels: **Windows PowerShell / Administrator prework**, **Ubuntu/WSL Bash / normal user**, **inside agent**, **review only**. Can these remain legible in print and without color?
2. Give each platform command its own copyable block. Do not place Windows and Linux installers in one unlabeled block or show bypass flags as a default shortcut.
3. Place source/date on technical reference slides/handouts; keep long install matrices in the appendix. Use a visible “saved example” or “synthetic fixture” label where appropriate.
4. Can the no-account route be visibly equal in the workbook, with the same checkpoint, instead of a small troubleshooting footnote?

## Coordinator / rehearsal owner

1. Can approved fresh Ubuntu/WSL2 machines be provided for Round 3? This host is macOS; no Linux installer or sandbox behavior has been tested here.
2. Who checks venue outbound auth/provider access, proxy/CA policy, and participant device restrictions? Default: pre-event administrator check plus local/printed kit.
3. Who records exact installed versions/channels and any platform-specific deviations? Existing cheat-sheet version stamps are not fresh install evidence.
4. Request peer artifact paths for Round 2. This is a proposal and setup audit, not the completed workshop or final technical sign-off.
