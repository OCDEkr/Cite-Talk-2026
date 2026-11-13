# Verification report

Structural and local reference checks: **PASS**. Coordinator-relayed final design/teaching findings resolved and covered by regression checks. Lead signs off the editable PPTX and packet within the limitations below.

- 21 visible timed core slides, four hidden zero-time support slides, exactly 120 computed minutes.
- Editable single-block text, real title placeholders, notes/full prompts, shape bounds, font floors, en-US language and image alt text checked in actual PPTX. Internal Help/Return links are authored; click behavior is not GUI-tested.
- Design density/contrast and agenda lint passed. Font-based fit checks passed; these are measurements, not visual review.
- Actual participant ZIP extracted into a fresh directory; reference triage/checker/report commands passed with expected rows. Wrong-header-only input rejected without output; existing output preserved; fixture hash unchanged.
- Teacher validator ran in a separate source staging copy using the extracted archive's lab modules: 25 local checks, ten CLI checks, 21 matching timed slides, four bounded support views, design lint PASS. Reference CLIs also ran directly from the extracted attendee kit. Detailed evidence is in `../integration/extracted-kit-verification.json` and local commands in `verification.json`.
- Regressions checked: complete C08 instructions; current R0 READY/status/permissions in C07 notes; explicit C14 checker and C18 workbook L3 run instruction/report checks; padded DONE/STUCK cards; semantic Help links clear of footer and inside the 912-point content edge; CHECK labels on reveals; SETUP provenance; correct per-slide link metrics. Participant ZIP excludes internal proposals/reviews/questions/corrections and design discussion.
- Linux preflight syntax passed; macOS runtime correctly returned SKIP/exit 2. No Linux success is claimed.
- Offline HTML handouts contain no scripts/remote assets; local links resolve inside this package. Print CSS is supplied; browser/print appearance is not visually tested.

**Native export: NOT RUN / awaiting user approval.** The PowerPoint approval request was canceled unanswered. It was not retried and no alternative route was used. No PDF export, slide raster, contact sheet or native visual sign-off is claimed. No separately drawn PDF is supplied.

Other NOT RUN: Linux/WSL VM and Python-floor rehearsal, native Windows, live model access/permissions, participant-generated code, browser rendering and classroom pacing. The 120-minute total is arithmetic, not a timed live rehearsal. Runtime references executed on macOS/Python 3.14.9.

Known scope limits: reference triage uses a fixed synthetic schema and arbitrary US/UTC rules; it does not detect compromise or impossible travel. The static report is an application exercise, not a network scanner. Generated participant code must be reviewed/tested separately. Final read-only specialist findings were relayed by the coordinator and resolved; no native visual sign-off is claimed.
