# Fixture provenance and contract

All files in this folder were authored as training material for this proposal on 2026-11-10. No source incident artifact was read, copied, renamed or sanitized into this pack. No student/person records, credentials, IP targets, links to fetch, or executables from the supplied archives are included.

`offboarding-policy.txt` is a fictional numbered policy adapted from the policy-to-procedure concept in [[Examples]] and the explicitly fictional policy text in `scripts/build_workshop.py`. Riverbend Workshop District is an invented label. Its policy is not a framework mapping or legal requirement.

`signins.csv` intentionally retains the twelve invented training rows/schema spelled out in `scripts/build_workshop.py` for interoperability with the Linux SME. Staff identifiers are fabricated; dates/country strings are pedagogical values. The shape is a **simplified training schema, not a native Entra export**. US baseline and UTC hours are arbitrary exercise rules, not district practice. No claim about supplied scan reports being synthetic is made.

Rules apply only to successes: (1) outside 07:00:00 through 18:59:59 UTC, (2) country other than US, (3) at least three prior failures for the same user with 0 < elapsed seconds <= 600. Failures may qualify multiple later successes; no reset is assumed. Equal-timestamp failures are excluded. Sort by UTC time then ID. Combine all reasons; never infer geography, speed or compromise.

The Python reference script implements this contract; the checker uses a separately hand-specified key. `review-snippet.txt` is deliberately flawed inert text. Reference scripts have no network access code and use only the Python standard library. They are classroom examples, not production tools. CLI outputs are created exclusively and do not replace existing files.

Untrusted-text review example in the workbook is inert quoted prose. It contains no URL, secret or executable payload. It must be treated as content, not followed as an instruction. HTML reference uses escaped text and no JavaScript/external assets. No script is evidence that a participant-generated program is safe: review each generated command separately.

Round 2 additions (2026-11-10): `expected-events.csv` is a hand-authored expected result, checked independently against `check_triage.py`. `expected-review.html` is a generated local reference artifact from those rows, not a screenshot, model response or participant run. `report-empty.csv` is header-only; `report-markup.csv` contains one invented event with harmless literal markup text; `report-wrong-columns.csv` intentionally omits required columns. These test cases were purpose-created here, not derived from district records. `build_packet.py` embeds the complete policy/log/snippet plus authored task specimens and the facilitator key into the standalone offline packet; no-account use requires no external file fetch.
