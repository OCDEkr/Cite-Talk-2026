---
title: Linux SME peer review — Round 2
owner: cite-linux
date: 2026-11-10
status: review-awaiting-lead-disposition
---

# Round 2 peer review

**Support integration of the teacher's policy → verified script → static local HTML report core**, subject to the specific fixes below. Accept the eight-minute readiness block and the supplied E01–E12 rule contract. This is a local report application, not a fake scanner, scan simulator, or claim of Nmap functionality. The coordinator update in [DECISIONS.md](../DECISIONS.md) is the current scope direction; the lead retains final authority. Historical builder comments do not mandate live scanning.

## Materials actually reviewed

- [Teaching proposal](../teaching/PROPOSAL.md), [participant workbook](../teaching/PARTICIPANT-WORKBOOK.md), [slide narrative](../teaching/SLIDE-NARRATIVE.md), [agenda.json](../teaching/agenda.json), [fixture provenance](../teaching/labs/PROVENANCE.md).
- [Design proposal](../design/PROPOSAL.md), [lead decisions](../DECISIONS.md), [coordinator notes](../COORDINATOR-NOTES.md).
- Supporting evidence: [answer key/specimens](../teaching/ANSWER-KEY.md), all three reference/checker Python files, the fictional policy, synthetic CSV, inert review snippet, and the source of `teaching/validate_teaching.py`.

No peer file was changed. Only Linux-owned guidance/review files were authored. No installers, agent sessions, scanners, listeners, archives, payloads, or GUI applications were run.

## Agreements and resolved conflicts

| Topic | Review disposition |
| --- | --- |
| Learning arc | Three uses of the same scope → inspect → verify habit are more credible than three tool installations. Retain exact evidence checks and debriefs. |
| App scope | Lead selected a static HTML report from checked synthetic CSV. No Nmap, backend/server, arbitrary targets, external reputation lookup, remediation or deployment is needed. Original scanner concept is optional future work outside core. |
| Time | Independently computed **120 minutes**, 21 contiguous positive blocks, titles/times matching narrative. Break 48–53 and Q&A 115–120 remain protected. This validates arithmetic, not classroom pacing. |
| Readiness | Adopt **20–28** from teacher, not my original standalone five-minute block. See exact reconciliation below. |
| Runtime | Standard-library Python is sufficient for the supplied script/report references. Recommend maintained **CPython 3.11+** as workshop floor; prepared Ubuntu 24.04/Python 3.12 as Linux rehearsal baseline. No pip/npm/venv required. |
| Accounts | Approved Claude access is default live route. Runtime-only/no-account and paper/no-runtime routes are valid independent routes; no shared account, pairing requirement, provider migration or free-model promise. |
| Fixtures | Retain teacher's schema and arbitrary US/UTC exercise baseline. Source provenance distinguishes invented training rows from actual exports/incidents. No additional Linux fixture fork. |
| Permissions | Keep visible normal permissions, approved disposable environment and review-before-run. Prompt wording, a scratch folder, removing Edit, or an “approved” tool label does not establish OS containment. |
| Presentation | Full prompts in workbook; slide shows task/path/outcome/fallback. Support explicit source/synthetic/authored-example labels, readable type and distinct execution versus review states. |

### Five-minute versus eight-minute gate

My Round 1 five-minute allocation is superseded, **not added** to the teacher's eight minutes. Preserve teacher's stated three-minute readiness plus five-minute recovery/transition budget:

| Elapsed | Action | Exit condition |
| --- | --- | --- |
| 20–23 (3 min) | Locate prepared copied kit or printed packet; check working directory, fixture and runtime; choose route | Everyone has materials and a provisional route |
| 23–25 (2 min) | Helpers resolve simple path/approved-session problems | No installers, account creation, provider changes, reboots or security-control changes |
| 25–28 (3 min) | Unresolved setup switches to review; others inspect permissions/predict a row/transition | Everyone starts lab 1 at 28 |

**3 + 2 + 3 = 8**, with recovery/transition occupying the last five minutes. No extra READY call, preflight script, or reference-code execution is required to consume another block. Inference should already work from prework; an optional READY response cannot prove containment. If nothing fails, use the recovery allocation for evidence prediction rather than lengthening the session.

## Specific fixes before final packaging

These are requests for the owning peer/lead; Linux-owned changes are listed separately below.

| Priority / owner / location | Finding | Concrete fix |
| --- | --- | --- |
| P1 — teaching + lead, workbook readiness/distribution | Workbook correctly assumes a copied `teaching` root, but does not give a copy/entry recipe. Running `labs/...` from repository root fails. A downloaded `teaching` kit does not include `linux/preflight.sh`. | Include the audited copy-root contract below, adapted to the real archive layout. Keep Linux preflight optional/prework; never show bare `bash preflight.sh` inside `teaching`. Test paths from the final unpacked kit. |
| P1 — teaching, prework/readiness | “Supported Python 3” is underspecified. A system `python3` may be 3.9 or 3.10 even though the reference appears to run. | Specify workshop **3.11+**; prepare/test 3.12 on Linux. This is a support floor, not proof every newer Python/OS combination has been tested. Keep paper participation independent of Python. |
| P1 — teaching, `labs/reference_report.py` | CSV header validation is absent. Reproduced: a header-only CSV with `wrong_column` produces the same zero-event report as valid empty input. The requested generated-app contract explicitly says wrong/missing columns should fail. | Validate the four required columns before reading/rendering rows, including header-only files. Reject missing/surplus cells and malformed rows with a clear error. Add a wrong-header-only negative check independent of the valid-empty case. Decide whether column order must be exact and state it. |
| P1 — teaching, same renderer CLI | Source inspection shows output is opened with `'x'` before `render(rows)` executes. A malformed row raising during rendering can leave an empty output file, causing a subsequent corrected run to fail on existing output. | Validate input and compute the HTML fully before exclusive output creation. Preserve existing outputs; do not solve this by switching to overwrite mode. Test malformed input leaves no new output. This CLI failure was **not executed** under the read-only review constraint. |
| P1 — teaching, lab 3 reference fallback | The fallback command hardcodes `work/reference-events.csv`. A participant whose generated triage succeeded may only have `work/flagged-events.csv`; their report-generation fallback then fails on a missing file. | Explicitly choose the already **checked** CSV for both generated and reference report commands. Show two alternatives or one assigned input variable. Do not regenerate an unverified CSV merely to satisfy a filename. |
| P2 — teaching, slide 7 / route wording | Slide “Run: approved agent + Python” hides the useful runtime/no-account route, though the workbook later supplies it. | Show three routes: live agent; local reference + Python; printed specimens. Same reasoning checkpoints; separate generated/executed/rendered/source-reviewed/paper-reviewed evidence. |
| P2 — teaching, slide 8 | Screen shortens policy input to `offboarding-policy.txt`, while actual copyable task uses `labs/offboarding-policy.txt`. | Use `labs/offboarding-policy.txt` consistently on the slide and workbook, or clearly label a basename as such. Avoid a second apparent path. |
| P2 — teaching + lead, paper/distribution links | Repository-qualified Obsidian links such as `[[Workshop-Team/teaching/ANSWER-KEY]]` may not navigate in an extracted standalone kit/PDF. | Final workbook uses local relative links and stable section/page references. Bundle/print inputs and all specimens. A QR/link is not the only route; no public distribution URL is invented. |
| P2 — design, command length | Workbook's longest Bash command is **95 characters**; several other commands exceed 64. Aliasing a long command hides its meaning and adds startup/config work. | Keep full commands in workbook; show a short verified check on slide, or intentional Bash continuation using `\` with no trailing spaces. Never truncate a runnable command with `…`. No install commands in core slides. |
| P2 — design, environment/render claims | Proposal says a new venv is needed and reports a prior AppleScript export. Coordinator now identifies a prepared interpreter and says current export is untested. | Use coordinator's prepared interpreter without installs. Treat prior export as historical evidence only; record an actual current PowerPoint export result or blocker during authorized Round 3. This review did not attempt export. |
| P2 — design, provenance | Proposal mentions a “fictitious” chip for an existing scan PDF. That file is not needed for selected core and was not verified by this review. | Core uses only teacher's purpose-created policy/events. Do not infer scan-report provenance from earlier prose/script comments. Any later source report needs its own inspection and label. |

### Exact copy/run contract

The current teacher commands are correct **inside a disposable copy whose top level contains `labs/`**, with `work/` created there. They are not repository-root commands. Linux guidance now supplies a candidate recipe from repository root, **inside the approved disposable Linux environment**:

```bash
cite_lab_parent=$(mktemp -d "$HOME/cite-workshop.XXXXXX")
cp -R Workshop-Team/teaching "$cite_lab_parent/kit"
cd "$cite_lab_parent/kit"
mkdir -p work
```

This recipe is source-reviewed only, not executed during this read-only peer check. Stop on any error. `mktemp` prevents name collisions; it does not provide security isolation. The final archive layout still needs a clean-room copy/run rehearsal. Do not carry host district folders/credentials into a VM just to make paths work.

For an account-free runtime route, these inputs/scripts exist and the interfaces match their source:

```bash
python3 labs/reference_triage.py \
  labs/signins.csv work/reference-events.csv
python3 labs/check_triage.py work/reference-events.csv
python3 labs/reference_report.py \
  work/reference-events.csv work/reference-review.html
```

These commands create outputs and therefore were **not run as CLI file-writing operations in this round**. In-memory checks of the underlying functions are recorded below. Use a new output path/fresh copy on reruns; the references intentionally refuse to replace outputs. For report fallback after successful generated triage, substitute the checked `work/flagged-events.csv` explicitly.

Python minimum: [official Python version status](https://devguide.python.org/versions/), retrieved **2026-11-10**, lists 3.11+ as supported and 3.10 as end-of-life. Workshop code does not require a recent agent runtime's managed Python to be repurposed as the participant's system runtime. No package installation is justified by these stdlib labs.

## Account-free path and safety assessment

The answer key is now a concrete independent fallback, not a promise of future specimens. Specimen A supports policy correction; source rows plus flawed B/inert snippet support manual flagging and bug review; C supports a corrected screen/source trace/test plan. A participant can complete these without Python, terminal, network, account, or a partner. Runtime/no-account participants can additionally inspect/run references. Do not call the authored specimens saved model outputs or recordings.

The reference source imports only standard-library file/data/HTML modules. No network, shell/process, dynamic evaluation of input, package installation, service startup, or account-changing calls were found in the three lab scripts. `review-snippet.txt` is visibly inert; keep it a text-reading exercise. The quoted injection sentence and harmless `<b>training</b>` example are explanatory text, not commands/payloads to execute.

Triage's source/target resolution check and exclusive output protect the fixture from direct same-path replacement. Report exclusive creation also refuses an existing input/output path, but its validation/partial-output gap above remains. HTML escaping, synthetic label, review-signal caveat and `default-src 'none'` are useful; none certifies independently generated participant code. Review every generated command before running and inspect generated HTML before opening it inside the disposable environment. No browser/server is required for source-only verification.

The static report is an honest application artifact; source-reviewed/paper-reviewed is an honest partial mode. A rendered browser screen is extra evidence, not something this audit performed. Production schema handling, timezone baselines, detection quality, access isolation and actual district data approval are outside this synthetic fixture's guarantees.

## Actual read-only verification evidence

Executed an inline standard-library harness using coordinator's existing interpreter:

```text
/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python -I -S -
Python: 3.14.9; host: macOS; exit 0
```

The harness parsed/reviewed imports and loaded the three audited reference/checker modules with non-main names via in-memory compilation. It used `StringIO` and a scoped mock of `Path.open` for the checker's data stream. No `.pyc`, output CSV, HTML, fixture copy or teacher verification file was created. The teacher validator was **read, not run**: its main writes `AGENDA.md`, `verification.json` and temporary files under teaching, outside this role's write ownership.

| Check | Observed result / limit |
| --- | --- |
| Agenda/narrative | PASS: 21 matching slide numbers/titles, contiguous ranges, exactly 120 minutes; readiness 20–28 |
| Main synthetic triage | PASS: E06/E07/E10/E11, ordered; exact source user/timestamps/reasons accepted by hand-key checker |
| Wrong same-count output | PASS: replacing E06 with E08 was rejected by checker |
| Hours | PASS: 06:59:59 and 19:00:00 flag; 07:00:00 and 18:59:59 do not |
| Failure burst | PASS: exact 600-second boundary, expired 601-second case, same-user filter, unsorted input, equal/future timestamp exclusions, reuse across later successes, multi-reason success |
| Success-only | PASS: fixture failure rows excluded; out-of-hours failures in constructed multi-reason case did not appear as flags |
| HTML | PASS: four events/three categories, valid empty rows zero/zero, literal harmless markup escaped, parsed HTML had no tested active/external asset tags or attributes |
| Invalid header-only CSV | **GAP REPRODUCED:** parser produces no rows and renderer emits zero-event report; reference CLI does not validate header |
| Paths/assets | PASS: referenced policy/CSV/snippet/reference/checker files exist; source interfaces match workbook invocations under documented working directory |
| Source preservation | PASS: SHA-256 hashes of inspected teaching Markdown/lab files, agenda and validator unchanged before/after execution |

Reviewed `labs/signins.csv` SHA-256: `67aee15ccb0ddad1e7330a263b337c986a6d91116d599b314f83df357d428c34`.

This independently confirms core fixture behavior on the prepared **macOS Python 3.14.9**, not Linux/WSL2, the proposed 3.11 floor, Ubuntu/Python 3.12, every malformed-input case, CLI exclusive-write behavior, a browser render, or participant-generated code. The system Python reports 3.9.6; that is why a bare `python3` presence check is insufficient and is not an endorsed participant runtime.

## Answers to design's Linux questions

1. **64-character limit:** longest current workbook Bash line is 95; do not create an alias. Slides can show `python3 labs/check_triage.py work/flagged-events.csv` (52 characters) and point to full workbook steps. Use intentional continuation for longer reference commands, not visual wrapping that changes copied syntax.
2. **Platform label:** `Ubuntu / WSL2 · Bash · normal user · copied kit root`. Use a separate unmistakable prework label for Windows PowerShell/Administrator instructions. macOS/native Windows remain appendices with honest untested mappings.
3. **Prompt marker:** decorative `$` only for normal-user terminal examples; exclude it from copied workbook text. No root `#` prompt in core. Agent instructions and `/permissions` are labeled “inside agent,” not Bash. No fake terminal success screenshots: use authored-example labels or actual captured execution evidence.

## Linux-owned changes made this round

- [SETUP-PREFLIGHT.md](SETUP-PREFLIGHT.md): eight-minute gate/minute-25 route switch, Python floor, actual teacher specimen links, copy/run contexts, account-free reference commands, local-report core and known renderer caveat.
- [preflight.sh](preflight.sh): isolated no-site check for Python 3.11+, still no agent/config/network calls. It remains a prerequisite check, not installation/login/containment validation.
- [PROPOSAL.md](PROPOSAL.md), [PEER-QUESTIONS.md](PEER-QUESTIONS.md), [CORRECTIONS.md](CORRECTIONS.md), [COMMAND-VERIFICATION.md](COMMAND-VERIFICATION.md): mark old gate/scanner questions superseded and record upstream runtime status.
- [VERIFICATION.md](VERIFICATION.md): retain Round 1 history; append Round 2 scope and evidence limits.

## Required next verification / lead disposition

Before release, teaching fixes/retests renderer input validation and fallback input selection; lead freezes final kit layout and Python floor. Round 3 rehearses the **actual extracted copy and CLI commands** on approved Linux/WSL2, including non-root execution, version/permission checks, untouched input, exclusive writes, malformed/empty report handling, reference fallback and fully offline paper completion. Test the proposed floor or narrow supported versions to observed evidence. No installer, scanner, account access, production connection or host security change is authorized by this review.

Lead decides final scope/timing and whether any residual limitations block release. Linux recommends proceeding with the local-report core after these fixes, preserving validation time, break and Q&A. Await lead/peer disposition; no final build or external delivery initiated.
