---
title: Guardrails
section: 2
status: draft
tags: [cite-talk-2026, slides, guardrails, safety]
---

# Guardrails

Section 2 of [[Talk Outline]]. A deck. Each `##` heading is one slide; the **Slide** line is on-screen text, the rest is speaker notes.

This section sets the ground rules before any demo. It sits here on purpose, so the discipline frames every example that follows instead of arriving as an afterthought. The room is security staff, so pitch it as professional practice, not as a warning label.

The thread running through every slide: the human stays responsible. The tool is fast and confident and wrong often enough that you cannot hand it the keys and walk away. The later sections point back to these five rules.

## Slide 1. The rules before the demos

**Slide:** Five rules first. They are what make everything after this safe.

Speaker notes:
- Set expectations. You are about to see the tool do powerful things. Before that, the discipline that keeps a busy admin from turning power into an incident.
- The five guardrails, previewed: read before you run, work in a safe place, protect the data, keep your permissions tight, and verify the output. The rest of the section is one slide each, and the demos that follow lean on them.
- Say it plainly: none of these slow you down much. They are the difference between a tool that saves you a day and a tool that costs you a weekend.

## Slide 2. Read before you run

**Slide:** The model writes a confident command that deletes the wrong accounts. You are the last check.

Speaker notes:
- This is the habit the whole talk is built on. It runs through the code review and application build sections you will see. Here it gets stated as a rule up front.
- Claude will propose a command or a script that looks right and is wrong in a way you only catch by reading it: a wildcard that matches too much, a date filter off by a year, a destructive flag.
- The rule: for anything that changes state (deletes, disables, writes, sends), read what it will do before you let it run. For anything read-only, you can move faster.
- Tie it to permissions: check the active mode and allow rules, select Manual, and review proposed state-changing actions. The workshop uses plain `claude`, not a permission-bypass alias.

## Slide 3. Work in a safe place

**Slide:** Scratch folder, test tenant, non-production copy. Never rehearse on the live system.

Speaker notes:
- Give the tool a sandbox. A fresh folder for code, a copy of the data for analysis, a test tenant for anything that touches identity.
- Concrete cases for this room:
  - Account cleanup scripts: run them in report-only mode first, against an export, before they disable anything live.
  - Config changes: generate and review them, apply them in a maintenance window, not live from the chat.
  - A scratch folder is not isolation. Keep approval prompts on; the workshop does not use `--dangerously-skip-permissions`.
- The point is not fear. It is that the tool is fast, and fast plus a mistake on production is how you spend Saturday on restores.

## Slide 4. Protect the data

**Slide:** Do not paste student records, credentials, or anything under a data privacy agreement.

Speaker notes:
- This is the one with legal weight for K-12. FERPA, California SOPIPA, and your signed data privacy agreements govern where student data can go. A chat tool you have not vetted for that data is not a cleared destination.
- Practical rules:
  - Strip personal data before you hand a file to the tool. The demos later in [[Examples]] all work on scrubbed or synthetic data for this reason.
  - Never paste passwords, API keys, or tokens into a prompt. If a script needs a secret, it reads it from the environment, not from the chat.
  - Know what your plan sends where. Understand whether your Claude plan's terms cover the data you are about to use, and check your district's own agreement list before putting district data through any AI tool.
- Separate but related: do not commit secrets to the GitHub repos you will create in setup. A `.gitignore` and a quick scan before you push. The setup section has you push to GitHub, so flag this now and it lands when you get there.

## Slide 5. Keep your permissions tight

**Slide:** Give the tool the narrowest access the job needs. Widen it on purpose, never by default.

Speaker notes:
- Three levers, from the earlier sections:
  - The permission prompts. Keep them on in the workshop and for real work. Check the active mode and existing allow rules. `/permissions` supports narrow, deliberate exceptions.
  - Agent tool limits. Leaving Edit and Write out of the `log-triage` example does not enforce read-only access: Bash can still change or delete files. Keep approvals on, use a copy, and verify that the source stayed unchanged.
  - Plugins run as you. An enabled plugin's hooks and servers run with your permissions in every session. Review what a plugin does before installing it, the same way you read a script. This matters more for a large bundle, as you will see when we install ECC.
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
- Transition: with the rules set, the next section gets your machine set up so you can try it.

## Open questions for this section

- One-page attendee handout built: [[Guardrails Checklist]], a tick-off version of these five rules to keep by the desk.
- Confirm the FERPA and SOPIPA framing matches your district's actual data privacy agreement process. The slide states the obligation generally; you may want to name your specific vetting or DPA workflow.
- Placement decided: this sits at section 2, right after the intro, so the discipline frames every demo. Later references cover approval prompts, the log-triage agent, and optional plugin review; no bypass alias is part of the workshop.
- The prompt injection point is compressed into one line on slide 6. Decide whether this audience wants more on it, given OSINT and log triage both feed untrusted text to the tool.
