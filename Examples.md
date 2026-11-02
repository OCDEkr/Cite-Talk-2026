---
title: Examples
section: 4
status: draft
tags: [cite-talk-2026, examples, demos, prompts]
---

# Examples

Section 4 of [[Talk Outline]]. Five areas, two or three examples each. Every example is sized to run in under five minutes on stage and ends with something the room can see: a document, a table, a script, or a finding.

Each example has a one-line pitch, what to have ready, the prompt, and what to point at when it finishes. Prompts assume the attendee is in a scratch folder with `clauded` running, per [[Setup Guide]] step 6.

Two rules apply to every example and should be stated once at the start of the section:

- Only point these tools at systems and data you own or are authorized to assess. For the red team examples that means your own district's assets, with your director's sign-off.
- Do not paste student records, credentials, or anything covered by a data privacy agreement into the tool. Every prompt below works on exports stripped of personal data or on synthetic data you generate first.

## GRC: policies, procedures, and vendor vetting

### Gap analysis of an existing policy

Pitch: most districts have an acceptable use policy that has not been touched since before Chromebooks. Claude reads it against a current framework and tells you what is missing.

Have ready: your AUP or any security policy as a PDF or text file in the folder.

Prompt:

```
Read the policy in aup.pdf. Compare it against the CIS Controls v8 Implementation Group 1 safeguards and the NIST CSF 2.0 Govern function. Produce a table with one row per safeguard or outcome, marked covered, partially covered, or missing, with the policy section that covers it where one exists. Then list the five biggest gaps in order of risk to a K-12 district and draft replacement language for each.
```

Point at: the table, then open one drafted section and show it is usable text, not a summary.

### Turn a policy into a procedure

Pitch: a policy says "accounts must be disabled on separation". Nobody has written down how. Claude turns the policy line into a checklist tied to your actual systems.

Have ready: nothing beyond the policy. Name your systems in the prompt.

Prompt:

```
Our policy says: "User accounts must be disabled within 24 hours of employee separation and student withdrawal." We use Entra ID, Google Workspace, Aeries SIS, and a Fortinet VPN. HR notifies IT by email. Write a step-by-step offboarding procedure that satisfies this policy, with a step for each system, who does it, how it is verified, and what evidence to keep for an audit. Format it as a checklist we can paste into a ticket template.
```

Point at: the evidence column. Auditors ask for it and nobody plans for it.

### Vendor vetting from a privacy policy

Pitch: a teacher wants a new app approved by Friday. Claude reads the vendor's terms and privacy policy and fills in your vetting form.

Have ready: the vendor's privacy policy and terms saved as text files, and your vetting questionnaire if you have one.

Prompt:

```
Read vendor-privacy.txt and vendor-terms.txt. Answer each question in vetting-form.md using only what the documents say, quoting the sentence that supports each answer. Where the documents are silent, write "not addressed" rather than guessing. Then flag anything that conflicts with California SOPIPA or the SDPC California Student Data Privacy Agreement, and list the questions we should send back to the vendor before approval.
```

Point at: a "not addressed" row. The value is in what the vendor did not say.

## Red team

These examples assess the district's own assets with authorization. Say that out loud before starting, and keep the scope to things you own. The goal on stage is to show how fast you can understand your own exposure, not to run an attack.

### Make sense of your own exposure report

Pitch: you already have a scan report from your firewall vendor, your cyber insurance carrier, or a free external rating service. It is 40 pages. Claude turns it into the three things to fix Monday.

Have ready: an exposure or vulnerability report you already received, as a PDF or CSV, with any identifiers you do not want on screen removed first.

Prompt:

```
Read scan-report.pdf. This is an external exposure report for assets our district owns. Summarize it for a non-technical cabinet: what is exposed, why it matters in plain language, and the business risk if ignored. Then produce a remediation table for my team, sorted by risk, with the specific fix, the system owner who would do it, and a rough effort estimate. Flag anything that looks like a false positive and say why.
```

Point at: the cabinet summary. Translating technical findings into board language is the task that eats an afternoon.

### Phishing-awareness content for a tabletop

Pitch: security awareness training that uses generic examples gets ignored. Claude writes scenarios that sound like your district so staff actually recognize them.

Have ready: nothing. Describe your context in the prompt. This produces training material, not a live phishing campaign.

Prompt:

```
Write three security-awareness training scenarios for school district staff, based on real tactics used against K-12 districts: a fake message about payroll direct deposit, a spoofed message about a shared document, and a vendor invoice change request. For each, write what the lure looks like, the three signs a staff member should notice, and what they should do instead. Keep it to one page per scenario, written for teachers, not IT. Do not include any real names or working links.
```

Point at: the "three signs" list. This is the part that drops into a staff newsletter unchanged.

### Tabletop exercise facilitation

Pitch: you are supposed to run an incident response tabletop and have never written one. Claude builds the whole exercise.

Have ready: nothing.

Prompt:

```
Build a 45-minute ransomware tabletop exercise for a small K-12 IT team. Give me a realistic scenario that unfolds in four stages, the injects to reveal at each stage, the discussion questions for each stage, and a facilitator guide with the decisions we should be prodding the group toward. End with an after-action template we fill in as a group. Assume we have Entra ID, Google Workspace, backups to Azure, and cyber insurance with a 1-hour notification clause.
```

Point at: the facilitator guide. It turns a blank page into a runnable meeting.

## Blue team

### Triage a log export

Pitch: a week of sign-in logs is too much to read. Claude writes the code to find the odd ones and shows you those.

Have ready: a sign-in or firewall log export as CSV. Entra ID sign-in logs export cleanly. Scrub usernames to initials first if you prefer.

Prompt:

```
I have an Entra ID sign-in log export in signins.csv. Write and run a script that flags anything worth a human look: successful logins from new or unusual countries, impossible travel between two logins, repeated failures followed by a success, and logins outside normal hours for that account. Show me a table of the flagged events with the reason each was flagged, sorted by how suspicious. Do not change the file.
```

Point at: an impossible-travel row, and the script it wrote. Say that the script is reusable next week.

### Draft a detection rule

Pitch: you read about a technique and want to detect it, but do not speak KQL. Describe it in English.

Have ready: nothing. Microsoft Sentinel or Defender users get KQL; name your tool.

Prompt:

```
Write a Microsoft Sentinel KQL query that detects a user adding themselves or a new account to a privileged Entra ID role, then signing in from a new device within the next hour. Explain each part of the query in a comment so I can tweak it, and tell me what legitimate activity might trigger it so I can tune out the noise.
```

Point at: the comments. The explanation is what lets a one-person team own the rule.

### Explain an alert you do not understand

Pitch: a Defender alert fired with a title full of jargon. Claude explains it and tells you what to do.

Have ready: the alert text or a screenshot pasted in.

Prompt:

```
Here is a Microsoft Defender alert: [paste the alert]. Explain in plain language what it means, how serious it is for a school district, what could have caused it both maliciously and benignly, and the exact steps to investigate it. If it is likely a false positive, tell me how to confirm that before I close it.
```

Point at: the benign-cause list. It stops a tired admin from escalating a printer.

## Code review

### Review a script before you run it as admin

Pitch: a vendor or a forum gave you a PowerShell script. You are about to run it with privileges. Claude reads it first.

Have ready: the script in the folder.

Prompt:

```
Read deploy.ps1. I am about to run this as a domain admin. Walk me through what it actually does, line by line at a high level. Flag anything that reaches out to the internet, changes permissions, touches the registry, deletes files, or hides its own activity. Tell me the three things most likely to cause damage if I run it as-is, and what I should verify before running it.
```

Point at: an internet-reachout flag, if the script has one. This is the habit the whole talk is built on: read before you run.

### Find the obvious bugs in your own automation

Pitch: the cleanup script you wrote at 2am works, mostly. Claude finds the case where it deletes the wrong thing.

Have ready: a script you actually use, in the folder.

Prompt:

```
Review cleanup-accounts.py. This runs weekly and disables stale accounts. Find bugs, especially anything that could disable an account it should not: off-by-one errors, bad date math, missing error handling, assumptions about input format. For each issue show the line, why it is wrong, and the fix. Do not rewrite the whole thing; show me the diffs.
```

Point at: a date-math or filter bug. The scary ones are quiet.

## OSINT

Keep these to public information about your own organization. The point is to see what an outsider can learn about your district.

### What your district leaks publicly

Pitch: attackers start with what is public. Claude gathers the same picture so you can see it first.

Have ready: your district name and domain. This uses public web sources only.

Prompt:

```
Using only public web sources, build a profile of what an outsider could easily learn about Example Unified School District that would help them target us: our email address format, names and titles of IT and finance staff who appear on the public site, technologies mentioned in job postings, and any documents indexed publicly that mention internal systems. Present it as a risk briefing with what to remove or lock down for each item. Do not attempt to access anything non-public.
```

Point at: the email-format line. Staff names plus a predictable email format is how targeted phishing starts.

### Check staff exposure in known breaches

Pitch: staff reuse passwords. Claude checks whether district addresses show up in public breach data and tells you what to do.

Have ready: a list of staff email addresses you are authorized to check, or just your own for the demo.

Prompt:

```
Check whether these district email addresses appear in known public data breaches using Have I Been Pwned. [paste addresses, or use your own on stage] For any that appear, tell me which breaches, what data was exposed, and the exact remediation steps to send that person: reset where, enable MFA where, and what to watch for. Format it as individual messages I can send to each affected person.
```

Point at: the ready-to-send message. It turns a scary list into an action each person can take.

## Presenter notes for this section

- Run two or three of these live, not all of them. Pick one from GRC, one from blue team, and the code review script read. Those three land hardest for this room.
- Have every input file staged in the demo folder before you start. The examples assume the file is already there.
- Say the two rules at the top once, then do not repeat them. The room is security staff. They will respect that you said it and move on.
- The strongest single moment is the blue team log triage. If you only demo one thing live, demo that.

## Open questions for this section

- Confirm which demos run live versus which are screenshots, the decision deferred from [[Intro]].
- The breach-check OSINT example needs a current note on Have I Been Pwned access. Its bulk lookups need an API key. For a single address on stage the website is fine. See [[Sources]].
- Decide whether to ship the input files (sample AUP, fake vendor policy, synthetic logs) as a downloadable pack so attendees can follow along.
