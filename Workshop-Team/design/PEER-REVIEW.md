# Design peer review: round 2

Reviewer: cite-design (Claude). Date: 2026-11-10. The lead owns every final call. Everything here is a recommendation unless it quotes a measured result. I did not build a deck, and I wrote only inside `Workshop-Team/design/`.

Read for this review: `teaching/PROPOSAL.md`, `teaching/SLIDE-NARRATIVE.md`, `teaching/PARTICIPANT-WORKBOOK.md`, `teaching/AGENDA.md` and `agenda.json`, `teaching/labs/PROVENANCE.md`, `linux/PROPOSAL.md`, `linux/SETUP-PREFLIGHT.md`, `linux/PEER-QUESTIONS.md`, `DECISIONS.md`, `COORDINATOR-NOTES.md`.

## Summary

The teaching arc (policy → tested script → local report, 21 slides) fits a projected deck well. Lab slides stay up during work, so the slide count is right, and only three of the 21 slides need code on screen. Linux's prework-first, one-agent, no-bypass position is compatible with it. Three things still need reconciling before integration: the readiness block (8 minutes vs a 5-minute gate), route naming (two routes vs three), and shell/context labeling. Workbook command blocks currently have no context label. I've proposed one shared vocabulary for each, encoded in `tokens.json` and checked by `check_tokens.py`.

## 0. Corrections to my round-1 proposal

Also recorded at the top of `design/PROPOSAL.md`.

| Round-1 claim | Correction |
|---|---|
| "No Python here imports pptx/fitz/PIL; lead must set up a venv." | That was a probe of system Python only. **Verified by import today** in the coordinator's interpreter `/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python`: python-pptx 1.0.2, Pillow 13.0.0, pypdf 6.21.4, pypdfium2 present; **PyMuPDF (`fitz`) absent**. The legacy parallel-PDF path can't run unchanged there, and shouldn't be revived anyway. |
| "Kevin's existing choices to keep: black dividers, logo on every slide, eight-section order." | Inferred from assertions in `scripts/build_cite_deck.py`, not established by the brief. Relabelled as **suggestions**. The eight-section order belongs to the lecture outline. The 21-slide teaching arc governs this deliverable unless the lead decides otherwise. |
| "PowerPoint PDF export worked on 2026-11-09." | That came from my own prior-session notes, not this team's evidence. Per coordinator notes it is **not exercised**, and it may need automation permission. It's a candidate renderer, nothing more. |
| "Evolve `build_cite_deck.py`." | Agree with `DECISIONS.md`: don't import or run legacy builders (module-scope writes). Copy patterns into the lead's integration folder only. |
| Code limit 64 chars at 20 pt; `$` prompt marker | Measured Consolas advance is **11.0 pt/char at 20 pt** (Pillow 13 + PowerPoint's bundled `Consola.ttf`), so an 824 pt panel holds 74.9 chars. The limit is now **72 at 20 pt and 82 at the 18 pt floor**. The `$` marker is replaced by a context tab, so slides match the copyable workbook text. |
| One checkpoint template (working/partial/blocked) | Split into a **reveal/check** slide for teaching's slides 10, 15 and 19, and a **status-call strip** on lab slides for the mid-lab hand polls at 36, 64 and 98. This adds no slides and doesn't change the agenda. |

## 1. Teaching proposal, narrative and workbook

### Agreements
- **One workflow taught three times** suits a consistent visual grammar: the same lab template three times, so the room learns the layout once.
- **Full prompts in the workbook, concise screen text** matches my round-1 rule. The narrative's "Screen" lines are already short; all 21 pass the density linter (see §4).
- **Answer reveals separated from work slides** (teacher Q4). Yes. The manifest marks slides 10, 15 and 19 as `reveal`, and the checker fails a reveal placed before any lab.
- **Lab slides carry duration, filename, outcome and fallback** (teacher Q4). Yes. The lab template has a header band (lab number, minutes, "Stop at", provenance), a phase strip, steps, at most one command block, DONE WHEN and STUCK? boxes, and a workbook reference. The checker requires `minutes`, `elapsed`, `done_when`, `fallback`, `workbook_ref` and `provenance`.
- **No color-only pass/fail.** The teacher states it, and my templates already pair every state with a glyph and a word.
- **Fixture provenance** (`labs/PROVENANCE.md`): purpose-made, with the policy labelled fictional and the CSV labelled synthetic. Slides should carry exactly those labels: `FICTIONAL POLICY` on Lab 1, `SYNTHETIC` on Labs 2–3. No supplied scan, pcap or config appears on any slide.

### Timing review (computed, not estimated)
- Independent recomputation of `agenda.json`: **21 rows, 120 minutes**. `check_tokens.py --agenda` also verifies that every manifest slide's minutes and title match the agenda and that contiguous elapsed ranges run 00–02 … 115–120. Result: PASS. Teaching's own `validate_teaching.py` also reports PASS (I ran it read-only from the repo root).
- Hands-on share: lab work blocks are 10 + 18 + 13 = 41 minutes, plus 4 minutes of pair practice on slides 4–5 and 3 minutes of instruction-writing on slide 16. Checks and debriefs on slides 10, 11, 15 and 19 add 19 minutes. That's a credible hands-on workshop.
- **Front-loading:** minutes 0–20 are six talk-led slides before readiness. Slides 4 and 5 include pair activities, so this is acceptable. I wouldn't add content there.
- **Risk, not design's call:** in slide 9 (Lab 1) the generate-or-repair phase is 5 minutes. Model latency for a full four-system table can eat most of that. The specimen fallback covers it, and the phase strip makes the switch point visible.
- **Clock notation conflict:** my round-1 mockups used `0:52`, while teaching uses elapsed minutes (`57–75`) and "Return at elapsed 53:00". Recommendation: **elapsed minutes everywhere on slides** (`elapsed 57–75`, "Stop at 75"), with wall-clock time only on the break slide, as an editable `__:__` field the presenter fills in on the day. Elapsed time doesn't depend on the actual start time; wall-clock time does.

### 21-slide scope review
- 21 slides over 120 minutes averages 5.7 minutes per slide. Right for a lab workshop. Don't pad.
- **No section dividers are needed.** The old black-divider convention served an eight-section lecture. Here I suggest a black surface only for slides 1 and 21, with an eyebrow phase label on content slides (`WARM-UP`, `READINESS`, `LAB 1`, `LAB 2`, `REVIEW HABIT`, `LAB 3`, `CLOSE`).
- **Hidden appendix (zero minutes):** add hidden slides after slide 21 for specimens A, B and C, the Linux troubleshooting table, and a "saved example" backup per lab. Each would carry the `SAVED EXAMPLE · NOT LIVE OUTPUT` context label. That lets the facilitator show a specimen on screen when a model stalls without touching the timed agenda. The agenda validator should count only visible slides.
- **Densest slide:** slide 14 (Lab 2, 18 minutes) holds 4 steps, 2 command lines, the done/stuck boxes, a 4-phase strip and a status strip. My render (`template-mockups-r2.svg`) shows it fits at full size, but it is at capacity. Nothing more can go on it. The code-review snippet stays in the workbook ("Review the snippet. Do not run it.").

### Conflicts and fixes for the workbook (teacher + linux)
1. **Command blocks have no context label.** A ` ```bash ` fence, a ` ```text ` prompt and the in-session `/permissions` look alike once printed. Fix: put one bold label line above every block, using the shared vocabulary in §3 (e.g. **Ubuntu/WSL Bash · normal user · in the kit copy**, **Prompt · paste into the agent**, **Inside the agent session**).
2. **Long `python3 -c` one-liners** (80, 82 and 95 characters, measured) are hard to read and retype, and they won't fit a slide. On the primary Linux/WSL path, suggest `ls -l labs/signins.csv`, `cat labs/signins.csv` and `cat work/offboarding-checklist.md`. Keep the `py -3`/Python form in the native-Windows appendix. This is the teacher's and linux's call. I've used `ls -l` on slide 7 of the manifest as a marked suggestion.
3. **The no-account route reads as a footnote:** a bold paragraph after each lab's checks. Linux Q4 asks for equal weight, and so do I. Fix: give each lab three parallel sub-headings (Live agent / Local script / Paper review) with the **same check list**, differing only in the "Record" line (Executed / Executed (reference) / Reviewed).
4. **Print layout:** navy-filled code blocks waste toner and print poorly in grayscale. Suggest the workbook (print and PDF) use a light panel with a 2 pt left rule plus the context label, and keep the navy stage for slides only. I can supply a print stylesheet in round 3 if the lead wants one.
5. **Status vocabulary:** Lab 1's narrative asks "drafting, reviewing, blocked". Use one set for all three polls: **▶ RUNNING · ✎ REVIEWING · ✕ STUCK → SPECIMEN**, printed on the lab slide strip and spoken by the facilitator.

## 2. Linux proposal and setup preflight

### Agreements
- Prework for all installs and logins; one live agent; no bypass alias; no SSH, gh, plugins or herdr in core; `curl -k`, VPN shutdown and similar fixes are excluded. Design implication: **no install command appears on any in-room slide.** The checker rejects the `admin` context on slides.
- "Give each platform command its own copyable block; never mix Windows and Linux installers in one unlabeled block" (linux design Q2). Adopted as a rule in `tokens.json` → `contexts`.
- Source and retrieval date on technical reference material (linux design Q3). These go in the workbook and the hidden appendix slides, not on main slides. The footer of an appendix slide can carry `Source · retrieved 2026-11-10`.

### Conflicts and fixes
1. **Readiness duration:** linux proposes a 5-minute gate; teaching allocates 8 minutes (3 readiness + 5 buffer) on slide 7. These are compatible without changing the agenda. Run linux's 5-step gate from 20 to 25 (it matches teaching's "move unresolved to review by minute 25"), then 25–28 is buffer and transition. The slide shows three equal route cards, three Bash checks and "By minute 28, everyone proceeds."
2. **Route naming:** teaching names two routes (run / review); linux names three (live agent / local files + Python / paper). The workbook already implies three ("With Python but no account you may inspect/run the reference"). Recommendation: three canonical routes, **LIVE AGENT ▶ / LOCAL SCRIPT ■ / PAPER REVIEW ✎**, in `tokens.json` → `routes` with their record labels. Glyph plus word, so they survive grayscale.
3. **Agent readiness check differs:** teaching uses `claude`, then `/permissions`; linux uses `claude --permission-mode default`, `/status`, `/permissions` and a "Reply with READY…" prompt. The lead or linux should pick one sequence. Design need: the agent-side check belongs in the workbook under an **Inside the agent session** label. The slide shows only the three shell checks.
4. **Line length in prework:** the installer download lines measure 80–100 characters (Hermes curl line: 100). They're workbook-only, but at typical print sizes (9–10 pt mono on Letter) a 100-character line wraps mid-URL. Suggest a `\` continuation after `-fL` so no URL is split by the printer.
5. **Tool neutrality on slides:** linux says Codex is an alternative and Hermes optional; teaching keeps prompts tool-neutral. Suggest slides say "the agent" everywhere. Name a product only where a check is product-specific, which is in the workbook.

### Answers to linux's design questions
- **Context labels legible in print and without color?** Yes: label text plus border style carries the meaning (§3). Contrast: gold label on the navy stage is 9.10:1, and white code on the stage is 16.83:1 (from `check_tokens.py`).
- **Separate copyable blocks per platform:** yes, enforced as a rule.
- **Source/date placement:** workbook and appendix, as above.
- **Visibly equal no-account route:** yes, three equal cards on slide 7 and parallel sub-headings in the workbook (fix 3 in §1).

## 3. Shell and context labeling spec (shared by slides and workbook)

A tab above each block holds the label. No prompt marker (`$`, `PS>`, `#`) goes inside copyable text. Meaning never depends on color.

| Context key | Label | Slide surface / border | On slides? |
|---|---|---|---|
| `bash` | UBUNTU / WSL BASH · NORMAL USER (· IN THE KIT COPY) | navy stage, solid | yes |
| `agent` | INSIDE THE AGENT SESSION | navy stage, double left rule | yes |
| `prompt` | PROMPT · PASTE INTO THE AGENT | navy stage, sans text, excerpt at most 35 words | yes |
| `review` | REVIEW ONLY · DO NOT RUN | light panel, dotted border | yes |
| `data` | DATA · NOT AN INSTRUCTION | light panel, dotted border | yes (slide 6) |
| `saved` | SAVED EXAMPLE · NOT LIVE OUTPUT | light panel, dashed border | appendix |
| `admin` | WINDOWS POWERSHELL · ADMINISTRATOR · PREWORK ONLY | heavy dashed border | **no**, workbook and setup guide only |

The light-panel contexts (`review`, `data`, `saved`) deliberately don't use the navy "run" surface, so non-runnable text never looks runnable.

## 4. Command density review (measured)

| Command (source) | Chars | Fits 20 pt (≤72)? | Placement |
|---|---:|---|---|
| `python3 work/triage.py labs/signins.csv work/flagged-events.csv` (workbook Lab 2) | 63 | yes | slide 14 + workbook |
| `python3 labs/check_triage.py work/flagged-events.csv` | 51 | yes | slide 14 + workbook |
| `python3 work/build_report.py work/flagged-events.csv work/review.html` (Lab 3) | 69 | yes | slide 18 + workbook |
| `python3 labs/reference_triage.py labs/signins.csv work/reference-events.csv` | 75 | 18 pt only | workbook / appendix |
| `python3 labs/reference_report.py work/reference-events.csv work/reference-review.html` | 85 | no | workbook only |
| `python3 -c "…Path('labs/signins.csv').is_file()…"` (readiness) | 80 | no | replace with `ls -l` (suggestion) |
| `python3 -c "…read_text()…"` (Lab 1 / Lab 2 viewers) | 95 / 82 | no | replace with `cat` (suggestion) |
| Installer curl lines (linux prework) | 80–100 | no | workbook/prework only, with `\` continuation |

Only slides 7, 14 and 18 need commands, at most 3 lines each. The lab prompts (Lab 2 is about 200 words) belong in the workbook, with a 35-word excerpt on demo slides 8 and 17.

## 5. DECISIONS.md and coordinator notes

- Agree with the D04/D08 direction (prework; normal permissions; synthetic inputs) and with the coordinator's scope update (local HTML report, not a scanner). Design consequence: no "Zenmap clone" or scanner imagery or wording on slides. Slide 17 says "local review report".
- Render gate: agree that a parallel-drawn PDF is not a render. For round 3, I propose this order. Build the PPTX with the prepared interpreter. Attempt the PowerPoint AppleScript export. If it succeeds, rasterize with **pypdfium2** (available) for the contact sheet and my visual review. If it fails, record the exact blocker and review the PPTX structure only, labelled "not rendered."
- Structural checks to add to the lead's `verify()` (from round 1, still valid): every run is at least 14 pt; audience body text is at least 20 pt; a title per slide; `descr` alt text on every picture; no banned color pairs; lab slides have done/stuck; hidden appendix slides are excluded from the timing total.

## 6. Concrete integration fixes, by owner

| # | Fix | Owner |
|---|---|---|
| 1 | Use `design/slide-manifest.json` as design input to the lead's integration manifest (template kind, screen text, blocks, provenance, phases, status-call minute per slide). It passes `check_tokens.py --agenda teaching/agenda.json`. | lead |
| 2 | Run linux's 5-step gate inside teaching's 20–28 block (20–25 gate, 25–28 buffer). | lead / teacher / linux |
| 3 | Adopt the three canonical route names and the record labels. | teacher / linux |
| 4 | Add context labels above every workbook code block; keep no prompt markers inside blocks. | teacher / linux |
| 5 | Replace `python3 -c` file viewers with `ls -l` / `cat` on the Linux/WSL path. | teacher / linux decide |
| 6 | Give the paper-review route its own parallel sub-heading and checks in each lab. | teacher |
| 7 | One status vocabulary for mid-lab polls (RUNNING / REVIEWING / STUCK → SPECIMEN). | teacher |
| 8 | Use elapsed-minute notation on slides; the break slide gets an editable wall-clock field. | lead |
| 9 | Hidden zero-minute appendix: specimens A–C, saved examples, troubleshooting. | lead / teacher |
| 10 | Pick one agent-readiness sequence for the workbook. | linux / lead |
| 11 | No in-room slide shows install, admin or bypass commands (checker enforces `admin` off slides). | lead |
| 12 | The render path is PowerPoint export → pypdfium2 rasterize. Don't use fitz. If the export is unavailable, state the blocker. | lead |

## 7. Design artifacts (round 2)

| Path | Change |
|---|---|
| `design/PEER-REVIEW.md` | This review |
| `design/PROPOSAL.md` | Corrections block added at the top; inferred-history statements relabelled as suggestions; environment and renderer claims corrected |
| `design/tokens.json` | Code width 72/82 with the measurement noted; `contexts`, `routes`, `status_call`; terms and reveal limits |
| `design/check_tokens.py` | Now lints `blocks` contexts, prompt markers, per-size code width, `terms`/`route`/`reveal` kinds, lab phase sums, required lab fields, and agenda/elapsed agreement (`--agenda`) |
| `design/slide-manifest.json` | **New.** The 21 teaching slides mapped to templates. PASS against tokens and `teaching/agenda.json` |
| `design/example-slides.json` | Migrated to the block schema; four deliberate negative tests (long prompt, admin on slide, `$` marker, over-width line) fail as intended |
| `design/template-mockups-r2.svg` | **New.** Route (slide 7), lab with phase and status strips (slide 14), reveal (slide 15). Rendered with Quick Look and inspected; status strip raised to 16 pt after review |

To run the checks from the repo root:

```bash
python3 -I Workshop-Team/design/check_tokens.py --slides Workshop-Team/design/slide-manifest.json --agenda Workshop-Team/teaching/agenda.json
python3 -I Workshop-Team/design/check_tokens.py --slides Workshop-Team/design/example-slides.json   # expected: 4 failures
```

## 8. Still open (for the lead)

1. Logo placement: every slide, or title and close only? This is a suggestion either way, since no source establishes a requirement.
2. Is the workbook printed, PDF, or both? This decides whether I deliver a print stylesheet.
3. Should the appendix slides be hidden in the PPTX or moved to a separate facilitator PDF?
4. Is the PowerPoint export (automation permission) authorized for round 3?

Pausing here for the lead's decisions.
