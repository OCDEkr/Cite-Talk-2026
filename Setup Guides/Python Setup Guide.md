---
title: Python Setup Guide
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# Python Setup Guide

Companion to the “Check the runtimes” slide. Install an organization-approved, supported **Python 3** release. Keep an existing working supported installation unless the facilitator identifies a compatibility problem. Do not replace the operating system's Python or bypass district restrictions.

## Check first

macOS / Linux / Ubuntu in WSL:

```bash
python3 --version
```

Windows native (PowerShell or Git Bash):

```powershell
python --version
```

A successful check prints `Python 3.x.y` (the numbers vary). Confirm that release is supported using the official Python downloads page; a version string alone does not establish support. A Microsoft Store window opening is not a successful runtime check. On macOS, a developer-tools installation dialog is not proof that a supported Python runtime is installed. Follow the approved macOS instructions below, then repeat the checks. Ask IT if installation is blocked on a managed device.

## macOS

1. Open the Python project's macOS downloads page below.
2. Choose a supported stable Python 3 release and its macOS `.pkg` installer, not a prerelease or source archive.
3. Run the installer and finish its prompts.
4. On district-managed Macs, check with IT before running the certificate setup script. Once approved, open the installed `Python 3.x` folder in Applications and run `Install Certificates.command` to complete certificate setup. Do not disable certificate validation if it fails.
5. Reopen Terminal, then check:

```bash
python3 --version
python3 -m pip --version
python3 -c "print('Python is ready')"
```

Do not delete or overwrite Apple's developer-tool Python. If the wrong installation is selected, inspect `python3 -c "import sys; print(sys.executable)"` and ask for help before changing PATH.

## Linux

Use your distribution's packages; do not build over the system Python.

### Ubuntu / Debian (including Ubuntu in WSL)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Fedora

```bash
sudo dnf install python3 python3-pip
```

Then:

```bash
python3 --version
python3 -m pip --version
python3 -c "print('Python is ready')"
```

For other distributions, use their supported Python packages. Review the proposed package transaction before approval.

## Windows

### Native Windows / Git Bash

If you already have a working supported Python installation, skip installation and run the checks in step 3. Do not install the manager just for this workshop. These steps are for native Windows using PowerShell or Git Bash. If your workshop environment is Ubuntu in WSL, follow the Linux instructions inside Ubuntu instead.

1. Open the official Windows downloads page below and install the **Python install manager**. This is separate from downloading a runtime.
2. Open a new PowerShell window and install the default runtime:

```powershell
pymanager install default
```

3. Reopen PowerShell or Git Bash and check:

```powershell
python --version
python -m pip --version
python -c "print('Python is ready')"
```

Use `python`, not `python3`, for the native Windows checks on the “Check the runtimes” slide. If commands conflict with a legacy Python launcher or Microsoft Store aliases, consult the official troubleshooting section; do not remove organization-managed installations blindly.

### WSL

If your workshop environment is Ubuntu in WSL, follow the Linux instructions **inside Ubuntu** and use `python3`. Installing Python in Windows does not install it inside WSL.

## Optional: keep project packages isolated

The version check is enough for the “Check the runtimes” slide. When a later exercise needs packages, use a virtual environment inside its scratch project folder rather than installing into system Python.

macOS / Linux / WSL (Bash or zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Windows PowerShell, without changing script-execution policy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip --version
```

This last form uses the environment directly; activation is not required. Use only packages requested by an approved exercise. Do not use `sudo pip` or override an “externally managed environment” safeguard.

## Ready check / recovery

- The correct platform's version command prints Python 3.
- The one-line print test works in your workshop terminal.
- If a command is missing, reopen the terminal first.
- If pip or venv is missing on Linux, check that the corresponding distribution packages were installed.
- If an installer or certificate step fails on a managed device, ask your IT team; do not disable certificate validation.

Related: [[Git Setup Guide]], [[Node.js Setup Guide]], and [[Setup Guide]]. Return to the “Check the runtimes” slide after the checks.

## Official references

- macOS downloads: https://www.python.org/downloads/macos/
- macOS setup: https://docs.python.org/3/using/mac.html
- Windows downloads: https://www.python.org/downloads/windows/
- Windows manager and troubleshooting: https://docs.python.org/3/using/windows.html
- Ubuntu setup: https://ubuntu.com/developers/docs/howto/python-setup/
- Fedora setup: https://developer.fedoraproject.org/tech/languages/python/python-installation.html
- Virtual environments: https://docs.python.org/3/library/venv.html

Verification note: instructions checked against vendor documentation; installers have not been exercised on all three operating systems for this handout.
