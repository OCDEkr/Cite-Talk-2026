# CITE 2026 — AI for Cyber Security

Workshop materials for California Information Technology in Education (CITE), prepared for K–12 IT professionals and small teams using AI to help with cybersecurity work.

This is a **content and teaching repository**, not a deployed security product or a finished application. It contains an editable PowerPoint presentation, a browser-based workshop guide, Obsidian/Markdown source notes, setup handouts, example inputs, reusable extensions, and optional authoring scripts. The local nmap web application is something participants build during the workshop; it is not supplied here as a completed app.

## Start here

| If you are… | Start with… | What to do |
|---|---|---|
| Attending or working through the material yourself | [Cite Talk Guide.html](Cite%20Talk%20Guide.html) | Open your downloaded copy in a browser. Follow the sections and copy the prompts from the guide. |
| Preparing a laptop | [Setup Guide.md](Setup%20Guide.md) | Complete the installation and approved AI-access prework. Use the operating-system instructions linked from the guide. |
| Presenting the workshop | `CITE-2026-AI-Cybersecurity-Workshop-With-Intro-Revised.pptx` | Use the current curated presentation, with [Talk Outline.md](Talk%20Outline.md) and [Setup Walkthrough.md](Setup%20Walkthrough.md) beside it. |
| Checking safe working practices | [Guardrails Checklist.md](Guardrails%20Checklist.md) | Review the checklist before sharing data, running commands, or publishing work. |
| Looking for copyable examples | [Examples.md](Examples.md) | Read the thirteen prompts, their required inputs, and the verification notes. |
| Editing or maintaining the material | The file map and authoring notes below | Keep the guide, presentation, and source notes consistent. Do not assume an older builder reproduces the current deck. |

You do not need to run a build to read the supplied HTML, Markdown, PDFs, or presentation. Use a browser, Markdown reader/Obsidian, PDF reader, and PowerPoint or another compatible presentation viewer. AI exercises and external services have their own setup and access requirements.

### Working-copy and clone warning

The file map below describes the inspected **local working copy**, not just the last Git commit:

- The current `-Intro-Revised.pptx` presentation and the earlier `-Intro-Fixed.pptx` presentation are local, untracked files at the time of inspection.
- `Skills/cisco-ios-config-audit/` is also local and untracked.
- The older tracked filename `CITE-2026-AI-Cybersecurity-Workshop-With-Intro.pptx` is missing from this working copy. It is not the file to open locally.
- `Workshop-Team/` is ignored by Git. In particular, the teaching `signins.csv` referenced by the guide is inside that ignored folder.
- `Files/claude-openrouter.cfg` is local and untracked, contains credential material, and is **not covered by the current ignore rules**. Do not commit or share it as-is.

A fresh clone will not contain untracked or ignored files, and may contain an older committed version of a modified document. Before a class or release, explicitly prepare the intended presentation, skill folder, and exercise inputs. Do not solve that by indiscriminately adding the entire working folder to Git.

The configured remote is an SSH remote. If you have access through SSH, cloning uses:

```sh
git clone git@github.com:OCDEkr/Cite-Talk-2026.git
cd Cite-Talk-2026
```

Otherwise, use the workshop copy supplied by the presenter. SSH access to this repository is not a prerequisite for creating a separate local practice repository during class.

## How the workshop works

The attendee guide is the reference for the teaching sequence:

1. **Understand the tools.** The presentation introduces an LLM, a skill, an agent, a plug-in, and the work/check/repeat loop.
2. **Work safely.** Protect data, review proposed actions, limit permissions, and verify output.
3. **Set up the working environment.** Installations and approved AI access are prework. In class, create or sign into GitHub, create a workshop folder, and initialize its local Git repository. GitHub email-verification delays do not block local Git. Remote repositories, SSH, commits, and pushing are optional follow-up.
4. **Try the examples.** Work from simpler drafting tasks toward document analysis, code review, log triage, and authorized external research. All thirteen examples remain available; not every example is a fully provisioned lab.
5. **Build an application.** Plan, design, code, run/fix, and verify a local nmap web interface. See [Application Builds.md](Application%20Builds.md). Keep the application on localhost and use the authorized local target described by the guide.
6. **Extend the tool.** Inspect and use the provided Cisco auditor skill, then examine the existing skill, agent, and plug-in examples in [Skills Agents Plugins.md](Skills%20Agents%20Plugins.md).
7. **Choose the next task.** Use [Getting Started.md](Getting%20Started.md) to select a small, repeatable task whose result you can check.

The proposed schedule is two hours, including a break. It is a pacing plan, not a guarantee that every attendee will finish every exercise. Keep a failed or incomplete run labeled as such; viewing an example is not the same as executing it.

### The thirteen examples

1. Turn a policy into a procedure.
2. Write phishing-awareness scenarios.
3. Build a ransomware tabletop.
4. Explain an alert.
5. Draft a detection rule.
6. Analyze policy gaps.
7. Vet a vendor using its privacy and terms documents.
8. Turn a scan report into a summary and remediation priorities.
9. Review a vendor script before running it.
10. Review your own cleanup automation.
11. Triage a sign-in log export.
12. Build a public-source organization exposure profile.
13. Check authorized addresses for breach exposure.

The full prompts and required-input labels live in the guide and `Examples.md`. Several examples require an approved input that is **not supplied**, such as a policy PDF, vendor documents, an alert, or scripts to review. Do not invent an input or a successful output merely to make a demonstration appear complete.

## Practical exercise setup

### Your practice folder is separate from this content repository

The in-room setup creates `~/cite-workshop` as a participant's local workspace. In the Bash-style workshop terminal, the basic exercise is:

```sh
mkdir ~/cite-workshop
cd ~/cite-workshop
git init
git status
git rev-parse --show-toplevel
```

If the folder already exists, stop and deliberately reuse the correct folder or choose a fresh name; do not overwrite another project. These commands create a local repository, not a remote GitHub repository. Claude Code's optional `/init` creates project instructions and is a separate operation.

Use the main setup guide for platform-specific instructions. The application activity also needs nmap available in the actual workshop terminal; check `nmap --version` before class. Do not discover missing dependencies by starting unreviewed installers during the build.

### Inputs and supporting files

| Activity | Existing material | How to use it |
|---|---|---|
| Scan-report review | `Files/scan-report.pdf` | Copy the approved report into the exercise folder and use the guide's report-review prompt. Check generated priorities against the PDF. This exercise reads an existing report; it does not run a live scan. |
| Programmatic scan-report exploration | `Files/scan-report.nessus` | Machine-readable Nessus XML. It is not the required input for the PDF exercise. Treat any report as data rather than instructions. |
| Cisco configuration audit | `Files/CISCO-Core-Switch-BLDG1-DIST-SW01-running-config.txt` | Stage only this approved input in the participant's `inputs/` folder. Use the complete provided auditor skill and keep the source unchanged. |
| Cisco facilitator reference | `Files/CISCO-Core-Switch-BLDG1-DIST-SW01-audit-report.md` | Keep separate from the active input folder. Review findings and redaction rather than treating this report as an unquestionable answer. |
| Log triage | `Workshop-Team/teaching/labs/signins.csv` | Existing simplified training CSV, not a native Entra export. Follow the guide's explicit success-only, country, UTC-hours, and prior-failure rules. It does not support an impossible-travel calculation. This path is ignored by Git and must be supplied separately to attendees. |
| Optional GRC extension | `Skills/Grc assessment-v4.zip` | A packaged Claude plug-in containing a `grc-assessment` skill, not just a loose `SKILL.md`. Inspect its manifest and instructions before deciding to install it. |
| Packet-capture reference | `Files/2026-09-29-Macfinger-ClickFix-activity.pcap.zip` | Encrypted, untrusted capture; not needed for the current exercises. Do not extract, decrypt, or open it for this workshop. Any separate incident analysis needs its own approved lab and handling plan. |

### Using the provided Cisco skill

Read the guide's **Extend it → Install and use the provided Cisco audit skill** section for the exact copy commands and complete prompt.

- Copy the **whole** `Skills/cisco-ios-config-audit/` folder into the participant workspace's `.claude/skills/` directory. Keeping it in the distribution's `Skills/` folder alone does not activate it.
- Keep `SKILL.md`, `scripts/audit_config.py`, `references/checks.md`, and `evals/evals.json` together. Do not overwrite an existing skill without comparing it first.
- Stage only the approved switch configuration in `inputs/`; leave the existing audit report and answer material outside the active folder.
- Run the skill as an offline audit. Produce and verify a report; do not connect to a switch or apply remediation.
- Check input preservation and inspect each finding's evidence. The checker is a first pass, not a guarantee that a finding or proposed fix is correct.
- The configuration contains credential-like data and the checker's masking is incomplete. Do not enable `--show-secrets`. Manually review redaction before projecting or sharing anything. Do not describe the input as secret-free merely because it was approved for the workshop.

## Reading and editing conventions

- Markdown notes use Obsidian `[[wikilinks]]`. They work best in Obsidian; a generic Markdown renderer may display them as plain text. Normal relative links in this README work independently of Obsidian.
- `Cite Talk Guide.html` is the browser-ready attendee guide. `Cite Talk Guide.src.html` is the authoring version and includes custom diagram markup; it is not the recommended attendee entry point. Its diagram compiler and referenced `kit.css` are not included in this repository. Keep the two files' instructional content synchronized when making changes; there is no supplied command here to compile the source guide.
- “Slide 1,” “Slide 2,” and similar headings inside source notes can be **section storyboards**, not current presentation page numbers. Use the actual deck and the current setup walkthrough for presentation navigation.
- Keep copyable prompts and long commands in the guide or notes, and keep projected slides readable. Updating a Markdown note does not automatically update an already saved PowerPoint file.
- Tool commands, model availability, and provider terms can change. Use the official references linked by the setup notes and recheck the intended route before a session; this README does not independently certify every command printed in an older cheat sheet.

## Optional authoring tools

These are for maintainers. Attendees do not need the Python document-generation stack merely to read the materials.

The scripts' imports identify these optional dependencies:

- `reportlab` for the Hermes and herdr cheat sheets.
- `python-pptx`, `Pillow`, and `PyMuPDF` (`fitz`) for the older slide/workshop builders.
- The builders reference macOS fonts under `/System/Library/Fonts/Supplemental/`; adapting them to another system requires reviewing those paths and layout assumptions.

There is no top-level dependency lockfile or single build command that recreates the current curated presentation. Review the scripts before running them: some create output directories or assemble content at import time, and `--help` is not a safe dry-run for scripts without an argument parser.

Use **Python 3.10 or later** for the cheat-sheet scripts; the system's default `python3` may be older. The two scripts accept a required output PDF path and overwrite an existing file at that path. With ReportLab installed in your chosen Python environment, examples from the repository root are:

```sh
python3 scripts/herdr_sheet.py /path/to/output/herdr-Cheat-Sheet.pdf
python3 scripts/hermes_sheet.py /path/to/output/Hermes-Agent-Cheat-Sheet.pdf
```

Choose an existing output directory and a new destination if you want to preserve existing PDFs. The supplied Claude Code cheat sheet has no corresponding generator in `scripts/`.

**Do not run the older deck builders as the workshop workflow.** They are historical variants, not a way to rebuild the current presentation:

- `scripts/build_cite_deck.py` overwrites the tracked high-contrast outputs in `scripts/CITE-Slides/`. Its built-in content includes a retired permission-bypass recommendation and references files that are now missing. Review and correct its content and output paths before any separate redevelopment use.
- `scripts/build_workshop.py` builds a different prototype. Importing it immediately creates `scripts/workshop-deck/` and an `attendee-kit/` subfolder; that output tree is not currently ignored by Git.
- `Workshop-Team/integration/` contains another local prototype's build/packaging pipeline. It has its own manifests, narrower exercise scope, and delivery artifacts. Do not substitute it for the current workshop without review.

The older builders can draw a PDF alongside a PPTX from common layout instructions. That PDF is **not** evidence that PowerPoint natively rendered the PPTX correctly. Existing verification files and preview images apply to their own build, not automatically to the latest presentation.

## Local prototype material: `Workshop-Team/`

This ignored folder contains earlier design/teaching proposals, an integration pipeline, Linux-preflight notes, training fixtures, and packaged copies. It is useful authoring/reference material, but it is **not the primary entry point for the current workshop** and will not appear in a normal clone.

- `design/`: visual tokens, mockups, example content, and review notes.
- `linux/`: Linux setup/preflight sources and recorded checks or limitations.
- `teaching/`: an earlier agenda, workbook, no-account packet, authored fixtures, reference implementations, and answer material.
- `integration/`: manifests, older builders, packaging/export helpers, fit/verification outputs, and a renderer probe.
- `deliverables/`: packaged copies of that earlier prototype, including a separate deck, participant ZIP, HTML handouts, facilitator material, and checksums.

The packaged copies are not uniformly identical to the files elsewhere in `Workshop-Team/`. The workbook, no-account packet, reference report script, and Linux preflight notes have differences; do not assume editing one copy updates the other.

The local participant ZIP and participant tree include `ANSWER-KEY` files, expected outputs, and reference implementations. **Curate those before distribution**; “participant” in a path does not mean an artifact is appropriate to give out before an exercise. Preserve the documented sibling-directory layout if using that older packet, and follow its own README rather than mixing its execution commands with the current nmap build.

## Sharing or publishing a workshop copy

Before distributing a folder or committing a release:

1. Choose the intended presentation version explicitly. Resolve the missing older tracked filename and the untracked current presentation deliberately; do not silently restore an old deck over the revised one.
2. Include the reviewed Cisco skill and required training inputs in the distributed copy. If moving an input to a tracked location, update its guide references. Do not force-add the entire ignored team folder just to obtain one CSV.
3. Exclude the private OpenRouter configuration, real credentials, OS/editor state, lock files, caches, internal proposals, and facilitator-only answers as appropriate.
4. Open the intended PPTX in PowerPoint and check its content and appearance. A package/structure check alone does not establish native compatibility or classroom pacing.
5. Check the guide's relative file links from a fresh delivery copy and rehearse the activities with the intended account, terminal, dependencies, and authorized inputs.
6. Review only the files you intend to stage. No commit, push, account creation, or network assessment is performed by this README.

## File-by-file reference

The following tables cover the tracked paths and meaningful local working files found during inspection. **Tracked** means present in Git's index, not necessarily committed with its newest contents; **local** means not tracked; **ignored local** means excluded by `.gitignore`. The missing tracked presentation is listed explicitly rather than linked to a nonexistent file.

Transient files are described collectively at the end. `README.md` is this repository overview and usage guide.

### Repository root

| File | Availability | Purpose / usage |
|---|---|---|
| `.gitignore` | tracked | Ignore rules for Obsidian/OS state, virtual environments, Office locks, Python caches, and the local team folder. |
| `Application Builds.md` | tracked | Five-stage local nmap web-app build: plan, design, code, run/fix, and verify; includes boundaries and checkpoints. |
| `CITE-2026-AI-Cybersecurity-Workshop-With-Intro-Fixed.pptx` | **local; untracked** | Earlier 44-slide corrected revision, retained for reference; use the Revised deck for the latest introduction. |
| `CITE-2026-AI-Cybersecurity-Workshop-With-Intro-Revised.pptx` | **local; untracked** | Current curated 45-slide presentation. Includes separate LLM, skill, agent, plug-in, and loop introductions. |
| `CITE-2026-AI-Cybersecurity-Workshop-With-Intro.pptx` | **tracked; missing** | Older tracked presentation filename; currently absent from disk. Its index entry is not the local revised presentation. |
| `CLAUDE.md` | tracked | Repository instructions for Claude Code: content conventions, relative links, and Git/Obsidian context. |
| `Cite Talk Guide.html` | tracked | Browser-ready attendee guide and primary navigation/copyable-prompt entry point. |
| `Cite Talk Guide.src.html` | tracked | Authoring HTML with custom diagram markup; keep its instructional content synchronized with the browser-ready guide. |
| `Examples.md` | tracked | All thirteen example prompts, input requirements, source-specific variants, and presenter/debrief notes. |
| `Getting Started.md` | tracked | Follow-up tasks, tool-adoption habits, plan considerations, and a small-team rollout approach. |
| `Guardrails Checklist.md` | tracked | Short operational checklist for exercises and for reviewing material before a GitHub push. |
| `Guardrails.md` | tracked | Presenter/source notes for reviewing actions, protecting data, limiting access, and checking results. |
| `Intro.md` | tracked | Introductory source/storyboard notes about the audience, AI-assisted work, use cases, and limitations. |
| `Resource Index.md` | tracked | Curated external repository/tool references grouped by purpose; review them before adoption. |
| `Setup Guide.md` | tracked | Attendee setup instructions, runtime-guide links, in-room GitHub/local-repository steps, optional remote steps, and recovery. |
| `Setup Walkthrough.md` | tracked | Presenter setup plan, checkpoints, timings, and current deck-page references. |
| `Skills Agents Plugins.md` | tracked | Cisco skill lab plus generic skill-writing, agent, and plug-in tutorials and existing extension references. |
| `Sources.md` | tracked | Source references supporting definitions, risks, and other talk claims. |
| `Talk Outline.md` | tracked | Current teaching sequence, proposed section budgets, intended outcomes, and links to the source notes. |

### Runtime setup guides

| File | Availability | Purpose / usage |
|---|---|---|
| `Setup Guides/Git Setup Guide.md` | tracked | Platform-specific Git check-first, installation, success-check, and recovery instructions. |
| `Setup Guides/Node.js Setup Guide.md` | tracked | Platform-specific Node.js check-first, installation, success-check, and recovery instructions. |
| `Setup Guides/Python Setup Guide.md` | tracked | Platform-specific Python/virtual-environment checks, installation instructions, and recovery. |

### Cheat sheets

| File | Availability | Purpose / usage |
|---|---|---|
| `Cheat Sheets/Claude-Code-Cheat-Sheet.pdf` | tracked | Two-page Claude Code quick reference. No matching generator is supplied in scripts/. |
| `Cheat Sheets/Hermes-Agent-Cheat-Sheet.pdf` | tracked | Two-page Hermes Agent quick reference; generated by scripts/hermes_sheet.py. |
| `Cheat Sheets/herdr-Cheat-Sheet.pdf` | tracked | Two-page herdr terminal/pane/agent quick reference; generated by scripts/herdr_sheet.py. |

### Exercise inputs, assets, and local configuration

| File | Availability | Purpose / usage |
|---|---|---|
| `Files/2026-09-29-Macfinger-ClickFix-activity.pcap.zip` | tracked | Encrypted archive containing one PCAP; untrusted incident/reference material, not a core exercise dependency. |
| `Files/CISCO-Core-Switch-BLDG1-DIST-SW01-audit-report.md` | tracked | Existing Cisco audit interpretation for facilitator/reference review; keep outside the active input folder. |
| `Files/CISCO-Core-Switch-BLDG1-DIST-SW01-running-config.txt` | tracked | Approved offline Cisco lab input. Contains credential-like data; preserve the file and review redaction. |
| `Files/Mark-Title-COLOR-ForDarkBG.png` | tracked | OCDE logo/wordmark asset intended for dark backgrounds. |
| `Files/Mark-Title-COLOR-ForLightBG.png` | tracked | OCDE logo/wordmark asset intended for light backgrounds. |
| `Files/Slide Deck Prompt.md` | tracked | Slide-authoring prompt/reference used during presentation development, not an attendee exercise. |
| `Files/claude-openrouter.cfg` | **local; untracked** | Private local shell-export configuration for Claude/OpenRouter. Contains credential material; do not publish as-is. |
| `Files/scan-report.nessus` | tracked | Machine-readable Nessus XML scan report for programmatic inspection; not the PDF lab prompt itself. |
| `Files/scan-report.pdf` | tracked | Human-readable scan-report input used by the current report-review exercise. |

### Reusable extensions

| File | Availability | Purpose / usage |
|---|---|---|
| `Skills/Grc assessment-v4.zip` | tracked | Packaged GRC plug-in archive: .claude-plugin/plugin.json and skills/grc-assessment/SKILL.md. |
| `Skills/cisco-ios-config-audit/SKILL.md` | **local; untracked** | Cisco auditor entry point: task trigger, workflow, report format, and review/secret-handling limits. |
| `Skills/cisco-ios-config-audit/evals/evals.json` | **local; untracked** | Evaluation prompts with machine-specific fixture paths; referenced test configs are not supplied. Not a runnable included test suite. |
| `Skills/cisco-ios-config-audit/references/checks.md` | **local; untracked** | Check catalogue, context and false-positive guidance, sources, and change-safety notes used by the Cisco skill. |
| `Skills/cisco-ios-config-audit/scripts/audit_config.py` | **local; untracked** | Local Python first-pass configuration checker; emits Markdown or JSON and does not contact a device. Review masking limits. |

### Maintainer scripts

| File | Availability | Purpose / usage |
|---|---|---|
| `scripts/build_cite_deck.py` | tracked | Older high-contrast deck/PDF/preview builder targeting scripts/CITE-Slides/; not the curated 45-slide-deck source. |
| `scripts/build_workshop.py` | tracked | Separate workshop prototype builder targeting scripts/workshop-deck/, including its own support material and fixtures. |
| `scripts/cheatsheet_lib.py` | tracked | Shared ReportLab page layout, text, section, and callout helpers for the two generated cheat sheets. |
| `scripts/herdr_sheet.py` | tracked | Generates the herdr PDF to the positional output path; reports column overflow warnings. |
| `scripts/hermes_sheet.py` | tracked | Generates the Hermes PDF to the positional output path; reports column overflow warnings. |

### Older generated presentation outputs

| File | Availability | Purpose / usage |
|---|---|---|
| `scripts/CITE-Slides/CITE-AI-Talk-High-Contrast.pdf` | tracked | 55-page PDF proof from that older builder; not native rendering evidence for the root deck. |
| `scripts/CITE-Slides/CITE-AI-Talk-High-Contrast.pptx` | tracked | Separate generated 55-slide high-contrast presentation, not the current root presentation. |
| `scripts/CITE-Slides/deck-verification.json` | tracked | That older build's checks and rendering limitations; not a certification of the current deck. |
| `scripts/CITE-Slides/preview-1.png` | tracked | Preview/contact-sheet image 1 for the older generated high-contrast deck, not the current root deck. |
| `scripts/CITE-Slides/preview-2.png` | tracked | Preview/contact-sheet image 2 for the older generated high-contrast deck, not the current root deck. |
| `scripts/CITE-Slides/preview-3.png` | tracked | Preview/contact-sheet image 3 for the older generated high-contrast deck, not the current root deck. |
| `scripts/CITE-Slides/preview-4.png` | tracked | Preview/contact-sheet image 4 for the older generated high-contrast deck, not the current root deck. |
| `scripts/CITE-Slides/preview-5.png` | tracked | Preview/contact-sheet image 5 for the older generated high-contrast deck, not the current root deck. |

<details>
<summary>Complete local Workshop-Team inventory (ignored; not the primary workshop)</summary>

### Local team — coordination

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/COORDINATOR-NOTES.md` | ignored local | Internal coordinator notes for the earlier team/prototype work. |
| `Workshop-Team/DECISIONS.md` | ignored local | Internal decisions and scope record for that prototype. |
| `Workshop-Team/TEAM-BRIEF.md` | ignored local | Internal team roles, goals, constraints, and assignments. |

### Local team — design

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/design/PEER-REVIEW.md` | ignored local | Internal specialist review/findings for this workstream. |
| `Workshop-Team/design/PROPOSAL.md` | ignored local | Specialist proposal for this folder's workstream; not current attendee instructions. |
| `Workshop-Team/design/check_tokens.py` | ignored local | Checks proposed design tokens/content against the older design constraints. |
| `Workshop-Team/design/example-slides.json` | ignored local | Example/proposed slide content for the earlier design work. |
| `Workshop-Team/design/slide-manifest.json` | ignored local | Earlier design slide manifest and sequencing information. |
| `Workshop-Team/design/template-mockups-r2.svg` | ignored local | Revised editable SVG design mockups. |
| `Workshop-Team/design/template-mockups.svg` | ignored local | Initial editable SVG mockups for the older deck design. |
| `Workshop-Team/design/tokens.json` | ignored local | Earlier design palette, typography, and layout tokens. |

### Local team — linux

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/linux/COMMAND-VERIFICATION.md` | ignored local | Linux/setup command-review record and execution limitations. |
| `Workshop-Team/linux/CORRECTIONS.md` | ignored local | Corrections recorded during the local Linux/preflight review. |
| `Workshop-Team/linux/PEER-QUESTIONS.md` | ignored local | Internal questions exchanged during the Linux/preflight review. |
| `Workshop-Team/linux/PEER-REVIEW.md` | ignored local | Internal specialist review/findings for this workstream. |
| `Workshop-Team/linux/PROPOSAL.md` | ignored local | Specialist proposal for this folder's workstream; not current attendee instructions. |
| `Workshop-Team/linux/SETUP-PREFLIGHT.md` | ignored local | Earlier Linux-specific setup/readiness instructions for the local prototype. |
| `Workshop-Team/linux/VERIFICATION.md` | ignored local | Recorded checks and limitations for this older workstream or package, not current-deck native approval. |
| `Workshop-Team/linux/preflight.sh` | ignored local | Linux readiness/preflight shell helper; inspect it and its intended environment before running. |

### Local team — teaching

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/teaching/AGENDA.md` | ignored local | Computed/timed agenda for the earlier local workshop prototype. |
| `Workshop-Team/teaching/ANSWER-KEY.md` | ignored local | Facilitator answers for the earlier training exercises; separate from participant work until reveal. |
| `Workshop-Team/teaching/NO-ACCOUNT-PACKET.md` | ignored local | Standalone authored print/offline review packet for the earlier prototype; review is not live AI execution. |
| `Workshop-Team/teaching/PARTICIPANT-WORKBOOK.md` | ignored local | Earlier prototype workbook with tasks, checkpoints, command contexts, and lab references. |
| `Workshop-Team/teaching/PEER-REVIEW.md` | ignored local | Internal specialist review/findings for this workstream. |
| `Workshop-Team/teaching/PROPOSAL.md` | ignored local | Specialist proposal for this folder's workstream; not current attendee instructions. |
| `Workshop-Team/teaching/SLIDE-NARRATIVE.md` | ignored local | Presenter narrative/content mapping for the earlier teaching proposal. |
| `Workshop-Team/teaching/SOURCES-AND-VERIFICATION.md` | ignored local | Teaching-source mapping, provenance, and checks/limitations for the earlier material. |
| `Workshop-Team/teaching/SUPPORT-SLIDES.md` | ignored local | Earlier support-view content and parent-exercise relationships. |
| `Workshop-Team/teaching/agenda.json` | ignored local | Machine-readable earlier teaching agenda and timings. |
| `Workshop-Team/teaching/build_packet.py` | ignored local | Builds the earlier standalone teaching/offline packet from its authored material and fixtures. |
| `Workshop-Team/teaching/labs/PROVENANCE.md` | ignored local | Training-fixture origin and exact log-rule contract; read before interpreting expected results. |
| `Workshop-Team/teaching/labs/check_triage.py` | ignored local | Checker comparing a trainee result against independently specified expected log events. |
| `Workshop-Team/teaching/labs/expected-events.csv` | ignored local | Hand-authored expected sign-in results; facilitator/checker material. |
| `Workshop-Team/teaching/labs/expected-review.html` | ignored local | Generated reference HTML output for comparing the older reporting exercise; not a model response or screenshot. |
| `Workshop-Team/teaching/labs/offboarding-policy.txt` | ignored local | Authored fictional offboarding-policy exercise input. |
| `Workshop-Team/teaching/labs/reference_report.py` | ignored local | Reference local HTML-report implementation for the older prototype. |
| `Workshop-Team/teaching/labs/reference_triage.py` | ignored local | Reference implementation of the earlier teaching log contract; facilitator example, not proof generated code is safe. |
| `Workshop-Team/teaching/labs/report-empty.csv` | ignored local | Header-only CSV fixture for empty-data behavior. |
| `Workshop-Team/teaching/labs/report-markup.csv` | ignored local | Invented text/markup fixture for HTML-escaping tests. |
| `Workshop-Team/teaching/labs/report-wrong-columns.csv` | ignored local | Intentionally invalid-column CSV fixture for input-validation tests. |
| `Workshop-Team/teaching/labs/review-snippet.txt` | ignored local | Deliberately flawed inert code-review specimen, not production automation to execute. |
| `Workshop-Team/teaching/labs/signins.csv` | ignored local | Invented simplified sign-in training rows; reused by the current guide, but stored in this ignored folder. |
| `Workshop-Team/teaching/projection-content.json` | ignored local | Projection-ready teaching content for the older integration pipeline. |
| `Workshop-Team/teaching/validate_teaching.py` | ignored local | Checks the earlier teaching package/fixture contract and generated teaching artifacts. |
| `Workshop-Team/teaching/verification.json` | ignored local | Machine-readable results from an older workstream/package validation run. |

### Local team — integration

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/integration/BUILD-APPROACH.md` | ignored local | Earlier integration build plan, interpreter/dependency assumptions, and verification approach. |
| `Workshop-Team/integration/build_deck.py` | ignored local | Builds the separate older Workshop-Team deck from its manifests; not the root revised presentation. |
| `Workshop-Team/integration/core-slides.json` | ignored local | Earlier timed/core slide definitions used by the integration build. |
| `Workshop-Team/integration/export_powerpoint.applescript` | ignored local | Native PowerPoint export helper for the older pipeline; review paths and obtain required app permissions. |
| `Workshop-Team/integration/extracted-kit-verification.json` | ignored local | Recorded checks against an extracted copy of the older participant kit. |
| `Workshop-Team/integration/manifest-lint.txt` | ignored local | Recorded older manifest-lint results. |
| `Workshop-Team/integration/manifest.json` | ignored local | Earlier integration manifest containing slide/teaching contract data. |
| `Workshop-Team/integration/package_workshop.py` | ignored local | Packages the older workshop deliverables, HTML copies, ZIP, and related release records. |
| `Workshop-Team/integration/prepare_manifest.py` | ignored local | Prepares the older integration manifest from its design/teaching sources. |
| `Workshop-Team/integration/probe/STATUS.md` | ignored local | Renderer-probe status and recorded availability/approval limits. |
| `Workshop-Team/integration/probe/create_probe.py` | ignored local | Creates a minimal presentation for renderer-capability testing. |
| `Workshop-Team/integration/probe/renderer-probe.pptx` | ignored local | Minimal renderer probe, not workshop slide content. |
| `Workshop-Team/integration/run_export.py` | ignored local | Runner for the older native PowerPoint export helper; not an automatic permission bypass. |
| `Workshop-Team/integration/slides.json` | ignored local | Older integration slide content/definitions. |
| `Workshop-Team/integration/text-fit-report.json` | ignored local | Recorded estimated text-fit checks for the older build; not a native rendering. |
| `Workshop-Team/integration/verify_final.py` | ignored local | Earlier package/deck verifier; its results are scoped to that pipeline and its fixtures. |

### Local team — deliverables

| File | Availability | Purpose / usage |
|---|---|---|
| `Workshop-Team/deliverables/CITE-AI-Cybersecurity-Workshop.pptx` | ignored local | Separate older local workshop presentation with a narrower exercise contract. |
| `Workshop-Team/deliverables/CITE-participant-kit.zip` | ignored local | Packaged older participant tree; includes answer/reference material and requires curation before class. |
| `Workshop-Team/deliverables/FACILITATOR-GUIDE.html` | ignored local | Earlier prototype facilitator instructions, timings, prompts, and debriefs. HTML/browser counterpart. |
| `Workshop-Team/deliverables/FACILITATOR-GUIDE.md` | ignored local | Earlier prototype facilitator instructions, timings, prompts, and debriefs. |
| `Workshop-Team/deliverables/README.html` | ignored local | Browser/print counterpart of the older deliverables README. |
| `Workshop-Team/deliverables/README.md` | ignored local | Entry guide for the older local deliverables package and its separate build/exercise scope. |
| `Workshop-Team/deliverables/SHA256SUMS.txt` | ignored local | Checksums for that older packaged release; not automatically current after edits. |
| `Workshop-Team/deliverables/SOURCES-AND-MAPPING.html` | ignored local | Earlier package source mapping and provenance notes. HTML/browser counterpart. |
| `Workshop-Team/deliverables/SOURCES-AND-MAPPING.md` | ignored local | Earlier package source mapping and provenance notes. |
| `Workshop-Team/deliverables/VERIFICATION.html` | ignored local | Recorded checks and limitations for this older workstream or package, not current-deck native approval. HTML/browser counterpart. |
| `Workshop-Team/deliverables/VERIFICATION.md` | ignored local | Recorded checks and limitations for this older workstream or package, not current-deck native approval. |
| `Workshop-Team/deliverables/facilitator/LINUX-VERIFICATION.html` | ignored local | Packaged facilitator Linux verification/limitations record. HTML/browser counterpart. |
| `Workshop-Team/deliverables/facilitator/LINUX-VERIFICATION.md` | ignored local | Packaged facilitator copy: Packaged facilitator Linux verification/limitations record. |
| `Workshop-Team/deliverables/facilitator/TEACHING-SOURCES-AND-VERIFICATION.html` | ignored local | Packaged facilitator teaching-provenance and verification record. HTML/browser counterpart. |
| `Workshop-Team/deliverables/facilitator/TEACHING-SOURCES-AND-VERIFICATION.md` | ignored local | Packaged facilitator copy: Packaged facilitator teaching-provenance and verification record. |
| `Workshop-Team/deliverables/participant/README.html` | ignored local | Browser/print counterpart of the earlier participant README. |
| `Workshop-Team/deliverables/participant/README.md` | ignored local | Entry guide for the earlier packaged participant tree; not this repository's primary guide. |
| `Workshop-Team/deliverables/participant/linux/COMMAND-VERIFICATION.html` | ignored local | Linux/setup command-review record and execution limitations. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/linux/COMMAND-VERIFICATION.md` | ignored local | Packaged copy: Linux/setup command-review record and execution limitations. |
| `Workshop-Team/deliverables/participant/linux/SETUP-PREFLIGHT.html` | ignored local | Earlier Linux-specific setup/readiness instructions for the local prototype. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/linux/SETUP-PREFLIGHT.md` | ignored local | Packaged copy: Earlier Linux-specific setup/readiness instructions for the local prototype. |
| `Workshop-Team/deliverables/participant/linux/preflight.sh` | ignored local | Packaged copy: Linux readiness/preflight shell helper; inspect it and its intended environment before running. |
| `Workshop-Team/deliverables/participant/teaching/AGENDA.html` | ignored local | Computed/timed agenda for the earlier local workshop prototype. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/teaching/AGENDA.md` | ignored local | Packaged copy: Computed/timed agenda for the earlier local workshop prototype. |
| `Workshop-Team/deliverables/participant/teaching/ANSWER-KEY.html` | ignored local | Facilitator answers for the earlier training exercises; separate from participant work until reveal. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/teaching/ANSWER-KEY.md` | ignored local | Packaged copy: Facilitator answers for the earlier training exercises; separate from participant work until reveal. |
| `Workshop-Team/deliverables/participant/teaching/NO-ACCOUNT-PACKET.html` | ignored local | Standalone authored print/offline review packet for the earlier prototype; review is not live AI execution. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/teaching/NO-ACCOUNT-PACKET.md` | ignored local | Packaged copy: Standalone authored print/offline review packet for the earlier prototype; review is not live AI execution. |
| `Workshop-Team/deliverables/participant/teaching/PARTICIPANT-WORKBOOK.html` | ignored local | Earlier prototype workbook with tasks, checkpoints, command contexts, and lab references. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/teaching/PARTICIPANT-WORKBOOK.md` | ignored local | Packaged copy: Earlier prototype workbook with tasks, checkpoints, command contexts, and lab references. |
| `Workshop-Team/deliverables/participant/teaching/labs/PROVENANCE.html` | ignored local | Training-fixture origin and exact log-rule contract; read before interpreting expected results. HTML/browser counterpart. |
| `Workshop-Team/deliverables/participant/teaching/labs/PROVENANCE.md` | ignored local | Packaged copy: Training-fixture origin and exact log-rule contract; read before interpreting expected results. |
| `Workshop-Team/deliverables/participant/teaching/labs/check_triage.py` | ignored local | Packaged copy: Checker comparing a trainee result against independently specified expected log events. |
| `Workshop-Team/deliverables/participant/teaching/labs/expected-events.csv` | ignored local | Packaged copy: Hand-authored expected sign-in results; facilitator/checker material. |
| `Workshop-Team/deliverables/participant/teaching/labs/expected-review.html` | ignored local | Packaged copy: Generated reference HTML output for comparing the older reporting exercise; not a model response or screenshot. |
| `Workshop-Team/deliverables/participant/teaching/labs/offboarding-policy.txt` | ignored local | Packaged copy: Authored fictional offboarding-policy exercise input. |
| `Workshop-Team/deliverables/participant/teaching/labs/reference_report.py` | ignored local | Packaged copy: Reference local HTML-report implementation for the older prototype. |
| `Workshop-Team/deliverables/participant/teaching/labs/reference_triage.py` | ignored local | Packaged copy: Reference implementation of the earlier teaching log contract; facilitator example, not proof generated code is safe. |
| `Workshop-Team/deliverables/participant/teaching/labs/report-empty.csv` | ignored local | Packaged copy: Header-only CSV fixture for empty-data behavior. |
| `Workshop-Team/deliverables/participant/teaching/labs/report-markup.csv` | ignored local | Packaged copy: Invented text/markup fixture for HTML-escaping tests. |
| `Workshop-Team/deliverables/participant/teaching/labs/report-wrong-columns.csv` | ignored local | Packaged copy: Intentionally invalid-column CSV fixture for input-validation tests. |
| `Workshop-Team/deliverables/participant/teaching/labs/review-snippet.txt` | ignored local | Packaged copy: Deliberately flawed inert code-review specimen, not production automation to execute. |
| `Workshop-Team/deliverables/participant/teaching/labs/signins.csv` | ignored local | Packaged copy: Invented simplified sign-in training rows; reused by the current guide, but stored in this ignored folder. |
| `Workshop-Team/deliverables/verification.json` | ignored local | Machine-readable results from an older workstream/package validation run. |

</details>


## Transient and application-managed files

| Path or pattern | Purpose |
|---|---|
| `.git/` | Git history and repository metadata. Manage with Git rather than editing its internals. |
| `.obsidian/` | Local Obsidian settings/workspace state; ignored and not required to read the Markdown. |
| `.DS_Store`, `Thumbs.db` | Operating-system metadata, not workshop content. |
| `~$*.pptx` and other `~$*` files | Office lock files for open documents, not valid presentations or source material. Do not try to open them as decks. |
| `__pycache__/` | Generated Python bytecode caches. |
| `.venv/` | Optional local Python environment; ignored, not a deliverable. |
| `.trash/` | Obsidian/local trash, if present; not workshop material. |

Only the explicitly selected attendee materials should be distributed. Keep source/reference material available for maintainers without treating every local artifact as part of the class handout.
