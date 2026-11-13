# Design proposal: CITE 2026 workshop deck (round 1)

Owner: cite-design (Claude). Status: proposal for cross-review. The lead (cite-lead) makes the final calls. This is not a final deck, and I have not changed any file outside `Workshop-Team/design/`.

> **Round 2 corrections (2026-11-10).** See `PEER-REVIEW.md` for detail.
> 1. **Environment:** the "no libraries" finding below was a probe of system Python only. The coordinator's prepared interpreter (`/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python`) imports python-pptx 1.0.2, Pillow 13.0.0, pypdf 6.21.4 and pypdfium2. I confirmed this by import. PyMuPDF (`fitz`) is **not** present there.
> 2. **Inferred history:** statements below about what Kevin chose or did earlier (the black dividers, logo on every slide, a previous PowerPoint PDF export) come from existing scripts or my own session notes, not from the team brief. Treat them as **suggestions to keep**, not fixed requirements. A PowerPoint PDF export has **not** been exercised in this team effort (coordinator notes).
> 3. **Code width:** measured Consolas advance is 11.0 pt/char at 20 pt. The slide limit is raised from 64 to 72 characters at 20 pt, with an 18 pt fallback up to 82. The `$` marker is replaced by a shell-context tab (see `PEER-REVIEW.md`).
> 4. **Checkpoint template:** split into a *reveal/check* slide (evidence list) and a *status call* strip on lab slides, to match the teaching narrative without adding slides.

## Artifacts

| Path | What it is | Checked |
|---|---|---|
| `Workshop-Team/design/PROPOSAL.md` | This document | n/a |
| `Workshop-Team/design/tokens.json` | Colors, type scale, grid, density limits as data | Parsed by the checker |
| `Workshop-Team/design/check_tokens.py` | Stdlib-only WCAG contrast check plus a density linter for slide content JSON | Ran: 14/14 required pairs pass; linter correctly fails the untrimmed prompt |
| `Workshop-Team/design/example-slides.json` | Six sample slides using source text from `Guardrails.md` and `Examples.md`, one deliberately over budget | Ran through the linter |
| `Workshop-Team/design/template-mockups.svg` | Divider, concept, demo, lab, checkpoint at 960×540 | Rendered with macOS Quick Look and visually inspected; no clipping |

Run the checks from the repo root:

```bash
python3 -I Workshop-Team/design/check_tokens.py --slides Workshop-Team/design/example-slides.json
```

## Assumptions (provisional)

- Audience: K–12 district IT and security staff, per the brief. Many will be sysadmins first and security staff second.
- Room: a projector in a hotel or conference room, with back rows roughly 8 to 10 screen-heights away. People will also be looking down at laptops during labs, so the slide has to be glanceable, not readable in full.
- Presenter machine: unknown. It could be Kevin's Mac or a venue Windows PC. Fonts are chosen to survive both (see Type).
- Output: an editable 16:9 PPTX first, with a PDF exported from that PPTX.

## What I inspected

- `Workshop-Team/TEAM-BRIEF.md`, `CLAUDE.md`, `Talk Outline.md`, plus the slide-relevant parts of `Intro.md`, `Guardrails.md`, `Examples.md`, `Close.md`, `Application Builds.md`, and `Setup Walkthrough.md`.
- `scripts/build_cite_deck.py`, the current high-contrast deck generator: 55 slides, the `Canvas` class, `render()`, `verify()`.
- `scripts/CITE-Slides/preview-1.png` and `preview-3.png`, contact sheets of the current deck, plus `deck-verification.json`.
- `scripts/build_workshop.py`, an earlier workshop build with the same palette. Its `attendee-kit` output is now explicitly asserted *absent* by `build_cite_deck.py verify()`, which may mean that output was abandoned (my inference, not established).
- `scripts/cheatsheet_lib.py`: the cheat sheets use charcoal with an orange accent `#E8590C`, a different system from the deck.
- `Files/Mark-Title-COLOR-ForLightBG.png` and `Files/Mark-Title-COLOR-ForDarkBG.png`. I decoded the pixels with a stdlib PNG reader and counted opaque colors.
- The `Cite Talk Guide.src.html` header. It uses the visual-explainer `kit.css` tokens and has no palette of its own to inherit.
- Installed fonts: `/System/Library/Fonts/Supplemental` and the Office-bundled `DFonts` in PowerPoint.app.

I did not open the pcap zip, the Skills zip, or the Nessus files; they weren't needed for design.

## Source-derived rationale

These findings come from the files above, and each one drives a decision below.

1. **The brand colors are measurable, so use them exactly.** The logo's dominant opaque colors are blue `#155191` (154,635 px) and gold `#E7B678` (41,434 px). The current script's `ACCENT='#155191'` already matches the logo. The gold is unused in the deck. It is the only warm color the brand gives us, and it is the right accent on dark surfaces (11.36:1 on black, 9.10:1 on navy).
2. **Gold fails on white (1.85:1) and blue fails on black (2.62:1).** Any system that "uses the brand colors everywhere" breaks one way or the other. Each color gets the surface where it works: blue on light, gold on dark.
3. **The dark-background logo exists but isn't used.** `branding()` puts a white rectangle behind the light-background logo on black slides. `Mark-Title-COLOR-ForDarkBG.png` has white wordmark text (93,509 white px) built for exactly this case. Use it, and drop the white patch.
4. **The current deck's chrome is too small for a room.** Section labels are 12 pt, the footer is 9 pt, and the practice-slide labels ("DO / CHECK / DISCUSS") are 13 pt. In the contact sheets the labels are unreadable even at thumbnail scale. The labels carry instructions (the "DO / CHECK" words), so they need to be at least 16 pt.
5. **Prompt slides are too dense to read on a projector.** Examples: the `deploy.ps1` code-review prompt at 69 words and 21 pt, and the OSINT and blue-team prompts (preview-3, slides 27–33). Nobody types a 69-word prompt from a projector. They copy it from the workbook. The slide's job is to show the shape of the ask and what to watch for.
6. **Each wrapped line is a separate text box.** `Canvas.text()` creates one `add_textbox` per line. That breaks editing (fixing a typo means reflowing by hand), reading order for screen readers, PowerPoint's accessibility checker, and copy/paste from the PPTX. It is the biggest structural problem I found.
7. **Slides have no title placeholders.** Every slide uses `slide_layouts[6]` (Blank), so the title is just a text box. PowerPoint's accessibility checker flags "missing slide title," and the outline and navigator views are empty.
8. **The PDF is drawn in parallel, not exported.** `render()` draws every shape twice, once into python-pptx and once into PyMuPDF. The PDF therefore proves the layout math, not what PowerPoint renders. `deck-verification.json` already admits this in `rendering_limit`. PowerPoint.app is installed on this Mac and is a candidate real renderer via AppleScript export. That export has not been exercised for this workshop and may need automation permission.
9. **Andale Mono is macOS-only.** On a venue Windows PC, PowerPoint substitutes it, and code blocks will reflow. Consolas ships with Office on both platforms (confirmed in `PowerPoint.app/Contents/Resources/DFonts/Consola.ttf`).
10. **Conventions in the existing build script, suggested to keep (not established requirements):** black title and section-divider slides with white content slides (asserted in `verify()`), the OCDE logo, and speaker notes on every slide. The eight-section order belongs to the lecture outline. The teaching proposal's 21-slide workshop arc replaces it for this deliverable, subject to the lead.
11. **The cheat sheets use a different (orange) system.** I don't think that matters: they are separate handouts. I'd leave them alone rather than rebrand them for this workshop. The question for the lead is below.

## Visual system

### Color (all pairs checked by `check_tokens.py`)

| Token | Hex | Where | Contrast |
|---|---|---|---|
| ink | `#111111` | All text on light | 18.88 on white, 17.08 on panel |
| ink_muted | `#454B53` | Secondary text on light | 8.81 on white |
| brand_blue | `#155191` | Eyebrows, numerals, rules, chips on light | 8.02 on white, 7.25 on panel |
| panel | `#EFF4FA` | Cards, done/stuck boxes | n/a (surface) |
| black | `#000000` | Title and divider backgrounds | n/a |
| stage | `#0B1E33` | Prompt and terminal panels, lab header band | white 16.83, gold 9.10 |
| brand_gold | `#E7B678` | On black/stage only: section number, eyebrow, `$` prompt marker, lab label | 11.36 / 9.10 |
| ok / partial / blocked | `#1E6B3A` / `#7A4A00` / `#B3261E` | Checkpoint states only, always paired with a glyph, a word, and a border style | 6.52 / 7.48 / 6.54 |
| rule | `#5A6270` | Meaningful borders | 6.15 |
| hairline | `#CCD2DA` | Decorative separators only (1.52, deliberately) | n/a |

All text pairs meet WCAG AAA (7:1) except the three state colors, which meet AA (4.5:1) and are never the only signal. Banned pairs are listed in `tokens.json` → `forbidden_pairs`.

Color carries one job per slide type: blue says "concept," the navy stage says "you type this / it typed this," and gold appears only on dark surfaces. No gradients, no photos, no stock "hacker" imagery, and no assistant persona (per the brief).

### Type

- **Sans: Arial.** It's already in use, it's on every Mac and Windows machine, and it's legible at distance. Aptos is nicer, but older Windows Office installs may lack it.
- **Mono: Consolas**, falling back to Menlo, then Courier New. Only for commands, file paths, and code. **Prompts are prose and stay in sans.** Mono slows reading of sentences, and a prompt is a sentence.

| Role | pt | Weight | Notes |
|---|---|---|---|
| display | 48 | bold | Title and divider title |
| title | 36 | bold | Max 2 lines and 60 characters (~43 chars/line at 864 pt width) |
| statement | 32 | bold | One-idea slides |
| body / card head | 24 | regular / bold | Bullets, lab steps |
| card body / caption | 20 | regular | **Floor for any audience-facing prose** |
| code | 20 (floor 18) | Consolas | 864 pt panel minus padding fits about 75 chars at 20 pt; the limit is set to 64 for margin |
| label (chips) | 16 | bold caps | DEMO, LAB n, CHECKPOINT, DONE WHEN, STUCK? |
| meta | 14 | regular | Eyebrow, clock, footer, page number. Never essential |

### Grid

- 960 × 540 pt canvas, the same units as the existing script, so the lead can reuse its coordinates.
- 48 pt side margins (864 pt content width), 12 columns, 24 pt gutter.
- Eyebrow baseline at 42. Title starts at 78. Body runs 186–470. Footer rule at 500, footer text at 510–530.
- **Logo:** title, dividers, and close only, at 220 pt wide in the bottom right, using the light or dark variant to match the surface. Content slides carry a text footer only, which frees 48 pt of vertical space. This changes `verify()`'s "logo on every slide" assertion, so it's a question for the lead/Kevin below.

### Icons

Keep the existing hand-drawn line icons in `Canvas.icon()`. They're editable geometry and visually quiet. Use at most one icon per card, as reinforcement only, never as the only label.

## Slide templates

All templates share the eyebrow (section · or chip), a clock on the right (elapsed time, e.g. `0:52`, which the facilitator uses to stay on pace), the title, and the footer. See `template-mockups.svg`.

### Divider (black)
Gold section number at 96 pt, a gold rule, a white 48 pt title, a one-line 24 pt subtitle, the elapsed block (`0:08 → 0:16`), and the dark-background logo. Nothing else.

### Concept
One idea per slide. Two variants:
- **Points:** up to 3 numbered points, each at most 12 words, 40 words total, at 24 pt with blue numerals.
- **Statement:** at most 25 words at 32 pt bold. Use for the guardrail one-liners ("Confidence is not evidence.").
- **Cards** (existing `cards` kind): at most 3 cards, 24 pt head and 20 pt body, at most 15 words per body.

### Demo (instructor drives)
- Blue `▶ DEMO` chip plus "Instructor drives · you watch · N min". The audience knows not to type.
- A navy stage panel with a gold `PROMPT` label and the **prompt excerpt at 24 pt sans, at most 35 words**, ending in `…`. A gold pointer line names where the full text is: "Full prompt: Workbook 3.4 · Examples.md".
- **Watch for:** at most 2 points (from the source's "Point at:" lines). This is where the guardrail lesson lands.
- The full prompt goes verbatim in speaker notes (the existing build already does this with `EXACT SOURCE PROMPT`) and in the workbook.
- Exception: a prompt that *is* the lesson (e.g. the one-line nmap/Zenmap prompt in `Application Builds.md`, 30 words) can be shown in full. The hard cap is 70 words at 20 pt, and the slide must say so in the JSON (`full_prompt: true`).

### Lab (attendees drive)
- A full-width navy header band: gold "LAB n · YOUR HANDS · N MIN" on the left, white "Stop at 0:34" on the right. The band shows it's a lab from across the room, before anyone reads a word.
- Title, then at most 4 numbered steps of at most 15 words each.
- An optional command panel: navy, Consolas 20 pt, a gold `$` marker, at most 10 lines of at most 64 characters. Commands must come from `linux/` after verification. My mockup command is a placeholder and is labelled as one.
- Two boxes side by side:
  - **✓ DONE WHEN**: green left bar, the expected result in at most 20 words. The checkpoint slide refers back to this.
  - **↪ STUCK?**: amber bar, the workbook section and fallback path.
- Footer carries the workbook reference.
- `check_tokens.py` fails a lab slide that lacks `minutes`, `done_when`, `fallback`, or `workbook_ref`.

### Checkpoint
- Black `■ CHECKPOINT` chip, a question title, and one line telling people how to respond (cards, hands, chat).
- Exactly three rows: **WORKING** (✓, solid green border), **PARTIAL** (~, dashed amber), **BLOCKED** (✕, dotted red). Each state differs by glyph, word, and border pattern as well as color, so it survives grayscale projectors and color-vision deficiency.
- Each row is at most 12 words and says what to do next, not just a status.
- Suggest printed green/amber/red cards with the same glyphs at each seat. Cheap, and much faster than reading the room. (Teacher's call.)

### Others (reuse existing kinds, restyled)
- **Title:** black, 48 pt, the dark logo.
- **Break:** statement layout, with the "back at 1:05" clock as the headline.
- **Close / Q&A:** statement, with the light logo. Contact details stay as in `Close.md`.
- **Agenda:** the existing `agenda` kind. Bump rows to 20 pt and add a lab/demo glyph per row so people see where the hands-on time falls.

## Treatment of example content

- **Prompts:** sans, in a navy stage panel, excerpted on screen and verbatim in notes and the workbook. Trim with `…` and never paraphrase inside quotation marks. The excerpt must be a word-for-word prefix or contiguous span of the source prompt.
- **Commands / paths:** Consolas, `$` marker in gold (not part of the copied text in the workbook), no syntax coloring. Placeholders look like `<your-folder>`, never real names.
- **File names** in running text (`deploy.ps1`, `scan-report.pdf`): Consolas inline, the same color as the text.
- **Data provenance chip**, top right of any slide showing input data: `FICTITIOUS` (e.g. `Files/scan-report.pdf`, whose own footer says fictitious), `SYNTHETIC` (purpose-made fixtures), or `REAL · SANITIZED`. The brief forbids labelling source incident data as synthetic. The ClickFix pcap must never get a SYNTHETIC chip. I'd keep it off slides entirely unless the lead decides otherwise.
- **Tool output screenshots** (if the teacher wants backup slides for failed live demos): crop to the relevant 10–15 lines, at least 18 pt equivalent after scaling, add a `RECORDED <date>` chip so nobody mistakes it for live output, and don't fabricate output. Only capture real runs.
- **Pricing:** none on slides (the brief says omit). The current deck's `plans` slide has prices, so that slide kind should go or be rewritten.

## Accessibility checklist for the PPTX

1. One text box per logical block, with paragraphs inside it, `word_wrap=True`, and autofit off. Keep the existing PIL-based overflow measurement as the fit check.
2. A real slide title on every slide: use a layout with a title placeholder (`slide_layouts[5]` "Title Only") and restyle it, or at minimum name the title shape so the checker and outline see it. The lead should verify which approach PowerPoint's checker accepts.
3. Reading order = z-order: add the title first, then body in visual order, then decoration last.
4. Alt text on the logo (`descr="Orange County Department of Education logo"`) and on every picture. Mark decorative rules and bars as decorative or leave them out of the tab order.
5. No meaning by color alone (the checkpoint and lab boxes already follow this).
6. Minimum 14 pt anywhere, 20 pt for audience-facing content (enforced in `verify()`, see below).
7. Set the presentation language to en-US.
8. Speaker notes stay on every slide (existing).
9. No animations or transitions that delay content. Nothing flashes.

## Build integration guidance (for the lead)

I suggest evolving `scripts/build_cite_deck.py`'s approach (or a copy in the lead's area). No new framework is needed.

1. **Load `Workshop-Team/design/tokens.json`** in place of the hard-coded `BG/FG/MUTED/ACCENT/PANEL` constants, so design changes are data changes.
2. **Rewrite `Canvas.text()` to emit one text box per block.** Keep the PIL wrap measurement to raise on overflow, then write all lines into one text frame (separate paragraphs for bullets). This is the main editability and accessibility fix.
3. **Add template kinds** `demo`, `lab`, `checkpoint`, following the mockup coordinates. Retire or rewrite `prompt` (full-prompt panel) and `practice` (13 pt labels).
4. **Logo by surface:** `ForDarkBG.png` on black, `ForLightBG.png` on white. Remove the white patch.
5. **Mono font** → `Consolas`. For the PIL measurement, load `/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/Consola.ttf` (present on this Mac) so measurement matches rendering.
6. **Lint content before rendering:** dump `SLIDES` to JSON and run `check_tokens.py --slides`. A failure stops the build.
7. **Extend `verify()`:** every run has at least 14 pt; body runs have at least 20 pt; every slide has a title; every picture has `descr`; no banned color pair on any text run; lab slides have done/stuck boxes.
8. **PDF from the real renderer.** Attempt a PPTX-to-PDF export through PowerPoint.app (AppleScript `save as PDF`). This is untested here and may need automation permission. If it fails, record the blocker; don't fall back silently. Rasterize the exported PDF with pypdfium2 (available) for the contact-sheet review. PyMuPDF is not in the prepared environment, so the legacy parallel-drawn PDF path won't run unchanged and shouldn't be revived.
9. **Environment (corrected in round 2):** use the coordinator's prepared interpreter (python-pptx 1.0.2, Pillow 13.0.0, pypdf 6.21.4, pypdfium2; no fitz). System Python lacks these. Do not pip install into the prepared environment.

I can review the integrated build's rendered pages in round 3 (contrast, density, legibility at 25% zoom as a back-row proxy).

## Conflicts with existing deck decisions (flagged, not overridden)

| Existing (`build_cite_deck.py`) | Proposed | Why |
|---|---|---|
| Logo on every slide except 1 (asserted) | Title, dividers, close only | Frees 48 pt; less noise. Kevin's call |
| Light logo plus a white patch on black | Dark-variant logo | The asset exists for this |
| Full prompts on slide (nmap prompt asserted verbatim) | Excerpts; full text in notes/workbook | Readability. The nmap prompt is short enough to stay full under my rule, so that assertion survives |
| Andale Mono | Consolas | Windows presenter machines |
| 9–13 pt chrome | 14 pt minimum, 16 pt labels | Room legibility |
| `plans` slide with prices | Removed or price-free | Brief: omit prices |

## Questions for peers

**cite-lead**
1. Is the logo on every slide a firm Kevin requirement, or can content slides go logo-free?
2. Will the final deck be built by modifying `build_cite_deck.py` or as a new script under `Workshop-Team/`? That decides where my template code (if wanted) should live. I can write a `design/templates.py` module the build imports, if useful.
3. Is a PowerPoint.app AppleScript export acceptable as "a real renderer" for the PDF deliverable? It needs Kevin's machine and an automation permission prompt.
4. Should the workshop deck stay visually separate from the orange cheat sheets, or should I propose a matching handout style for the workbook?

**cite-teacher**
1. How many labs and checkpoints are in the 120 minutes? I'd like a checkpoint after every lab. Is that compatible with your run-of-show?
2. Is the workbook printed, a PDF, or both? It decides whether "Workbook 3.4" references are section numbers or page numbers.
3. For live demos, do you want recorded-output backup slides? If yes, which demos?
4. Physical green/amber/red cards at seats: yes or no?

**cite-linux**
1. What's the longest verified command line we'll show? I've set 64 characters at 20 pt. If install commands (e.g. `curl … | bash` style) exceed that, I'd rather show a short alias on the slide and keep the full line in the workbook. Is that acceptable?
2. Which platform label do you want on lab slides: "WSL / Linux" only, with macOS in the appendix?
3. Should I show the prompt marker as `$` everywhere, or does any step need a root `#` (I'd prefer none, given normal permissions)?
