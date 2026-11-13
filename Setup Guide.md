---
title: Setup Guide
section: 3
status: draft
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# Setup guide

This is the handout for the hands-on portion of the talk. Work through it top to bottom. Each step ends with a check so you know it worked before moving on. The presenter's version with timing is in [[Setup Walkthrough]]. Steps 1 through 8 here match steps 1 through 8 in the [[Cite Talk Guide]].

Before the session, finish steps 1 through 4 and step 7: install the tools, sign in to your Claude account, and install VS Code. Do not create the workshop folder or repository ahead of time; you make it in the room. The workshop reserves 25 minutes for readiness checks, approval prompts (step 5), a GitHub account (step 6), and your local workshop repository (step 8). Install only missing tools; use the existing [[Setup Guides/Git Setup Guide]], [[Setup Guides/Node.js Setup Guide]], and [[Setup Guides/Python Setup Guide]] for platform-specific checks and recovery.

## What you need before you start

For the full application exercise, nmap must also be available before class. In the workshop terminal, check `nmap --version`. If it is missing, use your district-approved installation route before the session; do not add an unreviewed installer during the build. Repeat this check before the application activity.

- A laptop you have admin rights on. District-managed machines that block installers or terminal access will not work for the hands-on part.
- A paid Claude account (Pro, Max, Ultra, Team, or Enterprise). The free plan does not include Claude Code; the [[Cite Talk Guide]] shows a free way to try the tool through OpenRouter. Sign up at claude.ai if you need to.
- An email address you can open during the session. You create or sign in to a GitHub account in the room, and GitHub asks you to verify your email.
- About 45 minutes before the session for installs and sign-in, and a decent internet connection.

## 1. Open a terminal

Everything below happens in a terminal.

- macOS: open Terminal from Applications > Utilities, or press Cmd+Space and type "Terminal".
- Linux: Ctrl+Alt+T on most desktops.
- Windows: you have two choices, covered below. Either one gets you a Bash shell so the commands in this guide match what Mac and Linux users type. Claude Code also runs in plain PowerShell, but this guide does not cover that path.

### Windows only: pick WSL or Git Bash

Option A, WSL, gives you a full Ubuntu Linux inside Windows. It is the better choice if you expect to do more Linux-style work later, and it supports Claude Code's sandboxing. It needs admin rights and a reboot.

Option B, Git Bash, is a lighter install. It is a Bash shell that runs directly on Windows and comes with Git and ssh-keygen built in. Pick this if WSL is blocked on your machine, you cannot reboot, or you just want the smaller download. Claude Code uses Git Bash as its shell when it is present.

#### Option A: WSL

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

Reboot when asked. On first launch of the Ubuntu app, pick a username and password. From here on, "terminal" means that Ubuntu window, not PowerShell.

Check:

```bash
cat /etc/os-release | head -2
```

You should see an Ubuntu version.

#### Option B: Git Bash

Download Git for Windows from https://git-scm.com/downloads/win and run the installer, or from PowerShell:

```powershell
winget install Git.Git
```

Accept the installer defaults. The one worth checking is "Git from the command line and also from 3rd-party software", which puts Git on your PATH so VS Code and Claude Code can find it.

After it finishes, open "Git Bash" from the Start menu. From here on, "terminal" means that Git Bash window.

Check:

```bash
git --version
echo $HOME
```

The second line shows your Windows user folder in Unix form, something like `/c/Users/yourname`. That is where `~/.bashrc`, `~/.ssh`, and your `~/cite-workshop` folder will live.

Where Git Bash differs from WSL in the rest of this guide:

- Step 2: follow the native Windows sections of [[Setup Guides/Python Setup Guide]] and [[Setup Guides/Node.js Setup Guide]]. Git is already installed.
- Step 3: use the PowerShell install command for Claude Code, then run `claude` from Git Bash.
- Step 5: start plain `claude` and check Manual mode and existing allow rules. No bypass alias is created.
- Step 7: the WSL extension is not needed. Set Git Bash as the VS Code terminal instead.

## 2. Install Git, Python, and Node

Claude Code itself does not need Python or Node. The hands-on exercises do, because the scripts Claude writes for you will be in one or the other. Git is required for your local workshop repository in step 8.

### Follow the existing platform-specific guides

Use one current instruction set for each tool rather than mixing installers:

- [[Setup Guides/Git Setup Guide]]: check Git first, then use the matching operating-system installation and recovery steps.
- [[Setup Guides/Node.js Setup Guide]]: check Node first; review installer scripts before executing them.
- [[Setup Guides/Python Setup Guide]]: check Python in the actual workshop terminal, including a virtual-environment check where directed.

Run each command in the shell named by its guide. WSL is Linux inside Ubuntu; native Windows/Git Bash uses the Windows instructions. Reopen the terminal after installing. In Git Bash, use `python --version` where `python3` is unavailable. Complete installations before the workshop.

### Check

Open a new terminal window, then:

```bash
git --version
node --version
npm --version
python3 --version   # macOS, Linux, WSL; use python --version in native Windows/Git Bash
```

Each prints a version number. If one says "command not found", close the terminal, open a new one, and try again. Installers often change your PATH but the current window does not see it.

### Optional: tell Git who you are

The workshop does not make commits, so you can skip this today. You need it before your first commit, for example before the optional push after step 8. Check the current values first, and keep any values your organization manages:

```bash
git config --global user.name
git config --global user.email
```

If they are missing and you want to set them:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@yourdistrict.org"
```

These commands change your user-wide Git settings. Use the email you attach to your GitHub account in step 6. [[Setup Guides/Git Setup Guide]] has more detail.

## 3. Install Claude Code

macOS, Linux, and WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows with Git Bash: run the installer in PowerShell, then use `claude` from Git Bash afterward.

```powershell
irm https://claude.ai/install.ps1 | iex
```

The installer shows no progress bar. Wait for it to return to the prompt.

Check, in a new terminal window:

```bash
claude --version
claude doctor
```

The first prints a version. The second runs diagnostics and should report no errors. If `claude` is not found, the install directory is not on your PATH yet. Close and reopen the terminal. If it still fails, run:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # macOS
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # Linux and WSL
```

then open a new terminal.

## 4. Connect to your Claude subscription

Make a scratch folder and start Claude Code inside it:

```bash
mkdir -p ~/claude-scratch && cd ~/claude-scratch
claude
```

The first run opens a browser window to log in. Sign in with the account that has the paid plan. When the terminal shows the Claude prompt, type `/status` to confirm which account you are on, then `/exit` to leave.

If the browser does not open (common in WSL), the terminal prints a URL. Copy it into a browser on Windows, log in, and paste the code it gives you back into the terminal.

No paid plan? Step 4b of the [[Cite Talk Guide]] covers the free backup route through OpenRouter. Read its data warning before you use it.

## 5. Keep approval prompts on

Start plain `claude`, check the permission mode, and select Manual (ask before edits and commands). Do not assume the startup default. Review existing allow rules in `/permissions`; already-permitted actions may not ask again. Read each proposed state-changing action before approving it.

The workshop does not create or use the `clauded` shortcut or `--dangerously-skip-permissions`. A scratch folder is not an isolation boundary. Use `/permissions` only for narrow, deliberate exceptions, not blanket approval.

Check: in `~/claude-scratch`, ask for a harmless file. You should see and understand the edit or command approval before accepting it. If you do not see a prompt, inspect the active mode and allow rules.

## 6. Create a GitHub account

You do this in the room. If you already have a GitHub account, sign in at github.com and go to the check.

Otherwise, go to github.com/signup and follow the prompts. Use an email address your district allows and that you can open now; GitHub asks you to verify it. Each person uses their own account. Never share a password or verification code, and nobody creates an account for someone else.

Check: you can sign in at github.com.

If the verification email is slow or signup is blocked, keep going. Step 8 needs Git, not a GitHub account. Finish the account after the session.

## 7. Install VS Code and extensions

Download from https://code.visualstudio.com/download and install.

On Windows with WSL, also install the "WSL" extension so VS Code can open folders inside Ubuntu. Then from the Ubuntu terminal, `code .` opens the current folder in VS Code.

On Windows with Git Bash, make it the default terminal inside VS Code so the commands in this guide work there too: open the Command Palette (Ctrl+Shift+P), run "Terminal: Select Default Profile", and choose Git Bash.

Extensions to install (Cmd+Shift+X on Mac, Ctrl+Shift+X elsewhere, then search):

- Python, by Microsoft.
- Claude Code, by Anthropic. This adds a chat panel inside the editor. It bundles its own copy of Claude Code, so it works even if the terminal install in step 3 gave you trouble.
- WSL, by Microsoft (Windows with WSL only).

VS Code already understands JavaScript and Node without an extension.

Check: open VS Code, open the Extensions view, and confirm each extension you need shows "Installed".

## 8. Create your local workshop folder and Git repository

You do this in the room, in a new folder. Git tracks changes to the files in this folder on your laptop. Nothing goes to GitHub, and you do not need a GitHub account, a commit, or a push.

Run these in your workshop Bash terminal (macOS Terminal, Linux, WSL Ubuntu, or Git Bash):

```bash
git --version
mkdir ~/cite-workshop
cd ~/cite-workshop
git init
git status
git rev-parse --show-toplevel
```

Check: `git init` reports an initialized empty Git repository, `git status` says there are no commits yet, and `git rev-parse --show-toplevel` prints a path ending in `cite-workshop`. The branch name in `git status` may be `main` or `master`, depending on your Git version and settings. Either is fine. If Git prints hints about the default branch name, you can ignore them; you do not need to change any Git settings for the workshop.

If `mkdir` says the folder already exists, stop and decide on purpose. Reuse it only if it is your own workshop folder, or pick a different new folder name and use it in place of `cite-workshop`. Running `git init` again in a repository you already made does not erase anything.

If `git --version` fails, use [[Setup Guides/Git Setup Guide]], then come back to this step.

The rest of the workshop, including the app you build, uses this folder.

### Optional: let Claude write a CLAUDE.md

`/init` is a Claude Code command, not part of Git. It drafts a CLAUDE.md file that tells Claude about this project. It does not create a Git repository; `git init` already did that.

```bash
claude
```

At the Claude prompt, type `/init`. Read the file-write approval before you accept it.

To open the folder in VS Code, run `code .` from the folder, or use File > Open Folder.

## Optional after step 8: connect to GitHub

None of this is required for the workshop. Do it when you want to back up or share a project on GitHub. Pushing needs at least one commit, and a commit needs the Git identity from step 2.

### SSH key

First check for an existing appropriate SSH key. Reuse it if suitable; do not overwrite a private key. If you need a new key, the command below creates one. This is how your machine proves to GitHub that it is you.

```bash
ssh-keygen -t ed25519 -C "you@yourdistrict.org"
```

Use the default file location only if no key already exists there. If asked whether to overwrite an existing key, answer `n`; reuse the suitable key or follow GitHub's guide for a different filename. Protect new keys with a passphrase and use your approved SSH-agent/keychain workflow. Never print or share the private key.

Print the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the whole line, starting with `ssh-ed25519`. Then in GitHub: profile picture > Settings > SSH and GPG keys > New SSH key. Paste it, give it a name like "conference laptop", and save.

Check:

```bash
ssh -T git@github.com
```

The first time, compare the displayed host fingerprint with GitHub's published SSH key fingerprints. Type `yes` only if they match. Then it prints "Hi yourusername! You've successfully authenticated". That line is success; the rest of the message about no shell access is normal. See GitHub's documentation on checking existing SSH keys, key passphrases, and testing your SSH connection.

### GitHub command line tool

This lets Claude create repositories for you instead of you doing it by hand in the browser.

macOS:

```bash
brew install gh
```

Linux and WSL:

```bash
sudo apt install -y gh
```

Windows with Git Bash, from PowerShell:

```powershell
winget install GitHub.cli
```

Then log in:

```bash
gh auth login
```

Pick GitHub.com, SSH, the key you made, and "Login with a web browser". Follow the prompts.

Check:

```bash
gh auth status
```

### Push to a private GitHub repository

From your workshop folder, start Claude:

```bash
cd ~/cite-workshop
claude
```

Paste this, replacing the username:

```
Set up this folder as a git repository named "cite-workshop", create a private GitHub repository under the username YOUR_GITHUB_USERNAME, add it as the origin remote using SSH, and push. Use the gh command for anything that needs GitHub itself.
```

Confirm Manual mode and inspect existing allow rules. Read each proposed command before approving it. Reuse your workshop folder from step 8; do not overwrite an existing project. Never push private keys, credentials, or real district data.

If you skipped the GitHub command line tool, use this workshop's browser-based fallback. Create an empty private repository in the GitHub web interface first, then tell Claude the SSH URL it shows you (it starts with `git@github.com:`) and ask it to add that as the remote and push.

Check: open github.com/YOUR_GITHUB_USERNAME/cite-workshop in a browser. The files Claude committed should be there.

## Troubleshooting

- `claude: command not found` after install. Open a new terminal. If still missing, see the PATH fix in step 3.
- Login loops or "not authorized". You are signed into a free claude.ai account. Claude Code needs a paid plan.
- `mkdir: ... File exists` in step 8. The folder is already there. Reuse it only if it is your own workshop folder, or pick a new folder name.
- GitHub verification email does not arrive. Continue with step 8, which needs only Git, and finish the account later.
- `Permission denied (publickey)` from GitHub (optional SSH). The key is not on your GitHub account yet, or you generated it under a different name. Run `ls ~/.ssh` and check for `id_ed25519.pub`, then redo the paste in the optional SSH section.
- WSL cannot reach the network. Follow your district's approved network/VPN troubleshooting process; do not disable security controls to make the workshop work.
- `code .` does nothing in WSL. Install the WSL extension in VS Code on the Windows side, then restart the Ubuntu terminal.
- Git Bash says `python3: command not found`. The Windows installer names it `python`. Use that, or run `alias python3=python` and add the same line to `~/.bashrc`.
- Claude Code in Git Bash cannot find Git Bash. Add the path to `~/.claude/settings.json`: `{"env": {"CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"}}`.

Optional tools (herdr, Codex, Hermes Agent) are steps 9 to 11 in the [[Cite Talk Guide]]. None of them is needed for the workshop.


Application workspace: Use ~/cite-workshop as the local Git workspace from setup step 8. For the application, create a fresh nmap-app subfolder inside it and open Claude there. This is a subfolder of the same local repository; do not initialize a second repository. If the folder already exists, stop and deliberately reuse it or choose another fresh name.
