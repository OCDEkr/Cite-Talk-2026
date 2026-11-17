---
title: GitHub CLI Setup Guide
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# GitHub CLI Setup Guide

Companion to step 2 of [[Setup Guide]]. The GitHub command-line tool, `gh`, is how Claude creates your remote GitHub repository and works with it afterward: pushing, opening pull requests, checking issues. Install it before the workshop. You sign it in to GitHub in the room, after you have a GitHub account (step 6). Use district-approved software and get IT approval before changing a managed laptop; do not bypass device restrictions.

`gh` is separate from Git. Git tracks files on your laptop. `gh` talks to github.com for you.

## Check first

Open the terminal you will use for the workshop: Terminal on macOS, your Linux terminal, Ubuntu if you chose WSL, or Git Bash on native Windows. Run:

```bash
gh --version
```

If it prints a version, `gh` is installed; skip to the ready check. If the version is 2.45 or 2.46 on Ubuntu or Debian, remove it with `sudo apt remove gh` and follow the Linux steps below. GitHub's maintainers say those community-packaged versions no longer work against GitHub's API.

## macOS

With Homebrew:

```bash
brew install gh
```

Without Homebrew, ask IT. GitHub also publishes a `.pkg` installer on its releases page, but it is unsigned, so macOS will warn about it and a managed Mac may block it. Do not override that warning without approval.

## Linux

### Ubuntu / Debian (including Ubuntu in WSL)

Do not use `sudo apt install gh` on its own. That pulls the Ubuntu or Debian community package, which GitHub says is broken in the versions most releases ship. Add GitHub's own package repository instead. This block is copied from GitHub's install page; read it before running it, since it adds a signing key and an apt source with `sudo`:

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

Later updates come through `sudo apt update && sudo apt install gh`. If apt reports a signature error, GitHub rotated its package signing key in September 2026; see https://github.com/cli/cli/issues/13118.

### Fedora

On Fedora 41 and later (DNF5):

```bash
sudo dnf install dnf5-plugins
sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh
```

On older releases (DNF4):

```bash
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh
```

Avoid the snap package. GitHub's maintainers recommend against installing `gh` as a snap.

## Windows

### Native Windows / Git Bash

In PowerShell:

```powershell
winget install --id GitHub.cli --source winget
```

The installer changes your PATH, so close every Git Bash and terminal window and open a new one. A new tab is not enough. Then run `gh --version` in Git Bash.

If winget is blocked, GitHub publishes an `.msi` installer on its releases page. Use it only with IT approval.

### WSL

If you chose WSL in [[Setup Guide]], install `gh` inside your Ubuntu terminal with the Ubuntu steps above. A Windows install of `gh` does not reach into WSL.

## Sign in (in the room, after step 6)

Wait until you have a GitHub account you can sign in to. Then:

```bash
gh auth login
```

Answer the prompts:

1. Where do you use GitHub: `GitHub.com`.
2. Preferred protocol for Git operations: `HTTPS`. This works without an SSH key. If you already set up an SSH key with GitHub, `SSH` is fine too; when `gh` offers to upload a key, pick your existing public key or skip. Do not let it overwrite a key.
3. Authenticate Git with your GitHub credentials: `Yes`. Git can then push to GitHub without asking for a password.
4. How to authenticate: `Login with a web browser`. `gh` prints a one-time code. Press Enter, sign in to GitHub in the browser, and enter the code.

In WSL the browser may not open. Copy the URL it prints into a Windows browser and enter the code there.

`gh` stores its token in your system's credential store. If none is available (common in WSL and Git Bash), it falls back to a plain-text file and `gh auth status` shows where. That file is a live GitHub credential: do not share it, copy it into a project, or commit it.

## Ready check / recovery

Before the workshop:

- `gh --version` prints a version in the actual workshop terminal.

In the room, after signing in:

```bash
gh auth status
```

It shows `Logged in to github.com` with your username.

- `gh: command not found`: open a new terminal window. On Windows, check in Git Bash, not an old PowerShell window.
- `gh` works in PowerShell but not WSL: install it inside Ubuntu too.
- Sign-in fails or loops: run `gh auth logout`, then `gh auth login` again. If GitHub is still verifying your email, finish that first; the local workshop repository in step 8 does not need `gh`.
- Do not paste a GitHub token into a chat, a prompt to Claude, or a shared screen.

Next: [[Node.js Setup Guide]] and [[Python Setup Guide]], then return to step 2 of [[Setup Guide]].

## Official references

- Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
- macOS: https://github.com/cli/cli/blob/trunk/docs/install_macos.md
- Windows: https://github.com/cli/cli/blob/trunk/docs/install_windows.md
- Sign-in: https://cli.github.com/manual/gh_auth_login

Verification note: instructions checked against GitHub's install documentation on 2026-11-17; installers have not been exercised on all three operating systems for this handout.
