---
title: Teaching proposal — Round 1
status: proposal-awaiting-cross-review
owner: cite-teacher
---

# Teaching proposal — Round 1

**Round 2 update (2026-11-10):** lead’s current [[Workshop-Team/DECISIONS]] selects the local HTML report and approved-Claude prework lane. Scanner completion is not required; the historical scope question below is resolved. Audience remains a labeled working assumption, not a preparation blocker. See [[Workshop-Team/teaching/PEER-REVIEW]] for the peer exchange and implemented fixes. The original proposal below is retained as the Round 1 record; updated workbook, agenda and narrative take precedence over its readiness wording. Readiness is now capped at 20–25, with evidence/transition at 25–28. Four support views add zero core minutes.

Lead has final authority. This is a concrete teaching draft for cross-review, not a completed workshop or approval to build the final deck.

Teach one workflow three times: **describe the outcome → constrain access → inspect the result → check against evidence**. Participants turn a short policy into a checklist, write and verify a synthetic sign-in triage script, then turn its output into a local HTML report. The final exercise follows the planning/question/build pattern in [[Application Builds]] while reducing dependencies. A working network scanner is a separate scope decision for the lead.

## Audience and delivery assumptions

- [[Intro]] explicitly confirms K–12 district/county-office IT teams of one to five on 2026-10-29. TEAM-BRIEF calls the audience provisional; use this profile for the draft and ask lead to settle the discrepancy.
- Mixed terminal experience; pairs alternate driver and evidence reviewer. A solo attendee can use the same checks.
- Two hours includes transitions, an eight-minute readiness/recovery block, five-minute break, debriefs and five-minute Q&A. Installation is prework. No extra minutes are hidden before the start.
- Normal permission review, approved account if already available, disposable environment, synthetic fixtures only. A folder name does not confine shell access. No personal credentials shared between attendees.
- Printed/offline review packets meet the same reasoning outcomes when there is no account, runtime, internet, or terminal. Record execution separately; paper review is not a successful software run.

## Observable outcomes

| Outcome | Evidence at checkpoint | Minimum pass |
| --- | --- | --- |
| Scope an agent task | Lab brief and an approval/rejection explanation | Names input, allowed output, prohibited action and one check |
| Ground a procedure in evidence | Offboarding checklist | Four named systems; roles, verification, evidence; 24-hour deadline; missing retention decision acknowledged |
| Verify generated automation | Source rows plus output and check result | Exactly E06/E07/E10/E11 with correct reasons; boundary exclusions explained; no compromise claim |
| Plan and inspect a small app | Three acceptance checks and local report or annotated specimen | Four review events, three reason categories, no network calls or automatic remediation |
| Transfer safely to Monday | One-hour task card | Owner, approved input, expected result, test and stop condition |

## Proposed teaching scope

Keep the practical voice: the task that never got done, the ticket queue, a script you can reuse next week. Do not promise a productivity multiplier, mastery, or a finished production tool. Core scope is two substantial labs plus a short application extension; all three have independent answer material.

1. Policy to procedure, 16 minutes including briefing and checkpoint, then four-minute discussion. This gives a useful first win before code.
2. Log triage, four-minute briefing, 18-minute work period, seven-minute validation/debrief. Training rules are explicit; no impossible-travel inference from country strings.
3. Local report build, five-minute planning, 13-minute work, five-minute verification. Build from the already checked CSV; no dependencies, server, account creation or scanning. A text-only report remains an honest partial result if HTML fails.

Five minutes between labs 2 and 3 lets pairs write a reusable review instruction. Explain skills/agents/plugins at a conceptual level; do not install bundles or promise that removing Edit while allowing Bash creates read-only access.

## Source decisions for lead review

| Actual source read | Retain | Adapt or defer |
| --- | --- | --- |
| [[Intro]] | Small-team backlog; chat versus agent; human judgment | Drop order-of-magnitude and current threat-report claims without verification |
| [[Guardrails]]; [[Guardrails Checklist]] | Five habits, evidence checking, untrusted input | Remove bypass alias from teaching path; no GitHub push or legal advice exercise |
| [[Examples]] | Policy-to-procedure and blue-team triage; review-before-run | Explicit rules replace vague unusualness; other examples become take-home options |
| [[Application Builds]] | Plan, questions, smallest runnable slice, acceptance | Recommend local report over scanner for this slot; lead decides |
| [[Skills Agents Plugins]] | Reusable instructions, delegated job, package | No live installs; fix Bash/read-only misconception |
| [[Setup Guide]]; [[Setup Walkthrough]] | Prework, checkpoints, recovery | Eight-minute readiness gate replaces 55-minute setup; Linux SME owns setup instructions |
| [[Getting Started]]; [[Close]] | One task, one hour; pilot evidence; contact | No plan tiers/prices, free-provider promises, or unverified distribution link |
| `scripts/build_workshop.py` | Its explicit deterministic sign-in exercise and boundary checks | Script comments record a prior working-scanner request, not resolved here; source-data provenance claims in it are not independent evidence |
| `scripts/build_cite_deck.py`; `Cite Talk Guide.src.html` | Existing practical arc and editable-deck integration context | Read only; no build executed and no existing artifact overwritten |
| [[Sources]]; [[Resource Index]] | Starting pointers | Product recommendations and historical numbers are not silently revalidated |

No supplied scan PDF/Nessus/config, packet capture or skill archive is used in these fixtures. Their sensitivity/provenance has not been established here. Do not call those files synthetic based on an existing script comment.

## Artifacts and integration contract

- [[Workshop-Team/teaching/AGENDA]]: generated elapsed-time table; exactly 120 minutes.
- `agenda.json`: canonical slide durations; `validate_teaching.py` computes totals and checks narrative times.
- [[Workshop-Team/teaching/SLIDE-NARRATIVE]]: 21 core slides, concise screen text plus speaker notes, cues, checkpoints and fallbacks. These are proposed content, not final design.
- [[Workshop-Team/teaching/PARTICIPANT-WORKBOOK]]: copyable prompts/commands, worksheets, preflight and no-account route.
- [[Workshop-Team/teaching/ANSWER-KEY]]: facilitator answers, policy specimen, deliberately flawed log output, app review specimen and debrief criteria.
- `labs/`: purpose-created policy/log inputs, deterministic reference script, exact CSV checker and local report reference. `labs/PROVENANCE.md` describes lineage and limits.
- [[Workshop-Team/teaching/SOURCES-AND-VERIFICATION]]: source checks and actual local execution evidence; distinguishes source checking, execution and untested delivery paths.

Run local checks from the repository root with `python3 Workshop-Team/teaching/validate_teaching.py`. No third-party packages needed. Copy the teaching folder to a disposable lab environment before participant execution; run inside the copy as the workbook directs. All preparation writes stay within teaching/.

## Questions for cross-review

1. **Lead:** Does the working-scanner requirement recorded in `scripts/build_workshop.py` still govern? If yes, choose a tested minimal stack and reallocate time before integration. Do not label this local report as a scanner or count saved results as live execution.
2. **Lead/Linux:** Can prework be required, and will attendees have approved agent access? Proposed fallback remains valid with zero accounts; no shared login or provider workaround is required.
3. **Linux:** Reuse this E01–E12 schema/rule contract or propose a single replacement before fixtures diverge. Can Python standard-library-only execution be the minimum runtime? Which OS paths can you actually test?
4. **Design:** Can lab slides visibly carry duration, filename, outcome and fallback, with full prompts in the workbook? Keep answer reveals separate from work slides; avoid displaying dense scripts in the main deck.
5. **Lead/coordinator:** Confirm distribution URL, print/offline provision, assistant availability and audience profile. Until resolved, no invented QR destination or setup-success claim.

## Facilitation and recovery

At minute 28 everyone is either running or reviewing. At minute 75 stop generating and test. At minute 105 stop adding features and inspect. Protect the break, check periods and final Q&A. If a model stalls for two minutes, move to the specimen and explain the stalled step. During the readiness block, sort PATH/login/policy/runtime failures and switch routes; do not run installers live.

One instructor can run the review route from paper; circulating helpers improve live terminal support. Use spoken instructions and visible written checks, avoid color-only pass/fail signals, and allow verbal answers. Ask for evidence, then ask what uncertainty remains. Each pair reports one thing it corrected, not how much code it generated.

Pause after Round 1 for peer paths and cross-review. Final scope, deck build, distribution and sign-off remain with the lead.
