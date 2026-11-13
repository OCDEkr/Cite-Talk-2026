# Workshop decisions — Round 1

Status: provisional framework; awaiting specialist proposals and peer reviews.
Date: 2026-11-10. Owner: cite-lead. Coordinator: Droopy (Hermes).

## Final integration disposition — 2026-11-10

All three `PEER-REVIEW.md` files were read before final build. Lead froze policy → deterministic log triage → local static report, 21 timed core slides plus four hidden zero-time support views. Teaching's current projection-content and design's slide manifest/tokens were merged into the final integration manifest. Historical scanner comments remain historical; no scanner is built or claimed. Audience remains source-confirmed K–12 generalists as a labeled working assumption.

### Peer findings resolved

| Finding | Lead resolution and evidence |
| --- | --- |
| Readiness conflict | One eight-minute 20–28 block: capped 20–25 readiness/recovery, then 25–28 evidence/transition. No more setup at minute 25; no extra time added. |
| Route/account/runtime contract | Approved Claude default, reviewed local Python and independent paper packet. Python 3.11+ workshop floor, Ubuntu 24.04/Python 3.12 rehearsal target; actual reference execution macOS/Python 3.14.9 only. No account sharing, new install or provider migration required in class. |
| Copy-root and report fallback | ZIP extracts `cite-workshop/teaching` plus sibling `linux`; README identifies exact working directory. Generated-success and reference CSV paths tested as report inputs. No-account packet embeds all sources/specimens/answers offline. |
| Report validation/partial output | Final reference copy validates exact column order and nonempty row shape, computes HTML before exclusive output creation, rejects wrong/short input without output, preserves existing output. Boundary and malformed/empty/markup tests rerun. |
| Full readiness notes | C07 notes now include current workbook R0, READY prompt and `/status`/`/permissions`; regression assertions inspect the actual saved PPTX. |
| Omitted demo instruction | C08 now has three explicit points retaining draft-only, preserve deadlines and mark decisions needed. Builder rejects excess points instead of slicing them silently. |
| Lab commands/checks | Core work slides keep short instructions and explicitly require C14 checker execution and C18 counts/source/empty/escaped-text checks. Full commands remain in workbook and hidden support views. |
| Cards/help/reveals | DONE/STUCK bodies fit inside padded card bounds. Help links have semantic labels and clear the footer; actual internal targets/Return links checked. CHECK labels distinguish answer reveals. C07/S07A provenance is SETUP. Link metrics use actual slide index. |
| Distribution QA | Curated attendee ZIP excludes internal proposals/reviews/questions/corrections and design discussion. One attendee README entry leads to workbook. Facilitator notes and source audit records remain outside the attendee ZIP. Re-extracted actual archive passed CLI, regression and local-link checks. |
| Final read-only peer review | Coordinator relayed narrow teacher/design findings from the actual PPTX/build/notes; these are resolved above. Peers reported no offslide shapes, text-text overlap, low contrast or missing titles/notes in their read-only inspection. This is attributed peer evidence, not native-rendered visual inspection. |

### Renderer and sign-off boundary

Final narrow design recheck confirmed the earlier fixes. Its two finishing requests were applied: C18 now explicitly says “Build, then run the workbook L3 command.” and the Checker help link width is 182 points, ending at the 912-point content edge. Regression assertions cover both; final rebuild/repackage/verification and hash refresh passed. No scope expansion or native export occurred.

The one-slide editable probe exists under `integration/probe/`. Its PowerPoint export permission request was canceled unanswered. Per explicit coordinator/user instruction, export was **NOT RUN / awaiting user approval**; no retry, escalation or alternative renderer route was used. No PDF, raster or contact sheet is supplied or claimed. The dormant export helpers are not invoked by the build sequence.

Lead signs off the **editable PPTX and curated Markdown/HTML packet** on structural, source-review and safe local execution evidence. Native visual fidelity, browser/print appearance, Linux/WSL runtime, supported-floor rehearsal, model access, participant-generated code and classroom pacing remain NOT RUN. Detailed limits, commands and artifacts are in `deliverables/VERIFICATION.md` and `verification.json`; this is not a claim those broader gates passed.

Actual final outputs: `deliverables/CITE-AI-Cybersecurity-Workshop.pptx`, `deliverables/CITE-participant-kit.zip`, `deliverables/README.html`, workbook/no-account HTML and Markdown under `deliverables/participant/teaching/`, `deliverables/FACILITATOR-GUIDE.md`/`.html`, citations/source mapping, verification and SHA-256 inventory. Reproducible code is under `integration/`; no original file outside `Workshop-Team/` was written.

## Round 2 preparation — scope settled, build still gated

Read the requested teaching proposal/narrative/agenda/workbook/verification, Linux proposal/setup/command matrix/verification, design proposal/tokens and coordinator notes. Full review exchange remains pending; no final deck has been built.

- **Core scope is settled:** minimal approved Claude prework plus Python standard library for live script/report work; installation/authentication are prework. Genuine printed/offline/no-account review remains an equal reasoning route with execution tracked separately. Codex/Hermes are optional already-approved alternatives, not extra setup tracks.
- **Schedule authority:** adopt teaching's 21-slide `agenda.json`, computed 120 minutes. The eight-minute readiness/recovery at elapsed 20–28 supersedes Linux's proposed five-minute total: three minutes checks plus five minutes recovery/transition; switch unresolved participants by minute 25. Preserve break, lab validation and Q&A. Linux guide timing needs reconciliation in the final integrated copy.
- **Exercise authority:** policy → deterministic sign-in script → static local HTML report. Keep the E01–E12 schema, exact E06/E07/E10/E11 output/reasons and explicit training boundaries. No scanner completion requirement exists. Historical script comments are not binding. The local report preserves planning/questions/build/validation without network scanning or backend installation.
- **Design authority:** adopt design tokens, accessible lab/checkpoint distinctions, concise projector copy and full workbook prompts. Use logo on title/close and any justified future divider only, not every content slide. Original eight-section division is source organization, not a required 55-slide structure. No extra untimed core slides. Use actual title placeholders and editable text blocks.
- **Render authority:** use the prepared document interpreter, python-pptx, PowerPoint native PDF export and pypdfium2 rasterization. No PyMuPDF dependency or separately drawn PDF presented as a PPTX render. Native export remains untested, despite installed PowerPoint and historical design notes about prior export.
- **Evidence status:** teacher's verification reports PASS for 120-minute structure and safe local fixture/reference checks; Linux reports limited macOS host checks and source verification, with Linux/WSL runtime not tested. These are attributed specialist evidence, not lead-reproduced results. Preserve that distinction until Round 3.

Prepared artifacts: `integration/prepare_manifest.py`, `integration/slides.json`, `integration/manifest.json`, `integration/BUILD-APPROACH.md`. The manifest captures source hashes, continuous timings, notes, full workbook prompts, source references, lab acceptance/fallback and evidence reveals. Its build authorization flag remains false until all three peer reviews are read and resolved. No blocking decision requires user input at this stage.

## Coordinator update — scope direction before Round 2

Read `Workshop-Team/COORDINATOR-NOTES.md` and `Workshop-Team/teaching/PROPOSAL.md` on 2026-11-10. The decisions below supersede conflicting Round 1 assumptions/questions later in this document. The full proposal/review exchange remains a prerequisite to final integration and build.

- **Audience:** use source-confirmed K–12 district/county IT generalists as a labeled working assumption. No further audience confirmation blocks preparation.
- **Live route and prework:** approved Claude access is the default live route; installation/login/runtime readiness are prework. A genuine offline/no-account route must include supplied source rows, flawed output, review specimens and equivalent reasoning checkpoints. It must not require another participant's account. Review completion and actual software execution are recorded separately.
- **Application exercise:** select the teaching proposal's local HTML review report built from the checked synthetic sign-in CSV as the core application-building exercise. It preserves planning, clarifying questions, a small runnable artifact and acceptance checks while avoiding scanner installation, live network targets and backend dependencies. It is a local report application, not a scanner or a claim of Nmap/Zenmap functionality. Historical builder comments do not mandate live scanner completion. Keep the original scanner idea as an explicitly optional future extension outside the 120-minute core, subject to separate lab authorization and validation.
- **Teaching proposal:** accept its three-stage policy → tested script → local report arc as the working integration direction. Its stated 21 slides, 120 minutes, fixture totals and execution evidence remain proposal claims until the lead inspects the named artifacts and runs appropriate safe checks after peer review. Do not infer successful validation from the proposal alone.
- **Build environment:** coordinator reports verified imports of `pptx`, `PIL`, `pypdf` and `pypdfium2` in `/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python`. Use that interpreter for subsequent build/testing; do not install packages into it. This supplements the earlier system-Python probe. PyMuPDF/`fitz` is not established by that report, so do not assume the old builders run unchanged.
- **Rendering:** coordinator confirms `/Applications/Microsoft PowerPoint.app` exists. Native PDF export through AppleScript is a candidate, not a verified capability. Exercise it only during authorized integration with required automation permission; distinguish an export/automation blocker from successful deck creation. Never label the separately drawn legacy PDF as a rendering of its PPTX.

### Prepared integration checklist — not a build authorization

- Receive cite-design and cite-linux proposals and all substantive Round 2 reviews through the coordinator; reconcile their recommendations here.
- Inspect teacher's agenda, narrative, workbook, answer key, provenance, fixture/reference code and verification report; agree one schema/rule contract with cite-linux.
- Confirm duration arithmetic and slide-to-agenda mapping; carry protected break, explicit recovery time and Q&A into the final manifest without double counting.
- Map each objective to a live checkpoint and a complete no-account packet; ensure the report exercise uses checked inputs and handles untrusted strings safely.
- Select design templates/fonts after cite-design review; put full copyable prompts in the workbook and preserve notes/cues/timings in the deck.
- Adapt the build under `Workshop-Team/` using the prepared interpreter and available dependencies; audit every output path before execution. Do not import the existing builders with module-scope writes.
- During Round 3, run safe fixture/script checks, construct editable slides, inspect structure, then attempt a true PowerPoint PDF export and inspect rendered pages. Record untested platforms and export limitations precisely.
- Verify final local links and distribution instructions without inventing a public URL or claiming publication.

No blocking decision at this stage. Await the remaining proposals and full Round 2 before final integration.

## Authority and round boundary

The current mandate is `Workshop-Team/TEAM-BRIEF.md` and Kevin's Round 1 instruction. The lead owns final scope, integration and sign-off. Specialists remain responsible for their assigned work: cite-design (Claude), cite-linux (Codex), cite-teacher (Codex). No agents were launched and no other panes were controlled. This document is an independent source/asset assessment, not a completed workshop or authorization to start the final build.

Only `Workshop-Team/` may receive writes. Existing notes, decks, scripts, staged/unstaged changes and attachments remain Kevin's. Historical statements such as “user clarification” inside older scripts are source assertions, not newly confirmed instructions. Conflicts with the current brief resolve in favor of the current brief; other scope conflicts remain explicit until the coordinator supplies proposals/reviews.

## Provisional assumptions and scope

| ID | Provisional decision | Reason / reopening condition |
| --- | --- | --- |
| D01 | Design for K–12 district/county IT generalists, often small teams. | `Intro.md` explicitly records that audience as confirmed in October; the current brief deliberately calls it provisional. Coordinator confirmation remains open. |
| D02 | Preserve Kevin's practical voice and the “fast junior analyst; verify the work” frame. | Strong through-line in `Intro.md`, `Guardrails.md`, `Close.md`. Avoid unsupported productivity multipliers or guaranteed time savings. No assistant cartoon persona. |
| D03 | Use one primary CLI-agent path in core instruction, provisionally Claude Code; explain transferable habits. | Most source prompts and setup material assume it. Account eligibility and approved access need specialist verification; do not promise a free provider workaround. |
| D04 | Move installation, login and any reboots to prework. In-room setup is a short readiness check with a hard fallback. | `Setup Walkthrough.md` budgets about 55 minutes; the original deck repeats this. That cannot comfortably coexist with all proposed labs in 120 minutes. |
| D05 | Prioritize a source-grounded document task and a reusable, testable log-processing task. | `Examples.md` supplies policy-to-procedure and blue-team log-triage prompts. These give observable outputs without production access. Exact fixtures, rules and timings belong to cite-teacher's proposal. |
| D06 | Keep application building in the proposed narrative, but gate a participant live Nmap-app build on rehearsal evidence and peer review. | `Application Builds.md` proposes a web Nmap front end and leaves depth open; builders disagree about allocations. A polished working scanner cannot be promised from an untested time budget. Saved-result import, live scanning and a demonstrated plan must be labeled distinctly. |
| D07 | Linux/WSL is the main setup guide; macOS/native Windows are concise alternatives. | Required by the brief. Do not blur PowerShell, Git Bash, WSL and Linux commands or assume their PATH/runtime behavior is equivalent. |
| D08 | Keep normal permissions, isolated disposable workspaces and purpose-created synthetic inputs as defaults. | Current brief supersedes `clauded` bypass instructions. No SSH-key generation, personal GitHub publishing, provider migration or plugin-bundle installation is needed for core labs. |
| D09 | Teach skills/agents/plugins briefly; optional extension depth depends on remaining time. | Preserve the source topic without adding installation risk or displacing practice/debriefs. Bash access does not enforce read-only behavior. |
| D10 | Omit prices and precise model tiers/versions unless an essential claim is verified. | Existing sources contain volatile plan/model claims. Current upstream URLs and retrieval dates are required for retained commands and material product claims. |

Broad red-team scans, real breach-address lookups, production identity changes, live district OSINT, packet-capture analysis, archive installation and multi-toolchain shopping are outside the provisional core. Do not execute installers, scanners against real networks, archives or embedded commands on Kevin's machine. No evidence upload or secret access.

## Source and asset inventory

Paths below are relative to the repository root. “Inspected” means source/text/structure inspection, not an endorsement or runtime validation.

| Asset | What exists / inspected evidence | Integration disposition |
| --- | --- | --- |
| `CLAUDE.md`, `Talk Outline.md` | Obsidian vault conventions; eight-section sequence from intro and guardrails through setup, examples, extensions, application building, adoption and close. | Preserve source traceability and relative links. `CLAUDE.md` says there is no build step, but actual Python build scripts now exist. |
| `Intro.md`, `Guardrails.md`, `Guardrails Checklist.md`, `Getting Started.md`, `Close.md` | Practical small-team framing, five guardrails, first-project advice; also bypass-alias, publishing, pricing and broad data-handling claims. | Reuse the voice and review habits. Rewrite workshop copies to remove conflicting dependencies and unverified claims. |
| `Examples.md`, `Application Builds.md` | Policy checklist, log triage, code review, GRC, exposure review and OSINT prompts; proposed Zenmap-style web app. Original log prompt asks for signals requiring history/context not supplied by a simple CSV. | Select a small core; specify deterministic training rules and expected evidence. Keep optional examples out of the timed critical path. |
| `Setup Guide.md`, `Setup Walkthrough.md`, `Skills Agents Plugins.md` | Multi-platform installation, provider routing, shell aliases, SSH/GitHub, extension tutorials. Targeted sections inspected; full platform audit remains cite-linux's work. | Cite-linux supplies verified replacements in its owned folder. Do not run the source commands to discover whether they work. |
| `Sources.md`, `Resource Index.md` | Dated citation list and broad ecosystem catalog. Sources include generic landing pages and a named threat report claim. | Discovery leads only until exact supporting sources are checked. Do not infer a report exists from a general threat-intelligence URL. |
| `Cite Talk Guide.src.html`, `Cite Talk Guide.html` | Existing editable HTML source and longer handout; setup topics overlap the Markdown. Targeted source search inspected. | Preserve existing files. Final workbook needs one clear entry point and explicit precedence over conflicting historical setup guidance. |
| `Cite-AI-Talk.pptx` | Read-only ZIP/XML inspection: 55 slides, 55 notes parts, 12192000 × 6858000 EMU (16:9). Selected setup text includes 55-minute setup, bypass alias and SSH generation. | Lecture/content baseline; not a verified two-hour hands-on workshop. No native visual inspection yet. |
| `scripts/CITE-Slides/` | Existing 55-slide PPTX, PDF proof, five preview PNGs and `deck-verification.json`. PPTX has 55 notes parts; actual dimensions approximately 16:9 despite XML `type="screen4x3"`. Existing report declares structural PASS and acknowledges no PowerPoint-native render comparison. | Prior evidence only. Lead has not reproduced its PASS or visually reviewed its images. Explicit dimensions and native rendering matter more than the type label. |
| `scripts/build_cite_deck.py` | Eight-section builder using python-pptx, Pillow, PyMuPDF and macOS font paths; writes into `scripts/CITE-Slides/`. Source includes unsafe setup shortcuts and unverified pricing. | Reference implementation only. It creates output directories at module scope; do not import or execute it unchanged. |
| `scripts/build_workshop.py` | Alternate timed workshop builder, synthetic policy/log/Nmap-shaped XML generators, answer key, prompts, facilitator text and structural checks. Writes to `scripts/workshop-deck/`, including at module scope. | Reusable ideas pending specialist review; source-generated outputs are not currently inventoried as existing deliverables. Do not inherit its “confirmed” claims or expected totals as tested facts. |
| `scripts/cheatsheet_lib.py`, `scripts/herdr_sheet.py`, `scripts/hermes_sheet.py`; `Cheat Sheets/*.pdf` | ReportLab handout infrastructure; three existing PDFs for Claude Code, Hermes and herdr. Shared layout source inspected. | Supplemental reference; no need to teach all three harnesses. Small-print handout layout does not determine slide design. |
| `Files/Mark-Title-COLOR-ForDarkBG.png`, `Files/Mark-Title-COLOR-ForLightBG.png` | Two existing brand assets. | cite-design decides accessible treatment; reuse references/copies without altering originals. |
| `Files/cisco-config.txt.md`, `Files/scan-report.pdf`, `Files/scan-report.nessus` | Config and scan artifacts exist; names/formats inventoried. Older script text asserts the PDF is fictitious, which the lead has not independently established. Nessus is not Nmap XML. | Untrusted source evidence. Require provenance and sanitization review before inclusion. Never relabel incident/source data as synthetic or silently substitute formats. |
| `Files/2026-09-29-Macfinger-ClickFix-activity.pcap.zip`, `Skills/Grc assessment-v4.zip` | Archives exist, approximately 20.7 MB and 20.9 KB respectively. Neither unpacked nor executed by lead. | Exclude from core execution. Archive presence is not approval to install or analyze it. |

## Acceptance gates for final sign-off

All gates are currently pending unless expressly identified as Round 1 inspection above.

1. **Peer decision gate:** receive all three concrete proposals and the substantive review exchange via coordinator; read them, record conflicts/resolutions here, then assign final work. No final deck build before this gate.
2. **Scope/time gate:** one authoritative agenda computes exactly 120 minutes, with positive contiguous blocks and explicit lab time, transitions, troubleshooting buffer, break if used, debriefs and Q&A. Avoid double-counting buffer inside simultaneous activities. Optional appendices consume zero core minutes. A hard-stop recovery plan names what gets cut.
3. **Learning gate:** each core objective maps to a participant action, observable checkpoint, expected result, facilitator debrief and fallback. A participant without installs/accounts has a useful reviewing/paper/offline route; pairing alone should not assume an available partner account.
4. **Safety/provenance gate:** purpose-created fixtures carry a synthetic label and generation/provenance record. Source artifacts retain their true status. No secrets, student data, host installs, permission bypass or real-network scanning enter core execution. Any future scan exercise requires explicitly scoped disposable lab targets and separate executed evidence.
5. **Technical gate:** shell/runtime/version context and prework are explicit. Retained commands/material product claims have official sources and actual retrieval dates. Record source-checked versus locally executed versus VM-required checks separately. Never describe an install as successful without execution evidence.
6. **Lab gate:** safe runnable checks test expected results and meaningful failure/boundary cases, rather than only reproducing generator constants. Assert input preservation where relevant. An app import test does not prove a backend scan works. Capture command, environment, exit result and relevant output for executed checks.
7. **Artifact gate:** editable 16:9 PPTX with usable text/shapes and notes on every instructional slide; reproducible source/build code; participant workbook; Linux/WSL setup/preflight/troubleshooting; source mapping; decision log and verification report. All new outputs stay under `Workshop-Team/`.
8. **Render/accessibility gate:** structural checks for slide size, bounds, notes and links; visual review of all slides where possible for legibility, clipping, contrast and code readability. A PDF drawn independently from shared layout instructions is a proof, not evidence of the PPTX's rendering. Deliver a real renderer export if available; document unavailable renderer/untested native behavior honestly.
9. **Delivery gate:** local artifact links resolve, documented build paths work, distribution instructions name an actually available location. Do not claim anything has been published or uploaded. Lead signs only after the evidence report identifies remaining limitations.

## Integration approach

After Round 2, freeze one content manifest under a lead-owned integration directory in `Workshop-Team/`. It should hold stable slide/lab IDs, timings, on-screen text, notes, asset references and source IDs. Use those same IDs in workbook steps, facilitator notes, fixtures and verification evidence so updates cannot silently diverge.

Specialists continue owning `design/`, `linux/`, and `teaching/`. Lead consumes reviewed outputs without overwriting their proposals/reviews. Proposed final layout: `Workshop-Team/integration/` for source/build and `Workshop-Team/deliverables/` for deck, workbook, setup guide, citations and verification; these are reserved paths, not artifacts already created. Choose implementation after cite-design's proposal and renderer/dependency assessment. Copy/adapt useful legacy builder code only after auditing output paths and module-scope side effects. Never invoke an existing builder unchanged.

Use a single authoritative PPTX as the rendering source if tooling permits. Keep a separately produced proof clearly identified. Builds must resolve assets from documented relative paths, identify fonts/dependencies and avoid silently installing anything. Maintain a verification report with separate structural, visual, lab and platform sections and statuses PASS / FAIL / NOT RUN / SOURCE-CHECKED. Re-run relevant checks after substantive integration changes.

Read-only environment probe: `/usr/bin/python3` is available but its import discovery found no `pptx`, `PIL` or `fitz`; `libreoffice`, `soffice` and `pdftoppm` were absent from the checked PATH. Nmap is present on PATH but was not executed. This does not rule out other interpreters or GUI renderers. Do not install dependencies now; assess the available approved build environment during integration.

## Questions for specialists and coordinator

**cite-design:** Recommend a restrained, accessible 16:9 system using the existing brand assets. What layouts support projected commands and long prompts without shrinking text? Specify slide/notes/workbook division, fonts with fallbacks, contrast and minimum type sizes. Identify implementation/rendering needs and review criteria. Are existing black/white section conventions useful or constraining?

**cite-linux:** Propose the smallest supported Linux/WSL preflight and runtime set. Which account/CLI instructions and normal-permission behavior are officially documented now? Separate Linux/WSL from native Windows/Git Bash and mark actual execution versus source checking. What fails on managed district laptops, and what offline/no-account route avoids live installs? If the app remains core, what disposable loopback lab, runtime and bounded validation are credible without modifying Kevin's host?

**cite-teacher:** Recommend the achievable core and compute the full 120-minute agenda including transitions, recovery and Q&A. Is a live participant scanner build credible alongside document and script practice, or should application building be facilitated/optional? Supply checkpoints, timing cut rules, precise fixture provenance and an independent expected-result strategy. Make the no-install/no-account fallback educational and concrete.

**Cross-review requests:** design ↔ teacher: what belongs on slides versus workbook/notes? linux ↔ teacher: do commands, prerequisites and fallback steps fit lab time? design ↔ linux: are command blocks legible and shell contexts unmistakable? All peers: challenge any inherited unverified claim, undocumented fixture or promised completion unsupported by a rehearsal.

**Coordinator confirmation items:** audience/attendee prerequisites; whether paid/approved accounts and prework can be required; primary CLI tool; expected Linux/WSL distribution and managed-device restrictions; whether participant live Nmap-app completion is mandatory; available lab infrastructure, internet and distribution route; any fixed brand requirements beyond existing assets. These remain questions for relay, not reasons to start building or to contact other panes.

## Round 1 evidence and handoff

Read the team brief and repository guidance; inspected the outline, framing/guardrail/adoption notes, example/application sources, citation/resource notes, targeted setup/extension/HTML sections and relevant builder/handout source. Performed read-only file inventory, PPTX ZIP/XML counts/dimensions and tool/module discovery. No build, installer, scanner, archive payload, model login, network lookup or native slide renderer was executed. No upstream claim was newly verified in this round; cite-linux's audit and final source review remain required.

Only this decisions file was authored by the lead. Round 1 is complete; await coordinator-supplied proposal and review paths before making final integration decisions.
