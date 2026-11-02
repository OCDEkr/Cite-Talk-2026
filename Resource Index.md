---
title: Resource Index
status: draft
audience: attendees
tags: [cite-talk-2026, resources, handout]
---

# Resource index

A starting list of repositories worth knowing for AI-assisted work. Grouped so you can find a category, not memorize a list. Each entry says what the project is in a sentence or two. Descriptions were written from each repository on 2026-11-02; projects move fast, so check the repo before you rely on one.

Linked from [[Talk Outline]]. This is a living list; add to it as you find things.

## Claude Code core and official

- **[Claude Code](https://github.com/anthropics/claude-code)** Anthropic's agentic coding tool that runs in your terminal, reads your codebase, and handles coding, explanation, and git work from natural-language instructions. This is the tool the whole talk is built on.
- **[Anthropic Skills](https://github.com/anthropics/skills)** Anthropic's public collection of Agent Skills, each a folder with a `SKILL.md` of instructions Claude loads for a task. Doubles as working examples and a template for writing your own.
- **[Claude Plugins (Official)](https://github.com/anthropics/claude-plugins-official)** Anthropic's curated directory of Claude Code plugins, split into internal and third-party. Install any of them with `/plugin install <name>@claude-plugins-official`.

## Skill collections and frameworks

- **[Superpowers](https://github.com/obra/superpowers)** A skills framework and methodology that makes a coding agent brainstorm, plan, and follow test-driven development before writing code. Installs across many agent harnesses.
- **[Matt Pocock Skills](https://github.com/mattpocock/skills)** A set of reusable agent skills from one engineer's own working directory, covering alignment interviews, test-driven development, bug diagnosis, and codebase design.
- **[Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills)** A curated catalog of Claude Skills and related tools, sorted by category, including prebuilt automations for dozens of SaaS apps. A good place to browse what exists.
- **[Karpathy Skills](https://github.com/multica-ai/andrej-karpathy-skills)** A single `CLAUDE.md` of guidelines, based on Andrej Karpathy's notes on common LLM coding mistakes, meant to make Claude Code less error-prone. Use as a plugin, a project `CLAUDE.md`, or a Cursor rule.
- **[G-Stack](https://github.com/garrytan/gstack)** A collection of slash commands that give Claude Code specialized roles such as designer, QA lead, and release engineer, covering a sprint from planning to shipping.
- **[Oh My Claude Code](https://github.com/yeachan-heo/oh-my-claudecode)** A plugin that adds multi-agent orchestration to Claude Code, with workflows like `/autopilot` and `/team` and the ability to run other AI CLIs in tmux panes.
- **[ECC](https://github.com/affaan-m/ecc)** A large open-source agent harness that adds planning, test-first workflows, self-review, memory, and a big library of skills and agents, including a security scanner. Covered in the talk's skills, agents, and plugins section.
- **[Ponytail](https://github.com/dietrichgebert/ponytail)** A prompt and skill set that pushes an agent to write the smallest solution that still handles validation, security, and errors. Works across Claude Code, Codex, and Cursor.

## Memory

- **[Claude Memory](https://github.com/thedotmack/claude-mem)** A memory plugin that records what an agent does in a session, condenses it into searchable summaries, and feeds the relevant context back into later sessions.
- **[Agent Memory](https://github.com/rohitg00/agentmemory)** A persistent memory system that captures session activity and makes past decisions and fixes searchable, shared across agents through MCP, REST, or native hooks.

## Planning and orchestration

- **[Planning with Files](https://github.com/othmanadi/planning-with-files)** A skill that keeps task plans and progress in Markdown files on disk, re-injecting the plan each turn so it survives context loss, compaction, and crashes.
- **[Archon](https://github.com/coleam00/archon)** A harness builder that defines development processes as YAML workflows, running agents alongside scripts, tests, and human approval gates. A bundled pack can take an issue to a merged pull request.
- **[Vibe-Kanban](https://github.com/BloopAI/vibe-kanban)** A kanban board paired with coding agents, giving each task its own branch, terminal, and dev server, with diff review and pull requests. Note: the project has announced it is shutting down.

## Codebase understanding and web context

- **[Context7](https://github.com/upstash/context7)** Gives agents current, version-specific documentation and code examples for libraries, so they do not rely on outdated training data. Delivered as an MCP server or a CLI.
- **[RepoMix](https://github.com/yamadashy/repomix)** Packs an entire repository into a single AI-friendly file for feeding to a model, with token counts, secret scanning, and compression options.
- **[CodeGraph](https://github.com/colbymchenry/codegraph)** Builds a local knowledge graph of a codebase's symbols, calls, and dependencies and keeps it synced, so agents pull relevant code in fewer tokens. Connects over MCP.
- **[Graphify](https://github.com/Graphify-Labs/graphify)** Turns code, docs, schemas, and PDFs into a queryable knowledge graph, parsed locally, with each connection labeled explicit or inferred. Runs as a skill for coding agents.
- **[Firecrawl](https://github.com/firecrawl/firecrawl)** An API to search, scrape, and crawl the web at scale, converting sites into Markdown or structured JSON that agents can consume.

## Design and UX

- **[UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** A skill that gives coding assistants design guidance across frameworks: searchable styles, color palettes, font pairings, and stack-specific rules, and can generate a tailored design system.
- **[TasteSkill](https://github.com/leonxlnx/taste-skill)** A set of skills that gives agents art direction, real reference images, and a browser check so they build distinctive sites and screens instead of generic AI pages.

## Tooling and infrastructure

- **[GitHub MCP](https://github.com/github/github-mcp-server)** GitHub's official MCP server, connecting AI tools to GitHub to browse repos and manage issues and pull requests through natural language. Runs hosted or locally.
- **[CC Switch](https://github.com/farion1231/cc-switch)** A desktop control panel for AI coding tools that lets you switch API providers and manage MCP servers, skills, and prompts without hand-editing each tool's config.
- **[Visual Explainer](https://github.com/nicobailon/visual-explainer)** A skill that turns complex terminal output into styled HTML pages for diagrams, diff reviews, plan audits, and tables. Installs as a Claude Code plugin and also supports other agents.

## Security

- **[Maltese](https://github.com/HPE-AppliedSecurityResearch/maltese)** An HPE security-research tool that emulates malware network traffic, including domain-generation-algorithm and replay behavior, for evaluating malware detectors. Use it in a lab, not on a production network.

## Notes

- **Vibe-Kanban** is winding down. Keep it on the list for now as a reference, but do not build on it.
- **Maltese** is a dual-use security tool that generates malware-like traffic. It belongs in an isolated test environment with authorization, the same as any offensive tooling.
- Several of these overlap. Claude Memory and Agent Memory both do session memory; CodeGraph and Graphify both build codebase graphs; Context7 and the Anthropic skills both feed documentation. Pick one per job rather than stacking them.
