---
title: Guardrails Checklist
status: draft
audience: attendees
tags: [cite-talk-2026, guardrails, handout, checklist]
---

# Guardrails checklist

A one-page checklist to keep by your desk. It is the [[Guardrails]] section turned into things to tick off. The frame to remember: use AI coding like a fast junior analyst, capable and tireless and never trusted blind.

## Before you run anything that changes state

- [ ] Read the command or script before you let it run, for anything that deletes, disables, writes, or sends.
- [ ] Run a destructive script in report-only mode first, against an export, before it touches anything live.
- [ ] Work in a scratch folder or a non-production copy, not the live system. Use a test tenant for anything that touches identity.
- [ ] Generate and review config changes first, then apply them in a maintenance window, not live from the chat.
- [ ] Use plain `claude` in Manual mode with approvals on in the workshop and for real work. Review existing allow rules. Do not use the bypass alias; a throwaway folder is not isolation.

## Protect the data

- [ ] No student records, credentials, API keys, or tokens in a prompt. If a script needs a secret, it reads it from the environment, not the chat.
- [ ] Strip personal data from a file before you hand it over, or use synthetic data.
- [ ] Confirm your Claude plan's terms cover the data you are about to use. FERPA, California SOPIPA, and your signed data privacy agreements apply.
- [ ] Never paste anything sensitive into a free or third-party model you have not vetted. Assume its prompts are logged.

## Keep permissions tight

- [ ] Leave permission prompts on for real work. Use `/permissions` to allow specific safe commands instead of turning everything off.
- [ ] Give an agent the narrowest tool set the job needs. Read-only where it can be.
- [ ] Review what a plugin does before you install it. It runs with your permissions in every session.

## Verify the output

- [ ] Check the work against something real: run the query on known data, test the script on a case where you know the answer.
- [ ] Spot-check citations, control mappings, and detection rules before you trust them.
- [ ] For anything going to leadership or an auditor, you own the claim, not the tool.

## Before you push to GitHub

- [ ] A `.gitignore` is in place and you have scanned for secrets.
- [ ] The repository visibility is what you intend, private or public.

## Watch for

- [ ] Prompt injection. Untrusted logs, vendor documents, and web pages can try to steer the tool. Read the result before you act on it.

---

Cite Talk 2026, AI for Cyber Security. Pulled from the [[Guardrails]] section. Print one-sided and keep it visible.
