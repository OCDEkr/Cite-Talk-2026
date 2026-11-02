---
title: Application Builds
section: 6
status: draft
tags: [cite-talk-2026, demos, prompts, app-builds]
---

# Application builds

Section 6 of [[Talk Outline]]. This is where the talk moves from one-off tasks to building a working application. The earlier sections showed Claude writing a script and finishing. Here it plans, researches, asks questions, and builds something that runs.

Demo prompts in this section are meant to be run live. Each is written to show a different part of the build workflow.

## Demo 1. An nmap web front end

What this demo shows: Claude does not jump straight to code. Given a real project, it researches, plans, and asks you clarifying questions before building. The prompt below is written to trigger that behavior on purpose.

Do not run this while preparing the file. Run it live on stage, in a fresh project folder, so the room watches the planning happen in real time.

Before you start, set the model to Opus 5.5. Tested 2026-10-29: the build is fast and the planning is stronger on Opus 5.5 than on the default. Switch with `/model opus` inside the session, or confirm the selection shows Opus 5.5 before you send the prompt.

Prompt to use live:

```
I would like to build a user friendly interface to nmap similar to zenmap but a web app. Do your own research while planning and ask me any clarifying questions.
```

What to point at when it runs:
- The research and planning step before any code. This is the contrast with the earlier one-shot script demos.
- The clarifying questions it asks back. Have answers ready for the likely ones (see below) so the demo keeps moving.
- That it is scaffolding a real project: a folder structure, a web front end, and a backend that calls nmap.

Likely clarifying questions, with suggested on-stage answers to keep momentum:
- Which scan types to expose (ping sweep, port scan, service and version detection, OS detection). Answer: start with the common three and leave OS detection off by default, since it needs elevated privileges.
- Tech stack. Answer: let Claude pick a simple one it can run locally, for example a Python backend and a plain web front end, unless the room has a preference.
- Whether to run real scans or mock them. Answer: real scans against a host you own or a lab target such as scanme.nmap.org, which is the project's own sanctioned test host.
- Authentication and multi-user. Answer: out of scope for the demo; single local user.

Guardrails to say out loud before running:
- A tool that runs nmap for whoever opens the web page is a scanner you have exposed. Keep it on localhost during the demo. Never put an unauthenticated scan front end on a network.
- Only scan hosts you own or are authorized to scan. Use scanme.nmap.org if you need a live target on stage.
- This is the same read-before-you-run habit from the rest of the talk, applied to a thing you are building rather than a thing you downloaded.

## Open questions for this section

- Decide how far to take the build live. Options: stop after the plan and questions (safe, shows the planning), or build until the interface loads and runs one scan against scanme.nmap.org (stronger, needs a tested environment and more time).
- Confirm the tech stack you want Claude to use, or leave it to Claude on stage.
- Decide whether more build demos follow this one in the section, and what they are. This note currently has the one you provided.
