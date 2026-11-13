---
title: Skills, Agents, and Plugins
section: 5
status: draft
tags: [cite-talk-2026, slides, skills, agents, plugins, ecc]
---

# Skills, agents, and plugins

Section 5 of [[Talk Outline]]. This is a deck. Each `##` heading is one slide. The **Slide** line is on-screen text; the rest is speaker notes. It ends with installing ECC, a large open-source bundle, so the room sees that they do not have to build everything from scratch.

Teaching order is smallest to largest: a skill is a page of instructions, an agent is a worker you hand a job to, and a plugin is a package that ships skills, agents, and more as one unit.

Verify the commands against a current install before presenting. Claude Code changes fast. Details here were checked on 2026-10-29 against the Claude Code docs.

## Slide 1. Why extend Claude Code at all

**Slide:** Out of the box it is general. These three features make it yours.

Speaker notes:
- So far the talk has used plain Claude Code. It is already useful. The gap is that it does not know your district, your procedures, or the way you want work done.
- Three features close that gap. Skills teach it a repeatable task. Agents give it a specialist to delegate to. Plugins package both so you can share them or install someone else's.
- The payoff slide at the end: install ECC and get 71 agents and 300-plus skills in two commands.

## Slide 2. Skills: a repeatable task written down

**Slide:** A skill is a Markdown file that teaches Claude one task, loaded when it is relevant.

Speaker notes:
- A skill is a folder with a `SKILL.md` file in it. The file is plain Markdown with a short header.
- Claude reads the header of every skill at startup, so it knows the skill exists. It loads the full instructions only when the task matches, or when you run it by name with a slash command.
- Example that lands for this room: a skill that reviews a firewall config against your district's standard, written once, used every time.
- Two places a skill can live:
  - `~/.claude/skills/<name>/SKILL.md` is personal, available in all your projects.
  - `.claude/skills/<name>/SKILL.md` sits in a project and ships to anyone who clones it.

## Slide 3. Build a skill by hand

**Slide:** Three steps. A folder, a file, a test.

Speaker notes. Do this live. It takes two minutes.

Make the folder:

```bash
mkdir -p ~/.claude/skills/config-review
```

Create `~/.claude/skills/config-review/SKILL.md` with this content:

```markdown
---
description: Reviews a network device config against district security standards. Use when the user shares a switch, router, or firewall config and asks whether it is safe.
---

## Instructions

Review the configuration the user provides. Check for:
- default or weak credentials, and SNMP community strings left at public or private
- management interfaces reachable from student or guest networks
- telnet or other unencrypted management, where SSH should be used
- missing logging to the district syslog server

Produce a table of findings: issue, the line it is on, severity for a
school network, and the exact fix. Do not change the file.
```

- The `description` is the only part that matters for triggering. Claude reads it to decide when to use the skill, so write it as "what it does and when to use it".
- `name` is optional. Without it, the skill takes the folder name, so this one runs as `/config-review`.

Test it: paste a config and ask "is this switch config safe?", or type `/config-review`.

## Slide 4. Agents: a specialist you delegate to

**Slide:** An agent is a subagent with its own job, tools, and clean context.

Speaker notes:
- An agent, or subagent, is a worker Claude hands a whole task to. It runs in its own context window, does the work, and returns only the answer. Your main conversation stays clean.
- Why this matters for a small team: you can give an agent a narrow job and a narrow set of tools. A read-only review agent that cannot change files. A log-analysis agent that only reads and runs scripts.
- The difference from a skill in one line: a skill is instructions Claude follows itself; an agent is a separate helper Claude calls and waits for. Use an agent when the job is big enough to deserve its own context, or when you want to limit what it can touch.
- Same two locations as skills, with `agents` instead of `skills`:
  - `~/.claude/agents/` is personal.
  - `.claude/agents/` ships with a project.

## Slide 5. Build an agent by hand

**Slide:** One Markdown file. A header that says who it is, a body that is its brief.

Speaker notes. Do this live.

Create `~/.claude/agents/log-triage.md`:

```markdown
---
name: log-triage
description: Reviews exported security logs and surfaces only the events worth a human look. Use for sign-in logs, firewall logs, or audit exports.
tools: Read, Bash, Grep
model: sonnet
---

You are a security log analyst for a K-12 school district. When given a
log file, write and run code to find anomalies: logins from unusual
locations, impossible travel, bursts of failures followed by a success,
and activity outside normal hours. Return a ranked table of only the
events that merit review, each with the reason it was flagged. Never
modify the source file.
```

- `name` and `description` are required. The description is how Claude decides to delegate, so write it the same way as a skill's.
- `tools` is optional. Listing `Read, Bash, Grep` leaves out Edit and Write, but Bash can still change or delete files. Keep approvals on, use a copy of the input, and verify that the source stayed unchanged. Leave the tool list out and the agent inherits the parent tools.
- `model` is optional. `sonnet` is a sensible default for routine work; use `opus` for harder reasoning.
- The body is the agent's whole system prompt. It is its job description.

Test it: "use the log-triage agent on signins.csv". Note for older Claude Code: if you created the `agents` folder mid-session, restart so the watcher sees it.

## Slide 6. Plugins: skills and agents, packaged

**Slide:** A plugin is one directory that bundles skills, agents, hooks, and tool servers, installed as a unit.

Speaker notes:
- Once you have a few skills and agents, a plugin is how you package them. It is a folder with a small manifest and subfolders for each component.
- A plugin can hold more than skills and agents. It can add hooks, which are commands that run automatically at points in Claude's work, and MCP servers, which connect Claude to outside tools.
- You install a plugin from a marketplace, which is just a Git repository that lists plugins. One command to add the marketplace, one to install.
- Why you care: you can install a setup someone else built in two commands, and you get updates. You can also hand your own to the rest of your team.
- The honest caveat, because the room is security staff: an enabled plugin runs with your permissions. Its hooks fire and its servers run in every session. Read what it does before you install it, the same way you read a script before running it as admin.

## Slide 7. Build a plugin by hand

**Slide:** A manifest and the folders your components already live in.

Speaker notes. Show the structure; you do not have to build it fully live.

A minimal plugin directory:

```
my-security-pack/
  .claude-plugin/
    plugin.json
  skills/
    config-review/
      SKILL.md
  agents/
    log-triage.md
```

The manifest at `.claude-plugin/plugin.json`:

```json
{
  "name": "my-security-pack",
  "version": "0.1.0",
  "description": "Config review skill and log-triage agent for K-12 IT."
}
```

- The `skills` and `agents` folders hold the same files you just wrote. A plugin does not reinvent them; it collects them.
- To develop it without publishing, point Claude Code at the folder with `claude --plugin-dir ./my-security-pack`.
- To share it, push the folder to a Git repository with a `marketplace.json`, and teammates install from there.

## Slide 8. You do not have to build it all: install ECC

**Slide:** ECC is an open-source bundle: 71 agents, 300-plus skills, in two commands.

Speaker notes:
- ECC is a free, open-source harness for Claude Code. It packages planning, test-first workflows, self-review, memory, and a large library of security and engineering skills and agents. Source is at github.com/affaan-m/ECC.
- This is the point of the section. The manual tutorials show you how the pieces work. ECC shows that a community has already built hundreds of them, including a security scanner for agent configs.
- Install it live. Inside a Claude Code session:

```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

- There is also a guided installer outside Claude Code, which lets you pick a smaller profile instead of everything:

```
npx ecc-universal@2.2.3 setup
```

- Check the repository for the current version number before the talk; the `npx` line pins one. The two `/plugin` commands do not, so they are the safer choice on stage.
- After it installs, show one thing it added. Run `/plugin` and point at ECC in the installed list, or trigger one of its security skills.

## Slide 9. A starter kit of plugins

**Slide:** ECC is one option. Here are five smaller ones worth installing the same way.

Speaker notes:
- ECC is a large bundle. These five are focused plugins that each do one thing well, installed with the same two-command pattern. Install the ones that fit the work; skip the rest.
- Install each inside a Claude Code session, then run `/reload-plugins` or restart so they load.

Humanizer. Rewrites AI-sounding text so it reads like a person wrote it. Useful for the policy and communication drafts from the GRC examples.

```
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

Superpowers. A library of workflows for planning, test-first development, and systematic debugging. It makes Claude plan before it builds.

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Frontend design. Anthropic's own skill for building interfaces that look right. Its marketplace is already registered, so it is a one-line install. Relevant to the nmap web front end from [[Application Builds]].

```
/plugin install frontend-design@claude-plugins-official
```

Impeccable. A design-quality skill that audits a front end for accessibility, performance, and responsiveness. It builds on the frontend design skill above, so install one or the other, not both, unless you want the audit commands.

```
/plugin marketplace add pbakaus/impeccable
/plugin install impeccable@impeccable
```

TDD. Enforces red-green-refactor so the code Claude writes comes with tests. Matt Pocock's plugin bundles a `tdd` skill you run as `/tdd`. Several other TDD plugins exist too.

```
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

- Say the security line once more here: each of these runs with your permissions when enabled. These five are popular and open source, but the rule stands. Check a plugin before you install it.

## Slide 10. When to use which

**Slide:** Skill for a task. Agent for a delegated job. Plugin to package or install.

Speaker notes:
- Skill: you do the same task often and want Claude to do it your way. Lowest effort.
- Agent: the job is large or you want to limit what Claude can touch while it runs. A read-only reviewer is the classic case.
- Plugin: you have several of the above and want to share them, or you want someone else's whole setup like ECC.
- Leave the room with one action: write one skill for the task you repeat most. It is a folder and a file.

## Caveats and things to verify

- All paths and commands checked against the Claude Code docs on 2026-10-29. Re-verify near the talk date.
- The ECC agent and skill counts come from its repository and will drift. Say "dozens of agents and hundreds of skills" if you do not want to recheck exact numbers.
- ECC installs a large amount into every session, which has a context and usage cost. Mention that the guided installer's smaller profiles exist for people who do not want all of it.
- The plugin security point is not optional for this audience. Keep it.
- Install names verified against each marketplace manifest on 2026-11-02: `humanizer@humanizer`, `superpowers@superpowers-marketplace`, `frontend-design@claude-plugins-official`, `impeccable@impeccable`, and `mattpocock-skills@mattpocock`. Marketplaces change, so a quick check with `/plugin` before the talk is still worth it.
- "TDD" is a crowded space. The slide uses Matt Pocock's plugin, where tdd is one skill among several. Alternatives include nizos/tdd-guard for hard enforcement that blocks out-of-order edits. Superpowers also bundles a test-first workflow, so if you install superpowers you may not need a separate TDD plugin.

## Open questions for this section

- Decide whether to build the plugin fully live in slide 7 or show the structure as a diagram. Live is riskier and slower; the skill and agent builds in slides 3 and 5 already prove the hands-on point.
- Confirm you want ECC specifically, given its size and that it runs with full permissions. A smaller, security-focused plugin might suit the room better. Your call; the section is written around ECC as requested.
