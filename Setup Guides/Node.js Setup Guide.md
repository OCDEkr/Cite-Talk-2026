---
title: Node.js Setup Guide
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# Node.js Setup Guide

Companion to the “Check the runtimes” slide. Use an approved **LTS (Long-Term Support)** release, not an Alpha/prerelease. Do not replace an organization-managed installation without approval. Install before the workshop if possible.

## Check first

Open Terminal on macOS (Applications > Utilities), your Linux terminal on Linux, or Git Bash from Start on native Windows. If you chose Ubuntu in WSL, open Ubuntu instead. In that workshop terminal, run:

```bash
node --version
npm --version
```

Both should print versions. If already installed, confirm the Node release is still supported on the official download page; do not install a second copy unnecessarily.

## macOS

1. Open the official Node.js download page listed below.
2. Choose LTS, macOS, and the installer (`.pkg`) for your Mac's architecture (Apple Silicon/ARM64 or Intel/x64).
3. Run the installer, review its prompts, and finish installation.
4. Reopen Terminal and run both version checks above.

Use your district's approved installation method if one is already established. Do not mix an existing version manager with another installer without checking which executable will be used.

## Linux

Open a Bash terminal: on desktop Linux, open your distribution's Terminal app; on Windows with WSL, open **Ubuntu** from the Start menu. For a standard Ubuntu/Debian or Fedora workstation, use the following nvm route. Ubuntu in WSL uses these steps too. This is not an Alpine Linux guide.

### 1. Install prerequisites

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install curl ca-certificates
```

Fedora:

```bash
sudo dnf install curl ca-certificates
```

### 2. Install nvm, then Node LTS

nvm is a third-party per-user version manager. Read its official README below and obtain approval before running its installer; the script changes your shell startup configuration. Do **not** run it with sudo. In Bash, download the versioned script into a new, empty temporary folder in your home directory so nothing existing is overwritten:

```bash
NVM_TMP="$(mktemp -d "$HOME/nvm-install.XXXXXX")"
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh -o "$NVM_TMP/install.sh"
less "$NVM_TMP/install.sh"
```

Press `q` to leave the viewer. Reading `install.sh` reviews only the bootstrapper. When it runs, it downloads the rest of nvm from GitHub, so this review is not a full integrity check of everything installed.

After reviewing and approving the script, run the following in the **same** terminal (it uses `$NVM_TMP` from above):

```bash
bash "$NVM_TMP/install.sh" && rm "$NVM_TMP/install.sh" && rmdir "$NVM_TMP"
export NVM_DIR="${NVM_DIR:-$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")}"
. "$NVM_DIR/nvm.sh"
nvm install --lts
nvm alias default 'lts/*'
```

The `NVM_DIR` line matches nvm's own installer: it keeps an existing `NVM_DIR`, otherwise uses `$XDG_CONFIG_HOME/nvm` if that is set, otherwise `~/.nvm`. If the install fails, the temporary folder is left in place for troubleshooting; its path is in `$NVM_TMP`.

Reopen the terminal and run `node --version` and `npm --version`. If `nvm` is not found, check the shell-profile instructions in nvm's README. Do not solve it with `sudo npm` or a system-wide PATH change.

## Windows

### Native Windows / Git Bash

1. Use the official download page below. Choose LTS, Windows, the correct architecture, and **Windows Installer (`.msi`)**.
2. Run it and keep the Node.js runtime, npm, and PATH options enabled. Additional native build tools are not needed for these version checks.
3. Close existing PowerShell, Git Bash, and integrated terminal windows. Reopen Git Bash.
4. Run `node --version` and `npm --version` there.

Do not use the Linux nvm installer in native PowerShell. For this workshop, use the Windows installer rather than adding another Windows version manager.

### WSL

Use the Linux steps **inside Ubuntu**, not PowerShell. Windows and WSL are separate runtime environments; use the Linux Node installation for WSL workshop work.

Inside Ubuntu, confirm that WSL is using the Linux copies:

```bash
command -v node npm
```

Both paths should be inside your Linux home folder, for example `/home/<you>/.nvm/...`. If either one starts with `/mnt/c/` or another `/mnt/` drive, WSL is picking up the Windows installation. Reopen the Ubuntu terminal so nvm loads, then check again before continuing.

## Ready check / recovery

- `node --version` and `npm --version` both work in the same workshop terminal.
- Run `node -p "process.execPath"` to see the selected executable if installations conflict.
- If a command is missing, reopen your terminal before reinstalling.
- If PowerShell blocks `npm.ps1`, use Git Bash for this workshop, or `npm.cmd --version` for a PowerShell check. Do not weaken execution policy globally.
- If your district blocks downloads or installation, stop and ask for an approved route.

Related: [[Git Setup Guide]], [[Python Setup Guide]], and [[Setup Guide]]. Return to the “Check the runtimes” slide after the checks.

## Official references

- Node.js downloads and release status: https://nodejs.org/en/download
- nvm installation and LTS commands: https://github.com/nvm-sh/nvm
- Windows environment guidance: https://learn.microsoft.com/windows/dev-environment/javascript/nodejs-on-windows

Verification note: instructions checked against vendor documentation; installers have not been exercised on all three operating systems for this handout.
