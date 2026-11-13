---
title: Git Setup Guide
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# Git Setup Guide

Companion to the “Check the runtimes” slide. Install only what is missing. Use district-approved software and obtain IT approval before changing a managed laptop; do not bypass device restrictions. Finish downloads before the workshop if possible.

## Check first

Open Terminal on macOS (Applications > Utilities), your Linux terminal on Linux, or Git Bash from Start on native Windows. If Git Bash is not installed, use PowerShell for this first check. If you chose Ubuntu in WSL, open Ubuntu instead. Run:

```bash
git --version
```

If it prints a version, Git is installed. On macOS, this check may open Apple's developer-tools installation dialog instead. Follow the macOS instructions below only with the required IT approval; if installation is blocked, ask IT rather than bypassing restrictions. Git installation is separate from GitHub sign-in; the later GitHub exercise is covered in [[Setup Guide]].

## macOS

1. Open Terminal (Applications > Utilities).
2. If Git is missing, run Apple's Command Line Tools installer:

```bash
xcode-select --install
```

3. Complete the on-screen installation. This can take several minutes.
4. Reopen Terminal and run `git --version`.

If your district already uses Homebrew, an alternative is `brew install git`. Choose one route, not both. If Command Line Tools reports it is already installed but Git is still missing, ask the facilitator rather than removing existing developer tools.

## Linux

Open your Linux terminal. Choose the commands matching your distribution.

### Ubuntu / Debian (including Ubuntu in WSL)

```bash
sudo apt update
sudo apt install git
```

### Fedora

```bash
sudo dnf install git
```

For other distributions, use the Git project's Linux installation page below. Review the package transaction before approving it. Run `git --version` when installation finishes.

## Windows

### Native Windows / Git Bash

1. Choose either PowerShell installation or the manual installer—not both. For PowerShell installation, open PowerShell and run:

```powershell
winget install --id Git.Git -e --source winget
```

2. For the PowerShell method, follow any prompts that appear, then continue to step 4. The installation may use defaults without displaying an interactive installer.
3. For the manual method instead, download and run the Git for Windows installer from the official Windows installation page below. If choosing PATH options, select “Git from the command line and also from 3rd-party software.” Then continue to step 4.
4. Close all existing terminal windows, then open **Git Bash** from Start.
5. Run `git --version` there. Use this Git Bash window for the workshop's Bash commands.

### WSL

If you have chosen WSL in [[Setup Guide]], install Git **inside your Ubuntu terminal** using the Ubuntu commands above. A Windows installation does not replace the Linux installation. Keep subsequent workshop commands in the same environment.

## Set your commit identity

Check existing values first:

```bash
git config --global user.name
git config --global user.email
```

For a personal workshop account, if missing or incorrect:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@yourdistrict.org"
```

These commands change your user-wide defaults. Preserve organization-managed values. Use your approved GitHub email or GitHub-provided private email address; commit metadata can become public if a repository is published. This does not authenticate you to GitHub.

## Ready check / recovery

- `git --version` prints a version in the actual workshop terminal.
- Your intended commit identity is configured.
- If Git is not found, reopen the terminal. On Windows, verify in Git Bash, not an old PowerShell session.
- Do not disable endpoint protection or grant an unknown script elevated access to fix installation. Ask the facilitator if blocked.

Next: [[Node.js Setup Guide]] and [[Python Setup Guide]], then return to the “Check the runtimes” slide.

## Official references

- macOS: https://git-scm.com/install/mac
- Linux: https://git-scm.com/install/linux
- Windows: https://git-scm.com/install/win
- Commit identity: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup

Verification note: instructions checked against vendor documentation; installers have not been exercised on all three operating systems for this handout.
