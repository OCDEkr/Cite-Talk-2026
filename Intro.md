---
title: Intro
section: 1
status: draft
tags: [cite-talk-2026, intro, slides]
---

# Intro

Opening section of [[Talk Outline]]. Each `##` heading below is one future slide. The **Slide** line is the on-screen text; everything else under the heading is speaker-note material.

Audience (confirmed 2026-10-29): K-12 district and county-office IT staff, in teams of one to five people who own networks, identity, devices, and security with no dedicated security engineer.

## Slide 1. Title

**Slide:** AI for Cyber Security: What AI-Assisted Coding Does for Small Teams

Speaker notes:
- Open by saying what the talk is about: one person doing security work that used to need three people.
- Promise two things. A plain definition of AI-assisted coding, and a case for why it changes the math for small teams in particular.

## Slide 2. Who this is for

**Slide:** You, if your "security team" is also the help desk, the network team, and the person who resets passwords.

Speaker notes:
- Ask for a show of hands: who has dedicated security staff? At a K-12 conference, expect few.
- Most people in the room already know what they should be doing. What they lack is hours. Audit log review, scripting, config checks, and reporting all lose to the ticket queue, and the gap between knowing and doing is what the rest of the talk is about.

## Slide 3. What AI-assisted coding is

**Slide:** A model that reads your code, your logs, and your question, then writes and runs code to answer it.

Speaker notes:
- The tools come in three levels, from least to most capable:
  1. Autocomplete. The tool finishes the line you started. GitHub Copilot in 2022 was this.
  2. Chat. You paste a script or an error, ask a question, and get an answer. You still do all the copying and running yourself.
  3. Agents. The tool has access to your files, your terminal, and sometimes your systems. You describe an outcome. It reads what it needs, writes code, runs it, reads the output, and fixes its own mistakes. Claude Code, Cursor, Codex, and Copilot's agent mode are this.
- This talk is about level 3. Levels 1 and 2 save minutes. Level 3 changes what one person can take on.
- Limits to state up front: it is not a security product, it knows nothing about your environment until you show it, and it makes confident mistakes. Whoever uses it still has to know enough to check the result. See [[Sources#Limits and risks]].

## Slide 4. What that looks like in security work

**Slide:** The work that never got done because nobody had time to write the script.

Speaker notes. No demo in this section; list all six on the slide and save any live work for the examples section:
- Log triage. Hand it a week of firewall or Entra sign-in exports and ask what looks wrong. It writes the parsing code, runs it, and shows you the outliers, so you review the outliers instead of the raw log.
- Config review. Point it at a switch config, a Group Policy export, or a Google Workspace admin dump and ask it to check against CIS benchmarks. It drafts the findings and you verify them.
- Glue scripts. The script that pulls stale accounts from AD, checks them against HR, and drafts the disable list used to be a two-day project that never got scheduled. Now it is an afternoon.
- Incident response prep. Build the playbook, the evidence-collection script, and the tabletop scenario in one session instead of one quarter.
- Reading vendor code. A vendor ships a PowerShell deployment script. Ask what it does before you run it as admin.
- Compliance paperwork. Turn a control spreadsheet into evidence requests and draft responses. Dull work, and it eats hours.
- All of these were always possible. What blocked them was the labor cost of writing and debugging code, and that cost has dropped by roughly an order of magnitude.

## Slide 5. Why this is a game changer for small teams

**Slide:** Large teams get faster. Small teams get capabilities they never had.

Speaker notes:
- A 40-person security operations center already has a scripter, a detection engineer, and an analyst. AI makes each of them somewhat faster, which is an incremental gain.
- A two-person district IT shop has none of those roles. The script never gets written, so the control never gets implemented. For that shop the change is not speed. Work that did not exist before now does, and that is a step change rather than a percentage improvement.
- What changes in practice: one generalist can now work across scripting, log analysis, and config review at a usable level, because the tool fills in syntax and library knowledge while the person supplies the judgment. The "someday" backlog of projects that needed a week of coding shrinks to projects that need a day, so the list of known but unaddressed risks gets shorter.
- There is also the other side of the equation. Adversaries use the same tools to write phishing kits and scan for exposures faster, and small targets are the ones who could never keep up. This is the first time the defender's costs have dropped too. See [[Sources#Attacker use of AI]].
- Set up the rest of the talk: the next section sets the guardrails, then the hands-on setup and the real examples, because the ways to hurt yourself with this are as real as the capability.

## Slide 6. The caveat before we go on

**Slide:** It will confidently write a script that deletes the wrong accounts. You still have to read it.

Speaker notes:
- Stating the risk early makes the rest of the talk easier to trust.
- Preview three rules: read before you run, test on a non-production copy, and never paste secrets or student data into a tool you have not vetted against your data agreements.
- Hand straight into [[Guardrails]], the next section, which turns this preview into the five rules the talk works by.

## Open questions for this section

- The attacker claim on Slide 5 is now sourced to Anthropic's September 2026 threat report. See [[Sources#Attacker use of AI]].
