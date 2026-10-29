# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This is an Obsidian vault folder, not a software project. It holds the notes, outline, research, and slide material for "Cite Talk 2026", a talk on AI for cyber security. There is no build, lint, or test step; the content is Markdown files edited in Obsidian.

The folder lives inside a larger Obsidian vault (`/Users/kevin/Documents/Obsidian Vault/`). Only this subfolder is tracked in git.

## Working in this repo

- Write content as Obsidian-flavored Markdown. Use `[[wikilinks]]` to link notes within this folder, and keep links relative to this folder so they resolve when the repo is cloned on its own.
- Put reusable sources and citations in their own notes so the talk outline can link to them rather than duplicating text.
- Do not commit Obsidian workspace state (`.obsidian/workspace*.json`) or OS metadata; `.gitignore` already excludes these.
- The GitHub remote is `git@github.com:ocdekr/Cite-Talk-2026.git` over SSH (key: `~/.ssh/id_ed25519`). Default branch is `main`.
