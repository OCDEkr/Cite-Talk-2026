---
title: Linux and CLI agents — Round 1 proposal
status: proposal-awaiting-peer-review
owner: cite-linux
date: 2026-11-10
---

# Round 1 proposal

**Round 2 update (2026-11-10):** [PEER-REVIEW.md](PEER-REVIEW.md) supersedes the timing and application-scope questions below. Accept teaching's eight-minute readiness block (20–28; unresolved setup routes to review at 25) and the lead-selected policy → tested script → static local report core. Historical scanner-builder comments do not mandate scanner completion. Offline specimens are authored examples, not recorded model responses. The working runtime recommendation is Python **3.11+**, standard library only; Ubuntu 24.04's prepared Python 3.12 is the proposed Linux rehearsal baseline.

Use one prepared Linux/WSL2 environment and one live agent per participant or pair. Offer an equally explicit no-account route using printed/downloaded synthetic inputs, saved responses, and an answer key. Treat installs and authentication as prework. Do not spend the two-hour session installing three agents.

Assumption: attendees are district/K–12 IT/security staff with mixed Windows/macOS laptops, constrained administrative rights, and uneven AI-account access. These are recommendations for the lead to decide, not final workshop requirements.

## Proposed decisions

1. Keep Claude Code as the primary live tool because the repository's teaching material uses it. Codex is a supported alternative; Hermes is an optional comparison/demo. Learning objectives and checks must work without a live model.
2. For the Linux lane, rehearse on Ubuntu 24.04 LTS, x86_64, as a workshop baseline, not a vendor minimum. Also test ARM64 if attendees need it. Windows participants use an already prepared WSL2 distribution or an approved disposable VM. WSL is not a security boundary from the Windows host by default.
3. Baseline: Bash and local files. Add Python 3 only for a script lab. Add curl/CA certificates for installation and Git only if distributing by clone or teaching diffs. Node/npm, pip, GitHub login, SSH keys, gh, VS Code extensions, plugins, and herdr are not core prerequisites. The official standalone [Codex installer](https://learn.chatgpt.com/docs/codex/cli) avoids a separate Node installation.
4. Run with normal user privileges and visible permission controls. Remove persistent bypass aliases from the proposed workshop path. A disposable VM should have no production mounts or credentials; a scratch folder alone provides no containment. Tool approvals and OS isolation have different jobs. See [Claude permissions](https://code.claude.com/docs/en/permissions).
5. A live scan/app exercise needs a separate scope decision. Existing build scripts require Nmap and a real backend scan. My minimal path proposes saved synthetic results instead. That changes the existing scanner exercise's completion criterion; the lead must resolve this explicitly. No scanner was installed or run in this audit.
6. Prepare offline fallback before inviting attendees: workbook, fixtures, deliberately imperfect saved response, reference result, and facilitator demonstration recording/screenshots. OpenRouter is an account/provider alternative, not a no-account fallback. A local LLM adds model downloads/hardware/tool-calling compatibility work; do not make it the rescue route.

Official pages were retrieved on **2026-11-10**. Product facts and commands are mapped in [COMMAND-VERIFICATION.md](COMMAND-VERIFICATION.md). Prices and guaranteed free model availability are intentionally omitted.

## Artifacts for integration

| File | Purpose |
| --- | --- |
| [SETUP-PREFLIGHT.md](SETUP-PREFLIGHT.md) | Participant/preparer setup, readiness gates, troubleshooting, concise platform alternatives |
| [preflight.sh](preflight.sh) | Offline Linux prerequisite discovery; does not run agents, installers, diagnostics, or network checks |
| [COMMAND-VERIFICATION.md](COMMAND-VERIFICATION.md) | Command/source matrix, official URLs, date, expected evidence, untested boundaries |
| [CORRECTIONS.md](CORRECTIONS.md) | Exact source locations and proposed replacements for stale/unsafe shortcuts |
| [PEER-QUESTIONS.md](PEER-QUESTIONS.md) | Decisions/questions for lead, teaching, design, coordinator |
| [VERIFICATION.md](VERIFICATION.md) | What was read/executed and what still needs a disposable Linux/WSL2 rehearsal |

## Original five-minute gate — superseded in Round 2

- Minute 0–1: choose live-agent, local-files, or paper/saved-response route.
- Minute 1–3: open the same small synthetic input; Linux users may run the offline preflight.
- Minute 3–4: live users inspect identity/model/permissions and complete one harmless response. Others inspect the saved response.
- Minute 4–5: everyone identifies one unsupported claim or verifies one known row. Anyone blocked switches routes; facilitator continues.

This allocates **1 + 2 + 1 + 1 = 5 minutes** for readiness, not a full session agenda. Lead/teaching own the final 120-minute schedule.

## Round 1 boundary

Only `Workshop-Team/linux/` is authored. Original notes, PDFs, build scripts, and others' work remain untouched. No installs, agent launches, authentication, credential reads, payload execution, scans, or final deck builds occurred. Await peer artifact paths and lead review before Round 2.
