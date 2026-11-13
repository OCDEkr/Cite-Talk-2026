---
title: Round 1 Linux verification record
date: 2026-11-10
status: limited-host-verification
---

# Verification record

## Read as source material

- `Workshop-Team/TEAM-BRIEF.md`, `CLAUDE.md`, `Setup Guide.md`, `Setup Walkthrough.md`.
- `Getting Started.md`, `Guardrails.md`, `Guardrails Checklist.md`, `Resource Index.md`, `Sources.md`, `Skills Agents Plugins.md`, `Examples.md`, `Talk Outline.md`, `Application Builds.md`.
- Relevant setup/agent sections of `Cite Talk Guide.src.html`; setup/lab/verification portions of `scripts/build_workshop.py` and `scripts/build_cite_deck.py`; `scripts/hermes_sheet.py` and reference-library searches.
- All three `Cheat Sheets/` PDFs: inspected their text by decoding existing PDF content streams with Python standard-library ASCII85/zlib routines. This was text inspection, not PDF rendering or a complete shortcut-by-shortcut product audit. Claude and Hermes setup/permissions claims received the relevant review; herdr remains outside the core install audit.
- Official pages in [COMMAND-VERIFICATION.md](COMMAND-VERIFICATION.md), retrieved 2026-11-10. Installers were not downloaded/executed. No account, secret, credential cache, or incident capture was read.

Documentation limitation: GNU Bash/coreutils reference pages timed out on initial and alternate aggregate-page retrieval. POSIX utility-page alternatives returned 403. The matrix marks those GNU references as unverified retrieval; basic shell-discovery code is an authored adaptation, not a claim of upstream installer validation. Vendor product/install documentation was successfully retrieved.

## Executed on the host

This workspace is on macOS. Only read-only discovery/source inspection and local authoring checks were used; there is no claim of a successful Linux install.

| Check | Observed result | Limit |
| --- | --- | --- |
| Read/list/search repository files; `git status --short` | Source files and pre-existing modified/untracked state observed | Existing changes left alone; no commits/resets/builds |
| Python module availability check | Neither system nor Homebrew Python had the queried PDF libraries | No package installation attempted; standard-library text decoding used |
| Standard-library PDF text extraction | Claude, Hermes, herdr reference text was readable | Not a visual review; no embedded content executed |
| `bash -n Workshop-Team/linux/preflight.sh` | Syntax validation passed | Not a Linux runtime test |
| `bash Workshop-Team/linux/preflight.sh` | Printed `SKIP: Linux/WSL2 preflight requires Linux. Use the platform appendix or offline workbook.`; exit **2** | Expected macOS guard; Linux/root/missing-dependency branches not exercised |
| Walkthrough timing arithmetic | 3+8+4+4+3+4+7+3+4+8+10 = **58** | Source's “about 55” is rounded/inexact |
| Local Markdown artifact check | All seven artifacts present; no broken relative Markdown links or unbalanced code fences found; readiness arithmetic = **5 minutes** | Structural check, not content sign-off or live URL availability test |

The offline script does not read agent configs, inspect environment variables/secrets, invoke installed agent binaries, use a package manager, scan services, or contact the network. It checks tool presence only. Its success code is deliberately **not** called proof of live-agent readiness.

## Not executed or established

- WSL installation, virtualization checks, distro conversion, reboot, apt, nvm, Homebrew, npm, pip, or any vendor installer.
- Claude/Codex/Hermes version/help/doctor/login/inference commands. Their printed examples in the guide/matrix are source-checked instructions, not captured terminal success.
- Linux sandbox enforcement, AppArmor compatibility, WSL interoperability containment, Windows-native behavior, ARM64 installs, agent approval behavior under existing managed settings.
- Nmap or any scanner, packet replay, archive/payload execution, listener/server startup, production connections, or GitHub publishing/key creation.
- Availability/free status of the draft Nemotron model ID; current pricing; blanket data-policy assertions; full herdr command compatibility.
- A complete offline workbook bundle or final slide deck. These remain teaching/lead integration deliverables.

## Round 3 evidence checklist for an approved disposable lab

1. Record OS/distro, CPU architecture, non-root UID, WSL VERSION 2 where applicable; no account identifiers or credential material.
2. Run the offline preflight on a fresh image. Verify normal, missing-Python, and root cases on disposable fixtures/environments, not by removing host packages.
3. Install just the selected primary agent using the approved route. Record actual package owner/channel/version. Run local version/diagnostics and a harmless synthetic inference separately.
4. Inspect effective permissions and confirm sandbox enforcement using the vendor's documented probe in the disposable environment. A status label alone is weaker evidence than a denied out-of-scope operation.
5. Run the agreed local script against known synthetic input; verify exact expected record(s), boundary handling, and output. Test the printed/saved-response path with network unavailable.
6. Only if separately assigned/authorized: validate an optional scanner backend in its isolated lab against the agreed target/profile. Record real outputs; saved import cannot prove execution.
7. Recheck documentation near publication, account availability, provider policies, and venue access. Lead resolves scope and signs off; this Round 1 record does not substitute for that rehearsal.

## Round 2 addendum — 2026-11-10

Read the requested peer proposals, workbook/narrative/agenda/provenance, design proposal, lead decisions and coordinator notes, plus teacher's answer key and reference/checker source. [PEER-REVIEW.md](PEER-REVIEW.md) records agreements, fixes, commands and evidence limits. Lead-selected core is now the static local HTML report; no scanner requirement remains for core. Adopt teaching's readiness block 20–28 with unresolved setup switching routes at 25. The Round 1 five-minute arithmetic above is historical, not an added session block.

Executed a read-only, standard-library inline harness under the existing coordinator-prepared interpreter, Python **3.14.9 on macOS**, with `-I -S`. Reference functions were loaded by in-memory compilation under non-main names; CSV/checker inputs were in-memory streams. Agenda/title/time checks, exact triage/checker results, boundary/negative cases, HTML counts/escaping and inspected source hash preservation passed. Wrong-header-only CSV becoming a zero-event report was reproduced as an unresolved validation gap. No fixture/output/bytecode was written; teacher's write-producing validator was inspected but not run. The reviewed sign-in fixture hash is in the peer review.

Updated Linux preflight to check the proposed maintained Python **3.11+** workshop floor; this is a support recommendation, not proof of Linux/minimum-version execution. `bash -n` passed after the change. Running the script on this host again printed the expected non-Linux SKIP and returned **2**. Linux version/root/missing-runtime branches, copied-kit CLI writes and browser rendering remain NOT RUN. The shell-discovery statements in the original Round 1 record describe the earlier script revision; the new revision additionally invokes isolated Python solely to inspect `sys.version_info`.

Only Linux-owned files were modified. No installers, scans, listeners, payloads, login, model calls, GUI export, or external delivery occurred. Final review/build/sign-off remains lead-owned after peer disposition.
