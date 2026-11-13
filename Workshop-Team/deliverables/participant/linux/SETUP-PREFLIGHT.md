---
title: Practical Linux and WSL2 setup and preflight
status: integrated-workshop-edition
date: 2026-11-10
---

# Practical setup and preflight

Pick a route before doing any installs. Complete preparatory steps several days before the workshop; in the room, use the readiness gate below. The lead-selected core is policy → tested sign-in script → static local HTML report, not a scanner. Teaching's canonical readiness block is **elapsed 20–28**, with unresolved setup routed to review at **25**. Commands here are instructions for an approved lab environment. They were **not executed as installations on the author's host**. Official sources and verification status: [command matrix](COMMAND-VERIFICATION.md); [Round 2 review](PEER-REVIEW.md).

## Choose a route

| Route | What you need | What you do in the workshop |
| --- | --- | --- |
| No account, no install | Printed workbook or locally downloaded files and a reader | Inspect synthetic input, repair authored specimens A/B/C, verify against answer key, revise the prompt |
| Local files and Python, no AI account | Prepared Linux/WSL2 and Python 3.11+ | Same review plus run a reviewed local script on the fixture |
| Live agent | Prepared environment, one installed agent, approved individual account/provider access, working network | Same objective with live generation, human review, and known-result checks |

The fallback requires no shared login, new API key, GitHub account, or purchase. Pairing is optional; the account holder operates their own session and keeps credentials private. A printed route remains usable if downloading is blocked.

The concrete no-account pack now exists in [teaching's workbook](../teaching/PARTICIPANT-WORKBOOK.md), [answer key with specimens A/B/C](../teaching/ANSWER-KEY.md), and [labs provenance](../teaching/labs/PROVENANCE.md). Include `labs/offboarding-policy.txt`, `labs/signins.csv`, and `labs/review-snippet.txt` with those documents. Specimens are authored teaching examples, **not captured agent responses**. Keep the E01–E12 fixture and its exact answer contract. Print inputs and specimens before the event. Final kit packaging/distribution remains lead-owned. Do not relabel incident captures or existing reports as synthetic.

### Python runtime contract

Use a maintained CPython **3.11 or newer** for the run route, with standard library only. This is a workshop support floor, not a claim that the examples' syntax cannot run on older Python. Prefer the prepared Ubuntu 24.04 Python 3.12 runtime for Linux rehearsal. Python 3.10 is now upstream end-of-life; [Python version status](https://devguide.python.org/versions/), retrieved 2026-11-10. No Python at all is needed for the paper route. No pip, venv, Node, server, scanner or agent account is needed to run the reviewed reference code.

## Prework A: Windows host preparation

Use an organization-approved Windows installation. Microsoft's simplified install procedure requires Windows 10 version 2004/build 19041+ or Windows 11; that technical minimum is not a recommendation to use an unsupported OS. See [Microsoft WSL install](https://learn.microsoft.com/en-us/windows/wsl/install), retrieved 2026-11-10.

**PowerShell on Windows, inspect first:**

**WINDOWS POWERSHELL · PREWORK ONLY**

```powershell
wsl --status
wsl --list --verbose
```

Expected: an installed Ubuntu distribution with **VERSION 2** in the list. `cat /etc/os-release` alone cannot distinguish WSL1 from WSL2.

If WSL is absent, have the device administrator approve and complete this **before class**, with virtualization available under device policy:

**WINDOWS POWERSHELL · PREWORK ONLY**

```powershell
# Administrator PowerShell — changes the Windows host; prework only
wsl --install -d Ubuntu-24.04
```

Restart when requested, launch the distribution, and create its Linux user/password. If that distribution name is unavailable, inspect `wsl --list --online` and agree a tested image with the organizer. Existing WSL installations may need administrator-managed updates/conversion. Do not reinstall or unregister an existing distribution to troubleshoot.

If installation, virtualization, Store access, or a reboot is blocked, choose the no-install route. Git Bash is a native Windows shell environment; it does not provide Ubuntu's package manager or the Linux sandbox.

## Prework B: Linux environment

Workshop target: a disposable Ubuntu 24.04 LTS VM or WSL2 distribution. Use a normal Linux user, not root. Keep exercises under the Linux home directory, for example `~/cite-workshop`, rather than `/mnt/c` or an Obsidian/district file tree. Microsoft recommends matching file storage to the OS toolchain: [WSL file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems), retrieved 2026-11-10.

A full disposable VM offers a stronger separation option when it has no shared host directories, production credentials, or unnecessary network exposure. WSL interoperability and mounted Windows drives mean a new Linux folder is not equivalent to an isolated VM.

**Ubuntu/WSL terminal, inspection only:**

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
uname -s
uname -m
cat /etc/os-release
id -u
command -v bash
python3 --version
```

Expected: Linux, the prepared CPU architecture, intended distribution, nonzero user ID, Bash; Python 3.11+ is required only for the executable script/report lane. Inspect locally; do not post full machine diagnostics into chat.

**Only if packages are missing, approved prework by an administrator:**

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
sudo apt update
sudo apt install ca-certificates curl python3
```

Read apt's proposed changes before accepting them. This is an Ubuntu workshop package selection using [Ubuntu's package-management procedure](https://documentation.ubuntu.com/server/how-to/software/package-management/), not a universal prerequisite for every agent. Add `git` only if needed for the chosen distribution/review workflow. Add `python3-venv` only if the agreed exercise uses third-party Python dependencies. The proposed standard-library exercise needs neither pip nor a venv. Do not install Node just to install Claude or Codex.

## Prework C: install ONE agent, if using the live route

Use your organization's approved packaging/distribution process where available. Otherwise open the linked official install page directly, verify its exact URL, and use that vendor's current instructions. The commands below split download and execution so the preparer can inspect the script first. **Inspection and HTTPS do not pin or authenticate every downstream dependency.** Organizer records exact versions after rehearsal and rechecks before the event.

Run as the intended non-root user in the disposable lab. Choose one block. Downloads go in a unique temporary directory; no shell profile edits are prescribed here.

**Claude Code — [official setup](https://code.claude.com/docs/en/setup):**

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
cite_installer_dir=$(mktemp -d)
curl -fL https://claude.ai/install.sh -o "$cite_installer_dir/claude-install.sh"
# STOP if curl failed. Read this file before executing it:
less "$cite_installer_dir/claude-install.sh"
# After review, and only if the download succeeded:
bash "$cite_installer_dir/claude-install.sh"
```

**Codex CLI — [official CLI install](https://learn.chatgpt.com/docs/codex/cli):**

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
cite_installer_dir=$(mktemp -d)
curl -fL https://chatgpt.com/codex/install.sh -o "$cite_installer_dir/codex-install.sh"
# STOP if curl failed. Read before executing:
less "$cite_installer_dir/codex-install.sh"
# After review, and only if the download succeeded:
sh "$cite_installer_dir/codex-install.sh"
```

**Hermes — optional extension; [official install](https://hermes-agent.nousresearch.com/docs/getting-started/installation):**

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
cite_installer_dir=$(mktemp -d)
curl -fL https://hermes-agent.nousresearch.com/install.sh -o "$cite_installer_dir/hermes-install.sh"
# STOP if curl failed. Read before executing:
less "$cite_installer_dir/hermes-install.sh"
# Reviewed CLI-only adaptation using documented options:
bash "$cite_installer_dir/hermes-install.sh" --skip-browser --skip-computer-use
```

Hermes's source installer manages its runtime/tool dependencies; it can require system libraries and administrative package preparation. Browser/computer-use downloads are unnecessary for these labs. Those skip switches do not remove all dependencies or disable every tool. Its provider setup is separate from installation. Do not import existing agents' settings, credentials, or memories for the workshop. See the [quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart) for minimal setup and provider selection. Retrieved 2026-11-10.

Reopen the same Linux terminal after installation. If Claude or Hermes is absent from PATH, inspect the installer's reported launcher directory. A temporary session-only correction for their documented user launcher location is:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Do not apply that path to Codex without checking its actual installer output. Avoid repeatedly appending lines to startup files or sourcing a whole profile just to test PATH.

## Prework D: authentication and permissions

Complete one approved individual login before class. A successful installation or version check does not prove model access, quota, or approval policy.

- Claude: run `claude --version`, `claude doctor`, then `claude --permission-mode default` inside the exercise directory. Follow login prompts and inspect `/status` and `/permissions`. Account/provider options: [Anthropic authentication](https://code.claude.com/docs/en/authentication). Manual mode is explicit; do not assume the starting mode or that every read prompts. See [CLI reference](https://code.claude.com/docs/en/cli-reference).
- Codex: run `codex --version`, `codex --help`, then `codex login`. ChatGPT sign-in and API-key billing are distinct options. If the browser callback fails, `codex login --device-auth` is documented as beta and requires device-login availability/settings. See [OpenAI authentication](https://learn.chatgpt.com/docs/auth).
- Hermes: run `hermes --version`, `hermes setup`, and `hermes doctor` in the lab. Choose a minimal setup and an approved provider; leave integrations off. `hermes doctor` includes network connectivity checks; it is not part of the offline script. Keep its output private. Current quickstart requires a model context window of at least 64K; do not promise a small local model as a drop-in rescue.

All three need a successful real response for the live route. Account access, provider authorization, limits, and model compatibility must be checked with a harmless synthetic prompt. Do not paste keys into prompts, startup-file examples, command history, or the participant workbook. Do not read/copy existing credential caches to solve a classroom login issue.

**Codex session:** use `codex --sandbox workspace-write --ask-for-approval on-request` where local policy permits. This combination is in the [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli). Inspect `/status`; permissions may be managed. New permission profiles and older sandbox settings do not compose: [OpenAI permissions](https://learn.chatgpt.com/docs/permissions). Do not rewrite someone's managed configuration to force this example.

**Claude Linux sandbox:** WSL2 support does not mean the sandbox is enabled. For the proposed sandboxed lane, an administrator prepares `bubblewrap` and `socat`; inspect `/sandbox` and use regular permissions mode. Current docs describe optional additional filtering and AppArmor issues: [sandbox setup](https://code.claude.com/docs/en/sandboxing). Do not disable AppArmor/user-namespace protections or permit unsandboxed retries as a classroom fix.

**Hermes permissions:** inspect the active approvals and enabled tools. Manual dangerous-command prompts are not an OS sandbox or an approval for every possible file operation. Do not use `/yolo`, `--yolo`, or one-shot automation for the core exercise. See [Hermes security](https://hermes-agent.nousresearch.com/docs/user-guide/security).

## Copy and run paths — prepared lab environment only

The workbook commands run from a **disposable copy of the teaching kit**, not the repository root and not `linux/`. With the repository already available inside the approved disposable Linux environment, begin at its root and create a unique copy:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
# Bash in the approved disposable Linux environment; repository root
cite_lab_parent=$(mktemp -d "$HOME/cite-workshop.XXXXXX")
cp -R Workshop-Team/teaching "$cite_lab_parent/kit"
cd "$cite_lab_parent/kit"
pwd
python3 --version
python3 -c "from pathlib import Path; print(Path('labs/signins.csv').is_file())"
mkdir -p work
```

Stop if any step fails; expected fixture result is `True`. This copy recipe is a proposed integration instruction, not a claim that this machine is isolated by `mktemp`/`cp`. If the final distributed archive has a different root, the lead must provide/rehearse the equivalent path instead. Copies and outputs must remain in the approved lab environment.

Optional preflight is run **before changing directories**, from repository root as `bash Workshop-Team/linux/preflight.sh`. If already in `Workshop-Team/linux/`, use `bash preflight.sh`. That file is not in the teaching-only kit, so do not run `bash preflight.sh` inside the copied kit. The script discovers tools and checks the Python floor; it does not validate model access or isolation.

After reading the reference scripts, the no-account **runtime** route inside the copied kit is:

**UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY**

```bash
python3 labs/reference_triage.py labs/signins.csv work/reference-events.csv
python3 labs/check_triage.py work/reference-events.csv
python3 labs/reference_report.py \
  work/reference-events.csv work/reference-review.html
```

Expected: four flags, checker `PASS: exact IDs, order, source values and reasons`, and HTML with four review events/three categories. Input SHA-256 for the reviewed `labs/signins.csv`: `67aee15ccb0ddad1e7330a263b337c986a6d91116d599b314f83df357d428c34`. Existing outputs are refused; rerun in a fresh kit or use new output names throughout. Do not delete results to conceal an earlier error. The reference renderer's CSV-header validation needs improvement before final release; see the Round 2 review. Open local HTML only after source inspection, within the disposable environment. No server is required.

## In the room: elapsed 20–28, switch unresolved setup at 25

1. **20–23:** locate prepared kit/printed packet, check current directory/fixture/Python, choose live, runtime-only or paper route. Do not download/copy a repository for the first time during this block.
2. **23–25:** helpers may resolve simple approved path/session issues. For the live route inspect effective identity/permissions. An optional harmless READY response checks inference only, not containment; it is unnecessary for offline routes.
3. **25–28:** unresolved participants switch to the printed/authored specimens or already prepared reference route. Everyone predicts a source row, inspects a permission decision or transitions to lab 1. No installer, account creation or provider change.
4. **28:** lab 1 begins for everyone. Reference execution belongs to lab work periods, not an extra readiness task.

This is teaching's **3-minute readiness + 5-minute recovery/transition allocation**. The original Linux five-minute proposal is superseded, not added to these eight minutes. Never call specimen review live inference or manual checking successful execution. Retain errors locally and switch routes.

## Troubleshooting

| Symptom | First action | In-room fallback |
| --- | --- | --- |
| `wsl` absent, distribution missing, WSL1 | Device admin handles approved preparation before the event | Printed/files route |
| `command not found` | Reopen the correct Linux terminal; inspect `command -v TOOL` and installer launcher path | Saved response |
| Windows executable selected in WSL | Inspect `command -v TOOL`; use the Linux installation, keep project under `~` | Saved response |
| TLS/certificate, DNS, proxy, VPN failure | Ask device/network administrator; use approved proxy and CA configuration | Offline kit |
| Login/429/quota/timeout | Check identity and exact error; do not infer that a free plan is the only cause | Saved response or account-holder demo |
| Sandbox/AppArmor failure | Verify dependencies and documented device policy with admin | Approved prepared VM or offline kit |
| Hermes diagnostics fail for an optional tool | Determine whether the selected exercise needs it; no automatic `--fix` | Use selected primary agent or saved response |

Do not prescribe VPN/EDR shutdown, TLS bypass (`curl -k`), public DNS replacement, broad permission changes, or an unreviewed installer as troubleshooting. [Microsoft's WSL troubleshooting](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting) distinguishes several VPN/proxy/DNS cases; one generic workaround is unreliable.

## Concise platform alternatives

- **macOS:** already prepared native Claude/Codex can follow the same text task; Python naming and shell startup files differ. No Homebrew installation is needed just for the text task. Verify device support on the vendor setup page. Hermes currently lists Apple Silicon as its supported macOS platform: [platform matrix](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support).
- **Native Windows:** use the vendor's native Windows installation path if already approved. Do not paste Ubuntu `apt` or Linux installer instructions into Git Bash and assume equivalence. Current [Claude setup](https://code.claude.com/docs/en/setup) and [Codex Windows guidance](https://learn.chatgpt.com/docs/windows/windows-sandbox) differ in sandbox support. Native Windows is an alternative workflow requiring its own rehearsal, not a claim of Linux command compatibility.

These alternatives are appendices, not extra live install tracks. All official documentation above was retrieved 2026-11-10.
