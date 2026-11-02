---
title: Guardrails
section: 6
status: draft
tags: [cite-talk-2026, slides, guardrails, safety]
---

# Guardrails

Section 6 of [[Talk Outline]]. A deck. Each `##` heading is one slide; the **Slide** line is on-screen text, the rest is speaker notes.

This section earns the rest of the talk. The earlier sections showed the power. This one is the part that keeps a one-person IT shop from turning that power into an incident. The room is security staff, so pitch it as professional practice, not as a warning label.

The thread running through every slide: the human stays responsible. The tool is fast and confident and wrong often enough that you cannot hand it the keys and walk away.

## Slide 1. Why this section exists

**Slide:** Everything so far was the upside. These are the five ways it bites.

Speaker notes:
- Name the shift. Up to here the talk sold the capability. If you stop there, you have handed a room of busy admins a loaded tool and no trigger discipline.
- The five guardrails, previewed: read before you run, work in a safe place, protect the data, keep your permissions tight, and verify the output. The rest of the section is one slide each.
- Say it plainly: none of these slow you down much. They are the difference between a tool that saves you a day and a tool that costs you a weekend.

## Slide 2. Read before you run

**Slide:** The model writes a confident command that deletes the wrong accounts. You are the last check.

Speaker notes:
- This is the habit the whole talk is built on. It appeared in the code review and application build sections. Here it gets stated as a rule.
- Claude will propose a command or a script that looks right and is wrong in a way you only catch by reading it: a wildcard that matches too much, a date filter off by a year, a destructive flag.
- The rule: for anything that changes state (deletes, disables, writes, sends), read what it will do before you let it run. For anything read-only, you can move faster.
- Tie it to permissions: the default Claude Code asks before each action for exactly this reason. The `clauded` alias from [[Setup Guide]] turns that off, which is why it is scoped to scratch folders only.

## Slide 3. Work in a safe place

**Slide:** Scratch folder, test tenant, non-production copy. Never rehearse on the live system.

Speaker notes:
- Give the tool a sandbox. A fresh folder for code, a copy of the data for analysis, a test tenant for anything that touches identity.
- Concrete cases for this room:
  - Account cleanup scripts: run them in report-only mode first, against an export, before they disable anything live.
  - Config changes: generate and review them, apply them in a maintenance window, not live from the chat.
  - Anything with `--dangerously-skip-permissions`: scratch folders with nothing you care about, as the setup section said.
- The point is not fear. It is that the tool is fast, and fast plus a mistake on production is how you spend Saturday on restores.

## Slide 4. Protect the data

**Slide:** Do not paste student records, credentials, or anything under a data privacy agreement.

Speaker notes:
- This is the one with legal weight for K-12. FERPA, California SOPIPA, and your signed data privacy agreements govern where student data can go. A chat tool you have not vetted for that data is not a cleared destination.
- Practical rules:
  - Strip personal data before you hand a file to the tool. The demos in [[Examples]] all work on scrubbed or synthetic data for this reason.
  - Never paste passwords, API keys, or tokens into a prompt. If a script needs a secret, it reads it from the environment, not from the chat.
  - Know what your plan sends where. Understand whether your Claude plan's terms cover the data you are about to use, and check your district's own agreement list before putting district data through any AI tool.
- Separate but related: do not commit secrets to the GitHub repos you just learned to create. A `.gitignore` and a quick scan before you push. The talk taught them to push; this closes that loop.

## Slide 5. Keep your permissions tight

**Slide:** Give the tool the narrowest access the job needs. Widen it on purpose, never by default.

Speaker notes:
- Three levers, from the earlier sections:
  - The permission prompts. Leave them on for real work. `/permissions` lets you allow specific safe commands without turning everything off, which is the grown-up version of the `clauded` alias.
  - Agent tool limits. The read-only `log-triage` agent in [[Skills Agents Plugins]] could not change a file even if it tried. Build narrow agents for narrow jobs.
  - Plugins run as you. An enabled plugin's hooks and servers run with your permissions in every session. Review what a plugin does before installing it, the same way you read a script. This matters more for a bundle like ECC that installs a lot.
- The principle is least privilege, which this room already applies to users and service accounts. Apply it to the AI tool too.

## Slide 6. Verify the output

**Slide:** It is confident whether it is right or wrong. Confidence is not evidence.

Speaker notes:
- The failure mode that catches experts: the output is fluent, well formatted, and plausible, so it reads as correct. Fluency is not accuracy.
- Where it bites in security work:
  - A detection rule that looks right and never fires, or fires on everything.
  - A compliance mapping that cites a control the framework does not contain.
  - A config finding that is a false positive stated as fact.
- The rule: check the work against something real. Run the query against known data. Spot-check the citations. Test the script on a case where you know the answer. For anything going to leadership or an auditor, you own the claim, not the tool.
- Prompt injection, briefly: when you point the tool at untrusted content (a log full of attacker-controlled strings, a vendor document, a web page), that content can try to steer it. One more reason the human reads the result before acting on it.

## Slide 7. The one-line version

**Slide:** Use it like a fast junior analyst: capable, tireless, and never trusted blind.

Speaker notes:
- Give the room a single frame to remember. A sharp junior who works at machine speed. You would not let a new hire disable accounts in production unsupervised on day one. Same here.
- Supervision here is cheap: read the state-changing commands, sandbox the risky work, protect the data, keep permissions narrow, and verify what matters. That is the whole section in one breath.
- Transition: the next section is how to get started for real, now that they know both the power and the discipline.

## Open questions for this section

- Decide whether this needs a one-page attendee handout like [[Setup Guide]], a "guardrails checklist" they can keep. It would be easy to pull from these slides.
- Confirm the FERPA and SOPIPA framing matches your district's actual data privacy agreement process. The slide states the obligation generally; you may want to name your specific vetting or DPA workflow.
- Decide placement. This reads well as section 6, after the builds. An argument exists for moving it earlier, right after the intro, so the discipline frames every demo. Your call.
- The prompt injection point is compressed into one line on slide 6. Decide whether this audience wants more on it, given OSINT and log triage both feed untrusted text to the tool.
