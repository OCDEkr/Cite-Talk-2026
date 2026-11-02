---
title: Getting Started
section: 7
status: draft
tags: [cite-talk-2026, slides, getting-started, adoption]
---

# Getting started

Section 7 of [[Talk Outline]]. A deck. Each `##` heading is one slide; the **Slide** line is on-screen text, the rest is speaker notes.

This is the "now go do it" section. The talk has shown the power and the discipline. This section turns a room that is impressed into a room that opens a terminal on Monday. Keep it practical and small. The failure mode here is someone leaving inspired and never starting because they tried to boil the ocean.

## Slide 1. What to do Monday

**Slide:** Pick one annoying, repetitive task. Spend one hour. That is the whole plan.

Speaker notes:
- The biggest barrier is not cost or skill. It is starting. Set the bar at one task and one hour.
- Preview the three decisions this section walks through: which plan to pay for, what to install, and which task to start with.
- Say the honest thing: the first hour is slower than doing the task by hand. The second time you run it, you win the hour back and every hour after.

## Slide 2. Pick a plan

**Slide:** A subscription for predictable cost, or pay-per-use for a team. There is a free way to try it first.

Speaker notes:
- Walk the options. Prices move, so verify the current numbers on Anthropic's pricing page before the talk. These are the shape, not a quote.

| Option | Rough cost | Who it fits |
| --- | --- | --- |
| Claude Pro | about $20 per month | One person, light to moderate use. Where most people start. |
| Claude Max | about $100 per month (and a higher tier around $200) | One person who lives in the tool all day. |
| Team or Enterprise | per seat | A district rolling it out to staff, with admin controls. |
| API or Console | pay per token | Automation and scripts, or metered team use. |
| OpenRouter free model | free | Trying it with no commitment. See the setup walkthrough. |

- Two things people get wrong:
  - Usage is not a monthly bucket. It is a rolling limit per few hours plus a weekly cap, and the Claude Code tool and the Claude chat app draw from the same quota. Heavy days hit the limit; it resets.
  - Pro is enough to start. Do not buy Max until you have hit the Pro limit and felt it.
- The free OpenRouter path exists so nobody in the room is blocked by cost today. Repeat the warning from the setup section: a free model logs your prompts and may train on them, so no student data, no credentials.

## Slide 3. What to install first

**Slide:** Just Claude Code. Add plugins later, one at a time, when a real need shows up.

Speaker notes:
- Resist the urge to install everything on day one. A stack of plugins you do not understand is harder to trust and slower to run.
- The order that works:
  - Week one: plain Claude Code, from the setup section. Nothing else.
  - When writing prose: add the humanizer plugin. When you repeat a task: write one skill.
  - Later, if you want a full workflow system: install something larger like ECC, after you understand what a plugin is and read what it does.
- This mirrors the guardrails section. Every plugin runs with your permissions, so add them deliberately, not in a bundle you grabbed because a talk mentioned it.

## Slide 4. Choose your first project

**Slide:** Low stakes, repetitive, and you already know what the right answer looks like.

Speaker notes:
- The first task should be safe to get wrong and easy to check. Three tests:
  - Low stakes: it reads data or works in a scratch folder, and it cannot break production.
  - Repetitive: you do it often enough that a reusable script pays off.
  - Checkable: you know what a correct result looks like, so you can catch a confident mistake.
- Good first tasks for this room:
  - Summarize a week of sign-in logs into the handful worth looking at.
  - Turn a policy into an offboarding checklist.
  - Read a vendor's privacy policy against your vetting form.
  - Draft the tabletop exercise you have been putting off.
- Bad first tasks: anything that disables accounts, changes production config, or touches student data. Save those for after you trust the tool and your own review habit.

## Slide 5. Build the habit

**Slide:** Write one skill for the task you repeat most. Measure the hour you saved. Do it again next month.

Speaker notes:
- The jump from "I tried it once" to "I use it" is turning a task into a skill, so Claude does it your way every time. It is a folder and a file, from the skills section.
- Track the time. Even a rough note of "this used to take a day, now an afternoon" is what gets you a second hour, and what you show leadership.
- Grow by one thing at a time. One skill, then one agent for a bigger job, then a plugin to share with a colleague. Not all at once.

## Slide 6. Bring it to your team

**Slide:** Run a small pilot, show the time saved, then write the rules before you scale.

Speaker notes:
- A one-person win is a story. A team adoption needs three things:
  - Evidence: the hours saved from your own first month.
  - Rules: a short internal guideline on what data may go in, which plan or account to use, and the read-before-you-run habit. Pull it from the guardrails section.
  - A plan choice: a Team or Enterprise account if more than a couple of people use it, for the admin controls and shared billing.
- Get ahead of the data question before someone from cabinet asks it. Know whether your plan's terms cover district data, and have the "no student data in prompts" rule written down.
- This is where the talk's discipline pays off. You are not asking leadership to trust a tool. You are showing them a controlled way you already use it.

## Slide 7. Keep learning

**Slide:** One task today. The resource list for when you want more.

Speaker notes:
- Close the section by pointing at [[Resource Index]] for repositories worth knowing, and the [[Cite Talk Guide]] handout that collects the whole talk in one page.
- Last line, said plainly: you do not need to understand all of it. You need to open a terminal and do one task. Everything else follows from that.

## Open questions for this section

- Confirm the pricing figures against Anthropic's current plan page near the talk date. The top tier was being restructured as of late 2026.
- Decide whether this section needs its own one-page handout, or whether the [[Cite Talk Guide]] and [[Setup Guide]] already cover the takeaway.
- Decide the order of sections 6 and 7. Getting started reads well right before the close. If you moved guardrails earlier, this stays last.
