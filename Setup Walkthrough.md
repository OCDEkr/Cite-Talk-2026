---
title: Setup Walkthrough
section: 2
status: draft
audience: presenter
tags: [cite-talk-2026, setup, slides]
---

# Setup walkthrough

Presenter notes for the hands-on setup. The attendee version is [[Setup Guide]]; the step numbers below match it. Each heading is one slide.

## Before the session

- Email the [[Setup Guide]] to registrants a week ahead and ask them to finish steps 1 through 4. Most of the room will not, but the ones who do will not be downloading Homebrew over conference wifi.
- Bring a phone hotspot. If the venue wifi dies, you can still demo.
- Have a second laptop with everything already installed, or a VM snapshot, so a broken step on your machine does not stall the room.
- Decide whether to hand out a shared Claude account for people without a paid plan. If you do, make it a Team seat you can revoke afterward, not your own login.

## Slide: What we are setting up and why

Say what the end state is: Claude Code running in a terminal, logged in, with a project pushed to GitHub, and VS Code open on it. Everything after this in the talk builds on that.

Explain the platform choice. Windows users get a Bash shell, either WSL or Git Bash, so everyone types the same commands. Recommend WSL to anyone who can reboot and has admin rights, and Git Bash to anyone who cannot. Plain PowerShell works too, but supporting a third command set live is not worth it.

## Slide: Steps 1 to 3, terminal and language runtimes

Walk through step 3 on your own machine only for the platform you use. Point Windows and Linux users at the handout for theirs.

Say explicitly that Claude Code does not need Python or Node. People will ask. The exercises need them because the scripts Claude writes for you will be in Python or JavaScript.

Checkpoint: ask for hands when `git --version`, `python3 --version`, and `node --version` all print something.

## Slide: Step 4, install Claude Code

Run the install command live. Call out that it shows no progress, because people will think it hung.

Run `claude doctor` and show the output. This is the command to tell people to run when they ask you for help later.

Checkpoint: hands up for `claude --version`.

## Slide: Step 5, log in

Start `claude` live and do the browser login. Mention the WSL case where the browser does not open and you paste a URL instead.

Checkpoint: `/status` shows the right account.

## Slide: Step 6, the alias

This is the step to spend a minute on, because the room is IT and security staff and the flag is called `--dangerously-skip-permissions`.

Show the default behavior first: run plain `claude`, ask it to create a file, and let the room see the approval prompt. Then explain that for the next hour you are turning that off so the exercises move, and that the alias name is `clauded` so nobody confuses it with the safe default.

State the rule plainly: `clauded` only in a scratch folder. Anything touching a real system uses `claude`.

Alternative to mention if someone objects: `/permissions` inside a session lets you allow specific commands without turning everything off. That is the right answer for real work. The alias is the right answer for a 60-minute workshop.

## Slide: Step 7, GitHub and SSH keys

Do `ssh-keygen` live. Show the blank passphrase and say why you are doing it (no prompts during the exercises) and why they should not do it on their work machine (a copied key file is a usable credential).

Show the paste into GitHub. Do `ssh -T git@github.com` and point at the "successfully authenticated" line, because the "does not provide shell access" line after it looks like an error.

Checkpoint: hands up for the authenticated message.

## Slide: Step 8, gh CLI

Short. Explain that this is what lets Claude create a repository for you. Without it, Claude can push to a repository you made, but cannot make one. Run `gh auth login` live.

## Slide: Step 9, VS Code

Fast. Show the Extensions view and the three names. Show the Claude Code panel opening inside VS Code. Mention that it bundles its own copy of Claude Code, so if anyone's terminal install is still broken they can do the rest of the workshop from here.

## Slide: Step 10, first project

The payoff. Do it live, with `clauded` in a fresh folder, and narrate what Claude is doing as it runs `git init`, writes CLAUDE.md, calls `gh repo create`, and pushes. Then open the GitHub page in the browser.

Pause on the moment Claude runs a command and say: this is the thing to watch. You gave it permission to run anything. Read what it ran.

Checkpoint: hands up for a repository visible on GitHub. This is the gate for the next section.

## Timing

| Step | Minutes | Notes |
| --- | --- | --- |
| Intro and platform choice | 3 | |
| 1 to 3, runtimes | 8 | Longest if nobody did prework |
| 4, install Claude Code | 4 | |
| 5, login | 4 | WSL browser issue costs time |
| 6, alias | 4 | Do not rush the warning |
| 7, SSH keys | 7 | Most hands-on help needed here |
| 8, gh CLI | 3 | |
| 9, VS Code | 4 | |
| 10, first project | 8 | |
| Buffer | 10 | |

About 55 minutes with buffer. If the session slot is shorter, cut step 8 and have people create the repository in the browser, and cut the VS Code slide to a mention.

## Suggestions not in the original list

These are additions beyond what was first planned. Keep or drop as you see fit.

- Git was missing from the install list. Nothing in steps 7 or 10 works without it, and macOS does not ship with it until Xcode tools are installed.
- `claude doctor` as the universal first troubleshooting step. It saves you from walking the room.
- The gh CLI. The original example prompt asked Claude to create and push a repository using only a public key path. Claude cannot create a GitHub repository with an SSH key alone; it needs gh or a browser. The handout prompt is rewritten around gh, with a fallback for people who skip it.
- The original prompt had a typo in the key filename (`is_ed236665.pub`). The default from `ssh-keygen -t ed25519` is `id_ed25519.pub`, which is what the handout uses.
- A troubleshooting section at the end of the handout, written from the failures most likely in a K-12 room: PATH, free accounts, VPN clients that block WSL.
- A prework email. Even a 20 percent prework rate cuts the runtime step in half.
- Git Bash as a second Windows path. Some district laptops cannot enable WSL without a ticket to the imaging team. Git Bash installs as a normal app and gives Claude Code the shell it wants.
- Consider whether to show `/permissions` instead of the alias for the real-work guidance later in the talk. The alias is fine for the workshop. Leaving a room of security staff with only the alias as the pattern they learned is a bad look.
