---
title: Command verification matrix and official sources
date: 2026-11-10
status: source-checked-not-linux-tested
---

# Command verification matrix

**Retrieval date for every source/row: 2026-11-10.** Sources were opened and relevant sections read, not accepted from search snippets, except the explicitly marked GNU reference fetch failures below. OpenAI's old `developers.openai.com/codex/…` pages redirected to `learn.chatgpt.com`; links below use the resulting official documentation. This date records retrieval (or a marked failed attempt), not a software release or successful install date.

Status **D** = documented upstream; **A** = workshop adaptation of documented procedure; **H** = held out of core, unresolved or unnecessary. **None of these install/login/agent commands was executed during this audit.** Expected results below are checkpoints, not observed outputs. See [VERIFICATION.md](VERIFICATION.md) for actual host checks.

## Environment and install commands

| Context | Command or claim | Status / decision | Expected checkpoint | Official URL |
| --- | --- | --- | --- | --- |
| Windows PowerShell | `wsl --install -d Ubuntu-24.04` | D/A: distro choice is workshop baseline; admin/restart prework | Ubuntu installed and initialized | [Microsoft install](https://learn.microsoft.com/en-us/windows/wsl/install) |
| Windows PowerShell | `wsl --list --verbose` | D: mandatory distinction | Distribution has VERSION 2 | [Microsoft install](https://learn.microsoft.com/en-us/windows/wsl/install) |
| Windows PowerShell | `wsl --status`; `wsl --list --online` | D: inspect state/available distributions | Status or published distro list; missing install can error | [Microsoft basic commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands) |
| Linux workspace | Keep Linux project under Linux home | D: recommend for this lane | Project not on `/mnt/c` | [Microsoft file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems) |
| Ubuntu Bash | `sudo apt update`; `sudo apt install ca-certificates curl python3` | A: minimal package selection; approved prework only | Package manager reports successful completion | [Ubuntu package management](https://documentation.ubuntu.com/server/how-to/software/package-management/) |
| Linux shell | `command -v bash`; `python3 --version`; `uname -m`; `id -u` | A: authored prerequisite discovery; Python version flag source-checked; GNU reference fetches timed out | Bash, selected architecture, non-root user; Python for script route | [Python CLI](https://docs.python.org/3/using/cmdline.html); unverified retrieval: [Bash builtin](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html), [GNU utilities](https://www.gnu.org/software/coreutils/manual/html_node/System-context.html) |
| Claude Linux/WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | D: URL/command match; download/review/run separately in guide | `claude --version` prints installed version | [Anthropic setup](https://code.claude.com/docs/en/setup) |
| Codex Linux/WSL2 | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | D: standalone route; Node unnecessary for this route | `codex --version` prints installed version | [OpenAI CLI install](https://learn.chatgpt.com/docs/codex/cli) |
| Codex alternate packaging | `npm install -g @openai/codex`; `brew install --cask codex` | D/H: valid alternatives, not extra core prerequisites | One selected install owns the executable | [OpenAI CLI install](https://learn.chatgpt.com/docs/codex/cli) |
| Hermes Linux/WSL2 | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` | D: source installer, not a tiny standalone binary | Installed launcher responds | [Nous install](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |
| Hermes installer | `bash downloaded-script --skip-browser --skip-computer-use` | A: switches documented; wrapper not install-tested | Browser/desktop-control downloads omitted; other deps remain | [Nous install](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |
| Hermes runtime | Git/curl/tar/SHA-256 utilities; managed Python/toolchain | D: do not substitute an arbitrary system Python/Node recipe | Prerequisites satisfied in prepared image | [Nous install](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |
| Claude Linux sandbox | `sudo apt-get install bubblewrap socat`; `/sandbox` | D: administrator prework plus session check | Sandbox enabled with dependency/policy issues resolved | [Anthropic sandbox](https://code.claude.com/docs/en/sandboxing) |
| Optional Node lane | nvm `master/install.sh` | H: replace moving branch if ever needed | Current README uses tagged v0.41.0; pin runtime after rehearsal | [nvm upstream](https://github.com/nvm-sh/nvm#installing-and-updating) |
| Native Windows | PowerShell vendor installer, not POSIX install in Git Bash | D/H: appendix, separate rehearsal | Correct native executable and shell | [Claude setup](https://code.claude.com/docs/en/setup), [Codex install](https://learn.chatgpt.com/docs/codex/cli), [Hermes install](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |

The original vendor pipe-to-shell forms above are audit comparisons, not instructions to run every installer. The guide's `mktemp`/`curl -fL -o`/`less` sequence is an **adaptation**; downstream installer contents and downloads were not executed or fully audited. Never add `sudo` to vendor installer commands as a permissions workaround.

## Agent access, diagnostics, permissions

| Context | Command or claim | Status / decision | Expected checkpoint | Official URL |
| --- | --- | --- | --- | --- |
| Claude terminal | `claude --version`; `claude doctor` | D: installation diagnostics, not proof of model access | Version; diagnostics interpreted for selected lane | [Anthropic setup](https://code.claude.com/docs/en/setup) |
| Claude launch | `claude --permission-mode default` | D: explicitly choose documented Manual/default mode | Inspect permissions in active session; managed settings apply | [Anthropic CLI](https://code.claude.com/docs/en/cli-reference), [permissions](https://code.claude.com/docs/en/permissions) |
| Claude session | `/status`; `/permissions` | D: inspect identity and effective controls | Correct account/provider and intended permission rules | [Anthropic interactive mode](https://code.claude.com/docs/en/interactive-mode), [permissions](https://code.claude.com/docs/en/permissions) |
| Claude auth | Start `claude`, complete approved login | D: account/provider options, not paid-plan-only diagnosis | One harmless inference works | [Anthropic authentication](https://code.claude.com/docs/en/authentication) |
| Codex terminal | `codex --version`; `codex --help` | A/D: local binary check; confirm installed interface | Version/help; not inference | [OpenAI CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) |
| Codex auth | `codex login`; `codex login --device-auth` | D: browser login; device code is beta/availability-dependent | Approved individual login completes | [OpenAI authentication](https://learn.chatgpt.com/docs/auth) |
| Codex API-key alternative | `printenv OPENAI_API_KEY \| codex login --with-api-key` | D/H: documented, not needed for baseline; no sample secret values | Authorized API access, separate usage billing | [OpenAI authentication](https://learn.chatgpt.com/docs/auth) |
| Codex session | `codex --sandbox workspace-write --ask-for-approval on-request` | D: documented combination; existing managed profile may constrain use | `/status` shows effective controls | [OpenAI CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [permissions](https://learn.chatgpt.com/docs/permissions) |
| Codex WSL | WSL2, not WSL1 | D: current docs say WSL1 support ended after 0.114 | Prepared WSL2 session | [OpenAI WSL](https://learn.chatgpt.com/docs/windows/wsl) |
| Hermes setup | `hermes setup`; `hermes model` | D: configure one approved provider/model; opt out of extras | Known provider, model, and successful synthetic response | [Nous quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart), [CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Hermes terminal | `hermes --version`; `hermes doctor` | D: doctor can make a connectivity probe; no `--fix` in preflight | Version and relevant diagnostics reviewed | [Nous CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Hermes approvals | Manual/smart/off; `/yolo` | D/H: no bypass for core; manual covers dangerous commands, not every operation | Effective tools and approvals inspected | [Nous security](https://hermes-agent.nousresearch.com/docs/user-guide/security) |
| Hermes one-shot | `hermes -z "task"` always approves everything | H: blanket safety claim not established by retrieved docs; no core use | Requires exact-version controlled test | [Nous CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands), [security](https://hermes-agent.nousresearch.com/docs/user-guide/security) |
| Hermes troubleshooting | Bare `hermes --safe-mode` | H: incomplete recipe; current reference requires explicit model | Use installed help plus approved provider; not an isolation guarantee | [Nous CLI](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| All agents | Reply READY, tools prohibited in prompt | A: inference smoke check only | Response arrives; no claim that prompt enforces isolation | Vendor auth/session references above |

Hermes's security guide describes headless single-query denial policy, while the CLI reference describes `-z` as a scripted one-shot. They do not establish identical approval semantics for every version and entry point. Preserve this as an unresolved version-specific behavior instead of silently replacing one blanket assertion with another.

## Removed shortcuts and policy claims

| Existing instruction | Audit decision | Official evidence |
| --- | --- | --- |
| Save `clauded` bypass alias for class | Remove from teaching path; scratch folder is not containment | [Claude permissions](https://code.claude.com/docs/en/permissions), [sandbox](https://code.claude.com/docs/en/sandboxing) |
| Approves before every edit/command by default | Qualify: effective mode, rules, and tool determine prompts | [Claude permissions](https://code.claude.com/docs/en/permissions) |
| Paid setup means no model training | Correct: consumer choices and commercial policies differ | [Anthropic data usage](https://code.claude.com/docs/en/data-usage) |
| All free OpenRouter providers train/log identically | Correct: endpoint policy/settings differ; use synthetic-only classroom rule | [OpenRouter provider policies](https://openrouter.ai/docs/guides/privacy/provider-logging) |
| OpenRouter is no-account fallback | False: account/key/model availability remain dependencies; keep outside core | [OpenRouter Claude integration](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration) |
| Persistent shell-profile API keys | Avoid; provider docs themselves flag plaintext profile hygiene | [OpenRouter integration](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration) |
| Blank SSH passphrase, accept host key blindly | Remove key generation from core; if follow-up, protect key and verify fingerprint | [GitHub passphrases](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases), [SSH test](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection) |
| `ssh -T git@github.com` requires exit 0 | Correct: GitHub documents exit 1 on successful authentication; inspect message/identity | [GitHub SSH test](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection) |
| Disconnect VPN as generic WSL repair | Replace with admin-supported diagnosis and offline route | [Microsoft troubleshooting](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting) |
| Native Windows is always unsandboxed | Tool-specific: Claude and Codex currently differ | [Claude setup](https://code.claude.com/docs/en/setup), [OpenAI Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox) |

## Evidence still required before publication

Round 2 runtime clarification: the workshop recommends maintained CPython **3.11+**, with Ubuntu 24.04/Python 3.12 as the proposed Linux rehearsal target. This is a support policy, not a language-syntax floor or a vendor CLI prerequisite. [Python upstream status](https://devguide.python.org/versions/), retrieved 2026-11-10, lists 3.11+ as supported and 3.10 as end-of-life. The offline preflight now checks this floor with an isolated, no-site Python invocation; Linux runtime execution remains untested.

Record actual OS/distro/architecture, WSL version, installed agent version, installer channel/package owner, account route without identifiers, permission status, fixture hash, command exit codes, and expected-versus-observed result. Use no credentials in the record. Rehearse on fresh approved Linux and WSL2 images, then recheck upstream near the workshop date. Version numbers printed on existing cheat sheets are source claims, not versions observed during this audit.
