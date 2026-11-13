---
title: Setup Walkthrough
section: 3
status: draft
audience: presenter
tags: [cite-talk-2026, setup, slides]
---

# Setup walkthrough

Presenter notes for the hands-on setup. The attendee version is [[Setup Guide]]; the step numbers below match it and match steps 1 to 8 in the [[Cite Talk Guide]]. Slide numbers are positions in the current 45-slide deck. Setup runs from minute 15 to minute 40.

## Before the session

- The full application activity also requires nmap. Ask attendees to confirm `nmap --version` in their workshop terminal before class, using a district-approved installation route if it is absent. Repeat the check before the application block. Do not count a plan or observer-only fallback as a completed working application.

- Email [[Setup Guide]] and the three existing guides in Setup Guides a week ahead. Ask attendees to finish steps 1 through 4 and step 7: tool installs, Claude sign-in, and VS Code with its extensions. Do not ask them to create the workshop folder or repository ahead of time; that happens in the room. Attendees who already have a GitHub account can use it. In-room setup is 25 minutes of readiness checks, approval prompts, a GitHub account, and a local Git repository, not a full installation session.
- Bring a phone hotspot. If the venue wifi dies, you can still demo.
- Have a second laptop with everything already installed, or a VM snapshot, so a broken step on your machine does not stall the room.
- Confirm attendee access to the selected account route and the existing repository/files before class. Do not share personal logins. The existing free route is a backup that needs preflight, not a guaranteed equivalent.
- Confirm the venue network lets attendees reach github.com and receive GitHub's verification email.
- Recovery has a hard stop at minute 40. Use the documented VS Code extension route when the terminal install is broken. Anyone without a verified GitHub account continues with the local repository, which needs only Git. Anyone still blocked can review the same supplied report/config against presenter output; call that evidence review, not agent execution. Do not let one install hold the room.

## Slide: What we are setting up and why

Say what the end state is: Claude Code running in a terminal and signed in, VS Code installed, a GitHub account, and a local Git repository in `~/cite-workshop`. Everything after this in the talk builds on that folder. Pushing to GitHub is optional and comes later.

Explain the platform choice. Windows users get a Bash shell, either WSL or Git Bash, so everyone types the same commands. Recommend WSL to anyone who can reboot and has admin rights, and Git Bash to anyone who cannot. Plain PowerShell works too, but supporting a third command set live is not worth it.

## Slides 11 and 12: Steps 1 and 2, terminal and language runtimes

Check versions in the actual workshop terminal. Point anyone missing a tool to its existing platform-specific guide in Setup Guides; installation is prework.

Say explicitly that Claude Code does not need Python or Node. People will ask. The exercises need them because the scripts Claude writes for you will be in Python or JavaScript.

Exact existing files for slide 12: `Setup Guides/Git Setup Guide.md`, `Setup Guides/Node.js Setup Guide.md`, and `Setup Guides/Python Setup Guide.md`. Use these as the installation authority rather than maintaining another set of installer commands here. Native Windows/Git Bash checks `python --version`; WSL checks `python3 --version` inside Ubuntu. Reopen the terminal after installing.

Git identity is optional today. The workshop does not commit, so do not ask anyone to change their global Git settings in the room.

Checkpoint: ask for hands when `git --version`, `python --version` (or `python3` on Mac), and `node --version` all print something.

## Slide 13: Step 3, install Claude Code

Installation is prework. Show the installer only as a recovery reference; do not spend the readiness block waiting on a long download.

Run `claude doctor` and show the output. This is the command to tell people to run when they ask you for help later.

Checkpoint: hands up for `claude --version`.

## Slide 14: Step 4, log in

Start `claude` live and do the browser login. Mention the WSL case where the browser does not open and you paste a URL instead.

Checkpoint: `/status` shows the right account.

### Step 4b, a free option through OpenRouter (same slide)

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

## Slide 15: Step 5, approval prompts

Run plain `claude`, check the active permission mode, and select Manual (ask before edits and commands). Review existing allow rules in `/permissions`; already-permitted actions can still run without prompting. Do not assume a default mode.

Ask for a harmless file in `~/claude-scratch` and read the proposed change aloud before approving it. The workshop does not create or use a permission-bypass alias. A scratch folder is not isolation. Use `/permissions` only for narrow, deliberate exceptions.

## Slide 16: Step 6, GitHub account (in the room)

Anyone who already has an account signs in at github.com. Everyone else goes to github.com/signup and follows the prompts. GitHub asks them to verify their email, so they need an address they can open now and one their district allows.

Say it plainly: each person uses their own account. Nobody shares a password or verification code, and you do not create accounts for anyone.

If the verification email is slow or signup is blocked, the attendee keeps going. Step 8 needs Git, not a GitHub account; they finish the account after the session.

Checkpoint: hands up when you can sign in at github.com, or you have decided to continue local-only.

## Slide 17: Step 7, VS Code

Fast. Show the Extensions view and the three names. Show the Claude Code panel opening inside VS Code. Mention that it bundles its own copy of Claude Code, so if anyone's terminal install is still broken they can do the rest of the workshop from here.

## Slide 18: Step 8, local workshop repository

The payoff for setup. Everyone makes a new folder and a local Git repository in their workshop Bash terminal:

```bash
git --version
mkdir ~/cite-workshop
cd ~/cite-workshop
git init
git status
git rev-parse --show-toplevel
```

Narrate each line. `git init` creates the repository on the laptop. Nothing goes to GitHub, and there is no commit or push.

If `mkdir` says the folder exists, the attendee decides on purpose: reuse it only if it is their own workshop folder, or pick a new folder name. Running `git init` again in their own repository does not erase anything. The branch name may show as `main` or `master`; either is fine. On a machine with no Git settings, `git init` prints several `hint:` lines suggesting `git config --global init.defaultBranch`. Tell the room to ignore them; nobody changes Git settings in the workshop.

Then, as a separate and optional step, show `claude` and `/init` in the same folder. Say clearly that `/init` drafts a CLAUDE.md file for Claude and is not part of Git. Read the file-write approval aloud before accepting it.

Checkpoint: hands up when `git status` reports no commits yet and `git rev-parse --show-toplevel` prints a path ending in `cite-workshop`. This folder is where the app build happens later.

## Slide 19: Optional, SSH key

Optional and not a gate. Skip it when the room is behind and use the time for recovery on steps 6 and 8.

Before creating a key, check for an existing suitable one; never overwrite a private key. Protect new keys with a passphrase. Show only the public key and verify GitHub's host fingerprint before trusting a first connection.

Show the paste into GitHub. Do `ssh -T git@github.com` and point at the "successfully authenticated" line, because the "does not provide shell access" line after it looks like an error.

## Slide 20: Optional, gh CLI

Optional and not a gate. This workshop uses gh to create a remote repository; otherwise, use the browser-based fallback in the handout. Pushing needs a commit, and a commit needs the Git identity that is optional today, so this is for after the session. Show `gh auth login` only if time allows.

## Timing

| Slide | Step | Minutes | Clock |
| --- | --- | --- | --- |
| 11 | 1, terminal | 2 | 15–17 |
| 12 | 2, Git / Node.js / Python | 2 | 17–19 |
| 13 | 3, Claude Code | 2 | 19–21 |
| 14 | 4 / 4b, account route | 3 | 21–24 |
| 15 | 5, approvals | 2 | 24–26 |
| 16 | 6, GitHub account (in the room) | 4 | 26–30 |
| 17 | 7, VS Code | 2 | 30–32 |
| 18 | 8, local workshop repository | 5 | 32–37 |
| 19 | Optional, SSH key | 1.5 | 37–38.5 |
| 20 | Optional, gh CLI | 1.5 | 38.5–40 |

25 minutes total, minute 15 to minute 40. Installs and Claude sign-in are prework. The GitHub account and the local repository happen in the room. Slides 19 and 20 are optional; when the room is behind, skip them and spend those three minutes on recovery for steps 6 and 8. Do not extend setup past minute 40. These times are proposed and have not been rehearsed.

## Suggestions not in the original list

These are additions beyond what was first planned. Keep or drop as you see fit.

- Git was missing from the install list. Nothing in step 8 or the optional GitHub steps works without it, and macOS does not ship with it until Xcode tools are installed.
- `claude doctor` as the universal first troubleshooting step. It saves you from walking the room.
- The gh CLI. An SSH key authenticates Git transport; it is not the repository-creation step in this workshop. The optional handout workflow uses gh for creation, with a browser-based fallback. It comes after step 8.
- The original prompt had a typo in the key filename (`is_ed236665.pub`). The default from `ssh-keygen -t ed25519` is `id_ed25519.pub`, which is what the handout uses.
- A troubleshooting section at the end of the handout, written from the failures most likely in a K-12 room: PATH, free accounts, VPN clients that block WSL.
- A prework email. Ask attendees to complete installations and first login before the session; do not promise a particular completion rate or time saving.
- Git Bash as a second Windows path. Some district laptops cannot enable WSL without a ticket to the imaging team. Git Bash installs as a normal app and gives Claude Code the shell it wants.
- Use `/permissions` and Manual mode rather than a bypass alias. This applies to the workshop as well as real work.


Application workspace: Use ~/cite-workshop as the local Git workspace from setup step 8. For the application, create a fresh nmap-app subfolder inside it and open Claude there. This is a subfolder of the same local repository; do not initialize a second repository. If the folder already exists, stop and deliberately reuse it or choose another fresh name.
