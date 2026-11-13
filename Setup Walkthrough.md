---
title: Setup Walkthrough
section: 3
status: draft
audience: presenter
tags: [cite-talk-2026, setup, slides]
---

# Setup walkthrough

Presenter notes for the hands-on setup. The attendee version is [[Setup Guide]]; the step numbers below match it. Each heading is one slide.

## Before the session

- Email [[Setup Guide]] and the three existing guides in Setup Guides a week ahead. Ask attendees to finish steps 1 through 9, including first sign-in, GitHub authentication and editor setup. In-room setup is 25 minutes of readiness checks and bounded recovery, not a full installation session.
- Bring a phone hotspot. If the venue wifi dies, you can still demo.
- Have a second laptop with everything already installed, or a VM snapshot, so a broken step on your machine does not stall the room.
- Confirm attendee access to the selected account route and the existing repository/files before class. Do not share personal logins. The existing free route is a backup that needs preflight, not a guaranteed equivalent.
- Recovery has a hard stop at minute 41: use the documented VS Code extension or browser-created-repository route when applicable. Anyone still blocked can review the same supplied report/config against presenter output; call that evidence review, not agent execution. Do not let one install hold the room.

## Slide: What we are setting up and why

Say what the end state is: Claude Code running in a terminal, logged in, with a project pushed to GitHub, and VS Code open on it. Everything after this in the talk builds on that.

Explain the platform choice. Windows users get a Bash shell, either WSL or Git Bash, so everyone types the same commands. Recommend WSL to anyone who can reboot and has admin rights, and Git Bash to anyone who cannot. Plain PowerShell works too, but supporting a third command set live is not worth it.

## Slide: Steps 1 to 3, terminal and language runtimes

Check versions in the actual workshop terminal. Point anyone missing a tool to its existing platform-specific guide in Setup Guides; installation is prework.

Say explicitly that Claude Code does not need Python or Node. People will ask. The exercises need them because the scripts Claude writes for you will be in Python or JavaScript.

Exact existing files for slide 10: `Setup Guides/Git Setup Guide.md`, `Setup Guides/Node.js Setup Guide.md`, and `Setup Guides/Python Setup Guide.md`. Use these as the installation authority rather than maintaining another set of installer commands here. Native Windows/Git Bash checks `python --version`; WSL checks `python3 --version` inside Ubuntu. Reopen the terminal after installing.

Checkpoint: ask for hands when `git --version`, `python --version` (or `python3` on Mac), and `node --version` all print something.

## Slide: Step 4, install Claude Code

Installation is prework. Show the installer only as a recovery reference; do not spend the readiness block waiting on a long download.

Run `claude doctor` and show the output. This is the command to tell people to run when they ask you for help later.

Checkpoint: hands up for `claude --version`.

## Slide: Step 5, log in

Start `claude` live and do the browser login. Mention the WSL case where the browser does not open and you paste a URL instead.

Checkpoint: `/status` shows the right account.

## Slide: Step 5b, a free option through OpenRouter

Offer this for anyone who does not have a paid Claude plan and wants to follow along without paying. It routes Claude Code to a free model hosted on OpenRouter instead of to Anthropic.

Be honest about two things before anyone sets it up.

First, the big one for this room: treat backup-route prompts as public and assume they may be logged or used for training. Do not enter student data, credentials, district information, or anything sensitive. Privacy terms depend on the selected provider, plan, settings and district agreement; a paid plan is not by itself a privacy guarantee. Preflight current terms and availability before class.

Second, the honest limitation. OpenRouter's own documentation says Claude Code is optimized for Anthropic models and may not work correctly with other providers. Expect the free model to be slower and to stumble on the agentic steps that the paid models handle cleanly. It is good enough to follow along and see the shape of the tool. It is not the experience the rest of the talk demonstrates.

Setup. First make a free OpenRouter account and an API key at openrouter.ai/keys. Then add this to `~/.zshrc` on macOS or `~/.bashrc` on Linux and Git Bash:

```bash
export OPENROUTER_API_KEY="paste-your-openrouter-key-here"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""   # must be empty, or Claude Code tries Anthropic instead
export ANTHROPIC_DEFAULT_OPUS_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
export ANTHROPIC_DEFAULT_SONNET_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
export CLAUDE_CODE_SUBAGENT_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
```

Reload the shell (`source ~/.zshrc` or `source ~/.bashrc`). If anyone logged into Anthropic earlier, have them run `/logout` inside Claude Code first to clear the cached login, then restart Claude Code.

Checkpoint: `/status` shows the OpenRouter base URL and the Nemotron model instead of an Anthropic account.

Presenter note: the model ID and the free status can change. Confirm `nvidia/nemotron-3-ultra-550b-a55b:free` is still listed at openrouter.ai before the talk, and have a backup free model ID ready in case it is retired or rate-limited on the day.

## Slide: Step 6, approval prompts

Run plain `claude`, check the active permission mode, and select Manual (ask before edits and commands). Review existing allow rules in `/permissions`; already-permitted actions can still run without prompting. Do not assume a default mode.

Ask for a harmless file in the workshop folder and read the proposed change aloud before approving it. The workshop does not create or use a permission-bypass alias. A scratch folder is not isolation. Use `/permissions` only for narrow, deliberate exceptions.

## Slide: Step 7, GitHub and SSH keys

Check authentication from prework. Before creating a key, check for an existing suitable one; never overwrite a private key. Protect new keys with a passphrase. Show only the public key and verify GitHub's host fingerprint before trusting a first connection.

Show the paste into GitHub. Do `ssh -T git@github.com` and point at the "successfully authenticated" line, because the "does not provide shell access" line after it looks like an error.

Checkpoint: hands up for the authenticated message.

## Slide: Step 8, gh CLI

Short. Explain that this is what lets Claude create a repository for you. Without it, Claude can push to a repository you made, but cannot make one. Run `gh auth login` live.

## Slide: Step 9, VS Code

Fast. Show the Extensions view and the three names. Show the Claude Code panel opening inside VS Code. Mention that it bundles its own copy of Claude Code, so if anyone's terminal install is still broken they can do the rest of the workshop from here.

## Slide: Step 10, first project

The payoff. Use plain `claude` in a fresh practice folder, or reuse the prework practice repository without overwriting anything. Narrate and review the proposed `git init`, CLAUDE.md, repository-creation and push actions before approving them. Then open the GitHub page in the browser.

Pause on the first approval request and say: this is the thing to watch. Read what it wants to run before you approve it. Never push private keys, credentials or real district data.

Checkpoint: hands up for a private practice repository visible on GitHub. This is not a gate for reading the supplied PDF/config locally. Reserve the last three minutes for recovery, then move to the security exercise at minute 41.

## Timing

| Slide | Readiness check | Minutes | Clock |
| --- | --- | --- | --- |
| 9 | 1–2, terminal | 2 | 16–18 |
| 10 | 3, Git / Node.js / Python | 2 | 18–20 |
| 11 | 4, Claude Code | 2 | 20–22 |
| 12 | 5 / 5b, account route | 3 | 22–25 |
| 13 | 6, approvals | 3 | 25–28 |
| 14 | 7, SSH | 3 | 28–31 |
| 15 | 8, gh | 2 | 31–33 |
| 16 | 9, VS Code | 2 | 33–35 |
| 17 | 10, practice project + recovery | 6 | 35–41 |

25 minutes total. The final six minutes include three for the project checkpoint and three for bounded recovery. Installs and first login are prework. If needed, skip gh and create the repository in the browser, and reduce VS Code to a mention. Do not extend setup past minute 41.

## Suggestions not in the original list

These are additions beyond what was first planned. Keep or drop as you see fit.

- Git was missing from the install list. Nothing in steps 7 or 10 works without it, and macOS does not ship with it until Xcode tools are installed.
- `claude doctor` as the universal first troubleshooting step. It saves you from walking the room.
- The gh CLI. The original example prompt asked Claude to create and push a repository using only a public key path. Claude cannot create a GitHub repository with an SSH key alone; it needs gh or a browser. The handout prompt is rewritten around gh, with a fallback for people who skip it.
- The original prompt had a typo in the key filename (`is_ed236665.pub`). The default from `ssh-keygen -t ed25519` is `id_ed25519.pub`, which is what the handout uses.
- A troubleshooting section at the end of the handout, written from the failures most likely in a K-12 room: PATH, free accounts, VPN clients that block WSL.
- A prework email. Ask attendees to complete installations and first login before the session; do not promise a particular completion rate or time saving.
- Git Bash as a second Windows path. Some district laptops cannot enable WSL without a ticket to the imaging team. Git Bash installs as a normal app and gives Claude Code the shell it wants.
- Use `/permissions` and Manual mode rather than a bypass alias. This applies to the workshop as well as real work.
