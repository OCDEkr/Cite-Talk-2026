# Build approach — implemented after three peer reviews

Final status: actual editable deck and curated Markdown/HTML packet built; see `../deliverables/VERIFICATION.md`. All three peer reviews and coordinator-relayed narrow final findings were resolved in `../DECISIONS.md`. Native export is NOT RUN / awaiting user approval; do not execute dormant export helpers. Use `prepare_manifest.py`, `build_deck.py`, `package_workshop.py`, `verify_final.py` with the prepared interpreter to reproduce local outputs. The historical preparation checklist below records the approach; its former build/export permissions are superseded by current decisions.

No final deck build is authorized by this preparation. All paths below are within `Workshop-Team/` unless an existing asset or interpreter is read-only.

## Inputs and contract

`prepare_manifest.py` reads teaching's agenda, narrative and workbook without importing specialist code. It computes continuous elapsed times, asserts 120 minutes and extracts full prompts into the appropriate slide notes data. `slides.json` is the ordered slide-content list; `manifest.json` records preparation status and SHA-256 source snapshots. Regenerate after reviewed upstream changes and inspect the diff; source hashes identify drift, not approval. Source text remains in `source_screen` and `notes`; projector copy is separately shortened to design density limits.

The working core is 21 slides. It uses source-grounded policy drafting, deterministic local sign-in triage and a static local report application. No scanner is built. The readiness slide is eight minutes at elapsed 20–28, comprising three minutes of checks and five minutes of recovery/transition; switch unresolved setups by minute 25. Protect the 48–53 break and 115–120 Q&A. No extra agenda/divider slides should add time.

The manifest retains instructor notes, source mappings, full workbook prompts, workbook section references, lab stop times, done criteria and fallback steps. Checkpoint templates must preserve the actual evidence reveal as well as working/partial/blocked guidance. “Source mapping” entries from narrative are editorial references; assemble precise final citations from teaching's source report and Linux's command matrix rather than treating wikilink labels as verified claims.

## Final implementation after review gate

1. Read all three `PEER-REVIEW.md` files; resolve recommendations in `DECISIONS.md` and refresh the manifest. Presence alone does not satisfy the gate. Reconcile Linux's setup guide to eight-minute readiness and the primary-Claude core; leave Codex/Hermes instructions as optional references, not requirements.
2. Use `/Users/kevin/.hermes/environments/documents/gen-673c9dde9c6d4bbc80b99ddee6dc1bc5/venv/bin/python`. Do not install into it. Implement a new python-pptx builder here, without importing existing builders or writing to their output paths.
3. Load `design/tokens.json`; use 960×540 points / 16:9. Use Arial and Office Consolas, resolving and reporting actual font files before measurement. Use real title placeholders, one editable textbox per logical block, explicit font sizes and language. Add notes and image alt text. Keep source data visibly labeled synthetic. Prompts are prose; full copyable text belongs in workbook and notes.
4. Use black title and light content slides, navy lab panels, blue on light and gold on dark. Put the appropriate existing OCDE logo on title and close; content slides use text footers. Existing eight-section/logo-every-slide assertions are historical builder choices, not current acceptance requirements. Preserve topical progression through section labels without inserting lecture dividers.
5. Lint slides with design's checker before deck construction. Check title/notes completeness, bounds, font floors, declared reading order, contrast, editable text and lab fallback fields. Density checks cannot prove visual fit or accessibility.
6. Inspect and run safe teaching validation after source review, plus Linux syntax/macOS guard as applicable. Record executed commands and platform limits. Do not run installers, inference, network scans or archive content. A macOS PASS is not Linux/WSL installation evidence.
7. Save the editable PPTX under `deliverables/`. Export that actual file with installed Microsoft PowerPoint through an approved automation path. GUI/AppleScript execution may need sandbox/automation approval; request it only when export is concrete and needed. Do not overwrite original decks or change global settings.
8. Validate native PDF page count/text with pypdf, then rasterize the exported PDF with pypdfium2 and Pillow. Use no PyMuPDF dependency. Review every rendered page and make contact sheets; retain image paths and review findings. If export fails, report the actual failure and do not substitute an independently drawn PDF as a native render.
9. Package workbook, facilitator notes, setup/preflight, answer key, safe lab inputs/reference/check scripts, provenance and citations with working relative links. Keep the no-account packet complete and usable offline. Do not promise a public download URL or publication. Document versions, hashes, checks, visual findings and all NOT RUN items in final verification.

## Current evidence limits

Teacher reports successful fixture/boundary/report checks on macOS; Linux reports syntax success and expected macOS guard only. Lead has read those records but has not yet rerun their lab checks. No classroom timing rehearsal, Linux/WSL install, participant-generated execution, PowerPoint export or visual review of the new deck has occurred. This preparation only computes and lints content; it creates no slides or PDF.
