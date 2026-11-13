---
title: Application Builds
section: 5
status: draft
tags: [cite-talk-2026, demos, prompts, app-builds]
---

# Application builds

Workspace: Use ~/cite-workshop as the local Git workspace from setup step 8. For the application, create a fresh nmap-app subfolder inside it and open Claude there. This is a subfolder of the same local repository; do not initialize a second repository. If the folder already exists, stop and deliberately reuse it or choose another fresh name.

Section 5 of [[Talk Outline]]. This is where the talk moves from one-off tasks to building a working application. The earlier sections showed Claude writing a script and finishing. Here it plans, researches, asks questions, and builds something that runs.

The build runs in five phases, each with a checkpoint: plan, design, code, run and fix, verify. Claude moves to the next phase only after you approve the current one. The outcome is a functioning local app, checked against nmap itself.

## Demo 1. An nmap web front end

What this demo shows: Claude does not jump straight to code. Given a real project, it researches, plans, and asks you clarifying questions before building. The first prompt is written to trigger that behavior on purpose. The follow-up prompts make each later phase explicit.

Do not run this while preparing the file. Run it live in the workshop, in a fresh project folder, so the room watches the planning happen in real time. No runtime results or screenshots are recorded here; the room sees whatever the live session produces.

Pacing is about 30 minutes: plan 4, design 4, code 12, run and fix 6, verify 4. That is proposed classroom pacing, not rehearsed, and not a guarantee that every build finishes in 30 minutes.

Before you start:
- nmap is installed during prework. Python is too, if Claude picks a Python backend.
- Use the model you approved and preflighted for the session. Kevin's 2026-10-29 test found planning stronger on Opus 5.5 than on the default; confirm what your plan offers before the talk rather than assuming it. On the free OpenRouter route, expect it to be slower and to need more help.
- Plain `claude`, Manual approvals on, in a fresh folder. Read every command before you approve it.

### Phase 1. Plan (about 4 minutes)

Prompt to use live:

```
I would like to build a user friendly interface to nmap similar to zenmap but a web app. Do your own research while planning and ask me any clarifying questions.
```

What to point at when it runs:
- The research and planning step before any code. This is the contrast with the earlier one-shot script demos.
- The clarifying questions it asks back. Have answers ready for the likely ones (see below) so the demo keeps moving.

Likely clarifying questions, with suggested answers to keep momentum:
- Which scan types to expose (ping sweep, port scan, service and version detection, OS detection). Answer: start with the common three and leave OS detection off by default, since it needs elevated privileges.
- Tech stack. Answer: let Claude pick a simple one it can run locally, for example a Python backend and a plain web front end, unless the room has a preference.
- Whether to run real scans or mock them. Answer: real scans. In the workshop, scan 127.0.0.1 only. Later, a lab VM you own, or scanme.nmap.org, which is the project's own sanctioned test host.
- Authentication and multi-user. Answer: out of scope for the demo; single local user.

Checkpoint: approve the plan only when it matches those answers.

### Phase 2. Design (about 4 minutes)

```
Before you write any code, show me the design: the files you will create, how the backend calls nmap, and how the server is started. Requirements: bind to 127.0.0.1 only, one local user, no login, only ping sweep, port scan, and service and version detection, no OS detection, nothing that needs sudo or root. Call nmap with an argument list built from allowed options, never by building a shell command string from what the user types. Wait for my approval.
```

Checkpoint: the design states 127.0.0.1, the three scan types, no sudo, and an argument list for nmap. Send it back if it mentions 0.0.0.0, a shell command string, or sudo. The argument-list point is a review check on the code Claude proposes, part of verifying the output; it is not a separate lab.

### Phase 3. Code (about 12 minutes)

```
The design is approved. Write the code now. Ask me before you install any package, and tell me what each command you want to run does.
```

Checkpoint: read each approval. Installing a package is a state change, so approve it on purpose. Deny anything that asks for sudo.

### Phase 4. Run and fix (about 6 minutes)

```
Start the app on 127.0.0.1 and tell me the address to open. If it fails, show me the error and propose one fix at a time.
```

Checkpoint: the startup output shows 127.0.0.1, not 0.0.0.0, and the page opens in a browser.

### Phase 5. Verify (about 4 minutes)

- Run one scan of 127.0.0.1 from the app.
- In a second terminal, run the same kind of scan with nmap on its own, for example `nmap -sT 127.0.0.1` for an unprivileged port scan. The open ports should match.
- Type an invalid target such as `not-a-host` and confirm the app shows an error instead of running something else.

If it is not working when the time is up, say what works and what does not. Do not call it a working tool until its results match nmap.

Guardrails to say out loud before running:
- A tool that runs nmap for whoever opens the web page is a scanner you have exposed. Keep it on localhost. Never put an unauthenticated scan front end on a network.
- Only scan hosts you own or are authorized to scan. In the workshop, that is 127.0.0.1.
- This is the same read-before-you-run habit from the rest of the talk, applied to a thing you are building rather than a thing you downloaded.

## Open questions for this section

- Confirm the tech stack you want Claude to use, or leave it to Claude in the room.
- Decide whether more build demos follow this one in the section, and what they are. This note currently has the one you provided.
