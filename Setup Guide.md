---
title: Setup Guide
section: 2
status: draft
audience: attendees
tags: [cite-talk-2026, setup, handout]
---

# Setup guide

This is the handout for the hands-on portion of the talk. Work through it top to bottom. Each step ends with a check so you know it worked before moving on. The presenter's version with timing is in [[Setup Walkthrough]].

If you can do steps 1 through 4 before the session, do. Conference wifi is slow and the downloads are large.

## What you need before you start

- A laptop you have admin rights on. District-managed machines that block installers or terminal access will not work for the hands-on part.
- A paid Claude account (Pro, Max, Team, or Enterprise). The free plan does not include Claude Code. Sign up at claude.ai if you need to.
- About 45 minutes and a decent internet connection.

## 1. Open a terminal

Everything below happens in a terminal.

- macOS: open Terminal from Applications > Utilities, or press Cmd+Space and type "Terminal".
- Linux: Ctrl+Alt+T on most desktops.
- Windows: you have two choices, covered in step 2. Either one gets you a Bash shell so the commands in this guide match what Mac and Linux users type. Claude Code also runs in plain PowerShell, but this guide does not cover that path.

## 2. Windows only: pick WSL or Git Bash

Option A, WSL, gives you a full Ubuntu Linux inside Windows. It is the better choice if you expect to do more Linux-style work later, and it supports Claude Code's sandboxing. It needs admin rights and a reboot.

Option B, Git Bash, is a lighter install. It is a Bash shell that runs directly on Windows and comes with Git and ssh-keygen built in. Pick this if WSL is blocked on your machine, you cannot reboot, or you just want the smaller download. Claude Code uses Git Bash as its shell when it is present.

### Option A: WSL

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

### Option B: Git Bash

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

The second line shows your Windows user folder in Unix form, something like `/c/Users/yourname`. That is where `~/.bashrc` and `~/.ssh` will live.

Where Git Bash differs from WSL in the rest of this guide:

- Step 3: install Python and Node with winget, under the "Windows native" heading. Git is already installed.
- Step 4: use the PowerShell install command for Claude Code, then run `claude` from Git Bash.
- Step 6: the alias goes in `~/.bashrc`, the same as Linux. Git Bash creates the file if it is missing.
- Step 9: the WSL extension is not needed. Set Git Bash as the VS Code terminal instead.

## 3. Install Git, Python, and Node

Claude Code itself does not need Python or Node. The hands-on exercises do, because the scripts Claude writes for you will be in one or the other. Git is required for the GitHub steps.

### macOS

Install Homebrew if you do not have it (this also installs Git):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then:

```bash
brew install python node
```

### Linux and WSL (Ubuntu or Debian)

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv curl
```

The Node in Ubuntu's apt repository is old. Use nvm instead:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc
nvm install --lts
```

### Windows native (Git Bash users)

Run this in PowerShell, not in Git Bash. You already have Git from step 2.

```powershell
winget install Python.Python.3.12 OpenJS.NodeJS.LTS
```

Then close Git Bash and open it again so it sees the new PATH. In Git Bash, `python3` may not exist; use `python --version` instead.

### Check

Open a new terminal window, then:

```bash
git --version
python3 --version
node --version
```

Each prints a version number. If one says "command not found", close the terminal, open a new one, and try again. Installers often change your PATH but the current window does not see it.

### Tell Git who you are

```bash
git config --global user.name "Your Name"
git config --global user.email "you@yourdistrict.org"
```

Use the email you will attach to your GitHub account in step 7.

## 4. Install Claude Code

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

## 5. Connect to your Claude subscription

Make a scratch folder and start Claude Code inside it:

```bash
mkdir -p ~/claude-scratch && cd ~/claude-scratch
claude
```

The first run opens a browser window to log in. Sign in with the account that has the paid plan. When the terminal shows the Claude prompt, type `/status` to confirm which account you are on, then `/exit` to leave.

If the browser does not open (common in WSL), the terminal prints a URL. Copy it into a browser on Windows, log in, and paste the code it gives you back into the terminal.

## 6. Set up a shortcut for the hands-on work

By default Claude Code asks before every file edit and every command. That is the right default for your real work. For the exercises in this session we are going to turn that off, because stopping to approve every step would eat the whole hour.

Add this line to `~/.zshrc` on macOS or `~/.bashrc` on Linux, WSL, and Git Bash:

```bash
alias clauded="claude --dangerously-skip-permissions"
```

Then reload the shell:

```bash
source ~/.zshrc    # macOS
source ~/.bashrc   # Linux, WSL, and Git Bash
```

Read the flag name. It means what it says. With this on, Claude will run commands and change files without asking. Use `clauded` only in a scratch folder or a fresh project that contains nothing you care about. For anything connected to a real system, use plain `claude` and approve steps as they come.

If you would rather not have the alias at all, the exercises still work with plain `claude`. You will just press Enter more.

## 7. Create a GitHub account and an SSH key

If you do not have a GitHub account, create one at github.com/signup using the same email you gave Git in step 3.

Then make an SSH key. This is how your machine will prove to GitHub that it is you, without typing a password every time you push.

```bash
ssh-keygen -t ed25519 -C "you@yourdistrict.org"
```

Press Enter to accept the default file location. It will ask for a passphrase. For this session, press Enter twice to leave it blank so the exercises do not stop to prompt you. On your work machine afterward, set a passphrase and let your OS keychain remember it; a blank passphrase means anyone who copies the file can act as you on GitHub.

Print the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the whole line, starting with `ssh-ed25519`. Then in GitHub: profile picture > Settings > SSH and GPG keys > New SSH key. Paste it, give it a name like "conference laptop", and save.

Check:

```bash
ssh -T git@github.com
```

The first time it asks whether to trust GitHub's host key. Type `yes`. Then it prints "Hi yourusername! You've successfully authenticated". That line is success; the rest of the message about no shell access is normal.

## 8. Install the GitHub command line tool

This step is optional but it lets Claude create repositories for you instead of you doing it by hand in the browser.

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

Pick GitHub.com, SSH, the key you just made, and "Login with a web browser". Follow the prompts.

Check:

```bash
gh auth status
```

## 9. Install VS Code and extensions

Download from https://code.visualstudio.com/download and install.

On Windows with WSL, also install the "WSL" extension so VS Code can open folders inside Ubuntu. Then from the Ubuntu terminal, `code .` opens the current folder in VS Code.

On Windows with Git Bash, make it the default terminal inside VS Code so the commands in this guide work there too: open the Command Palette (Ctrl+Shift+P), run "Terminal: Select Default Profile", and choose Git Bash.

Extensions to install (Cmd+Shift+X on Mac, Ctrl+Shift+X elsewhere, then search):

- Python, by Microsoft.
- Claude Code, by Anthropic. This adds a chat panel inside the editor. It bundles its own copy of Claude Code, so it works even if the terminal install in step 4 gave you trouble.
- WSL, by Microsoft (Windows with WSL only).

VS Code already understands JavaScript and Node without an extension.

Check: open VS Code, open the Extensions view, and confirm all three show "Installed".

## 10. Connect a project to GitHub with Claude

Now put it together. Make a new folder, start Claude in it, and let Claude set up the repository.

```bash
mkdir -p ~/my-project && cd ~/my-project
clauded
```

At the Claude prompt, type:

```
/init
```

Wait for it to finish, then paste this, replacing the username:

```
Set up this folder as a git repository named "my-project", create a private GitHub repository under the username YOUR_GITHUB_USERNAME, add it as the origin remote using SSH, and push. Use the gh command for anything that needs GitHub itself.
```

Claude will show you each command as it runs it. Watch what it does. This is the habit to build: read what the tool is about to do, even when you have given it permission to do it.

If you skipped step 8, Claude cannot create the repository for you. Create an empty private repository in the GitHub web interface first, then tell Claude the SSH URL it shows you (it starts with `git@github.com:`) and ask it to add that as the remote and push.

Check: open github.com/YOUR_GITHUB_USERNAME/my-project in a browser. The files Claude created should be there.

## Troubleshooting

- `claude: command not found` after install. Open a new terminal. If still missing, see the PATH fix in step 4.
- Login loops or "not authorized". You are signed into a free claude.ai account. Claude Code needs a paid plan.
- `Permission denied (publickey)` from GitHub. The key is not on your GitHub account yet, or you generated it under a different name. Run `ls ~/.ssh` and check for `id_ed25519.pub`, then redo the paste in step 7.
- WSL cannot reach the network. On some district laptops the VPN client blocks WSL networking. Disconnect the VPN for the session.
- `code .` does nothing in WSL. Install the WSL extension in VS Code on the Windows side, then restart the Ubuntu terminal.
- Git Bash says `python3: command not found`. The Windows installer names it `python`. Use that, or run `alias python3=python` and add the same line to `~/.bashrc`.
- Claude Code in Git Bash cannot find Git Bash. Add the path to `~/.claude/settings.json`: `{"env": {"CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"}}`.
