"""Generate Hermes-Agent-Cheat-Sheet.pdf (2-page landscape reference).

Needs Python 3.10+ and reportlab:
    python3 -m venv .venv && .venv/bin/pip install reportlab
    .venv/bin/python scripts/hermes_sheet.py "Cheat Sheets/Hermes-Agent-Cheat-Sheet.pdf"

Layout lives in cheatsheet_lib.py. Prints OVERFLOW if a column runs past the footer.
"""
import sys
from cheatsheet_lib import *

c = start("Hermes Agent Cheat Sheet",
          "Checked against Hermes Agent 0.23.1 and its bundled docs, November 2026. "
          "Commands change between releases: type /help in a session to see the current list.",
          sys.argv[1])

# ---------------- Page 1 ----------------
header(c, "Starting, keys, and approvals", 1)

y = TOP
y = section(c, X[0], y, "01", "Start a session (in your terminal)", [
    ("hermes", "Start an interactive chat in the current folder."),
    ("hermes -c", "Continue the most recent session. Add a name to pick a different one."),
    ("hermes -r ID", "Resume a session by ID or title. <b>-r latest</b> is the same as -c."),
    ('hermes -z "task"', "One-shot: print only the final answer. Good for scripts, but it skips approvals."),
    ("hermes -w", "Work in a separate git worktree so parallel agents don't collide."),
    ("hermes -s name", "Preload one or more skills. Comma-separate several."),
    ("--reasoning high", "Reasoning effort for this run, from none up to ultra."),
    ("--checkpoints", "Snapshot files before destructive edits. <b>/rollback</b> restores them."),
    ("hermes --tui", "Use the newer full-screen interface instead of the classic prompt."),
])
y = section(c, X[0], y, "02", "Setup and upkeep", [
    ("hermes setup", "Setup wizard: provider, API key, and model."),
    ("hermes model", "Pick the default model and provider."),
    ("hermes doctor", "Check configuration and dependencies."),
    ("hermes update", "Install the latest version."),
    ("hermes logs -f", "Follow the agent log live. <b>logs errors</b> shows only errors."),
    ("hermes --safe-mode", "Start with config, memory, plugins, and MCP servers all off, to rule them out."),
])
check(y, "p1c1")

y = TOP
y = section(c, X[1], y, "03", "Keys in a session", [
    ("Enter", "Send the message."),
    ("Ctrl+J", "New line. Alt+Enter works too, and Shift+Enter in terminals that support it."),
    ("Tab", "Accept the gray suggestion or complete a slash command."),
    ("Ctrl+C", "Clear what you typed. On an empty prompt, interrupt Hermes. Press twice to quit."),
    ("Esc Esc", "Open the transcript to edit an earlier prompt or fork from it. Same as /rewind."),
    ("Ctrl+G", "Write the prompt in your editor. Save and quit to send it."),
    ("Ctrl+S", "Set the draft aside. Press again on an empty prompt to get it back."),
    ("Ctrl+V", "Paste text and any image on the clipboard. Alt+V pastes just the image."),
    ("Ctrl+T", "Watch running subagents and background processes."),
    ("Ctrl+P", "Fuzzy command palette."),
    ("Ctrl+D", "Exit, on an empty prompt."),
], keyw=0.27)
y = section(c, X[1], y, "04", "Add context to a prompt", [
    ("@file:path", "Include a file. Add <b>:10-25</b> for just those lines."),
    ("@folder:dir", "Include a folder's file tree."),
    ("@diff", "Include your unstaged git changes."),
    ("@url:link", "Fetch a web page into the prompt, as in @url:https://example.com."),
    ("!command", "Run a shell command yourself without spending a model turn."),
], keyw=0.33)
check(y, "p1c2")

y = TOP
y = section(c, X[2], y, "05", "Approvals for risky commands", [
    ("manual", "Hermes asks before every dangerous shell command."),
    ("smart", "The default. A second model rates the risk: low-risk commands run, clearly dangerous ones are denied, and the rest ask you."),
    ("off", "No prompts at all. Only for throwaway containers or CI."),
    ("/approvals smart", "Set the mode for good. It is stored as <b>approvals.mode</b> in config.yaml."),
    ("/yolo", "Skip every approval in this chat only. <b>hermes --yolo</b> does the same at launch."),
], keyw=0.33)
y = callout(c, X[2], y, "Habits that save you", [
    "Run <b>/plan</b> first on anything big. It writes a plan to .hermes/plans/ and changes nothing.",
    "Start with <b>--checkpoints</b> in a real repo so <b>/rollback</b> has something to restore.",
    "Run <b>/diff</b> before you commit, and read it.",
    "Use <b>/new</b> or <b>/compress</b> between unrelated tasks. Old context costs tokens.",
    "Put API keys in ~/.hermes/.env. <b>hermes config set</b> sends secrets there for you.",
])
y = callout(c, X[2], y, "Watch out", [
    "<b>-z</b> one-shot runs and <b>/yolo</b> approve everything. Keep them away from production systems.",
    "Hermes reads AGENTS.md and memory files on startup. Check what's in them before you share a repo.",
])
check(y, "p1c3")
footer(c)
c.showPage()

# ---------------- Page 2 ----------------
header(c, "Slash commands by task", 2)

y = TOP
y = section(c, X[0], y, "06", "Manage the session", [
    ("/new", "Start a fresh session. /reset does the same."),
    ("/retry", "Send your last message again."),
    ("/undo 2", "Back up two of your turns and prompt again. Default is one."),
    ("/rewind", "Edit an earlier prompt and resend it, or fork from it."),
    ("/branch", "Copy this session into a new one to try something else."),
    ("/title name", "Name the session so you can find it later."),
    ("/sessions", "Browse past sessions and resume one."),
    ("/save md file", "Export the conversation as Markdown, JSON, or HTML."),
    ("/quit", "Leave. Add --delete to erase the session history too."),
], keyw=0.3)
y = section(c, X[0], y, "07", "Steer it while it works", [
    ("/queue text", "Line up a prompt for the next turn. Short form /q."),
    ("/steer text", "Slip in a note after the next tool call without stopping it. Short form /s."),
    ("/btw question", "Ask a side question that doesn't interrupt the task."),
    ("/bg text", "Run a prompt in a separate background session."),
    ("/agents", "Show running agents and tasks."),
    ("/stop", "Kill all background processes."),
], keyw=0.3)
check(y, "p2c1")

y = TOP
y = section(c, X[1], y, "08", "Context and model", [
    ("/status", "Session, model, tokens, and context in one view."),
    ("/context", "How full the context window is, and what is filling it."),
    ("/compress", "Summarize older turns to free room. Add <b>focus topic</b> to keep one thread. /compact works too."),
    ("/model name", "Switch model for this session. Add <b>--global</b> to keep it."),
    ("/reasoning high", "Change reasoning effort, or show and hide the model's reasoning."),
    ("/usage", "Token use and rate limits."),
], keyw=0.3)
y = section(c, X[1], y, "09", "Plan, review, and automate", [
    ("/init", "Scan the repo and write or update AGENTS.md, the project instructions."),
    ("/plan task", "Write a plan to .hermes/plans/ without running anything."),
    ("/review", "Start a separate subagent to review the work you just discussed."),
    ("/diff", "Show git changes. <b>/diff session</b> limits it to this session's edits."),
    ("/rollback", "List or restore file checkpoints."),
    ("/goal text", "Set a goal Hermes keeps working on across turns until it's met."),
    ("/loop 10m text", "Rerun a prompt on a timer in this session."),
    ("/cron", "Manage scheduled tasks that run outside the session."),
], keyw=0.3)
check(y, "p2c2")

y = TOP
y = section(c, X[2], y, "10", "Skills, tools, and memory", [
    ("/skills", "Search, install, and manage skills."),
    ("/learn source", "Make a new skill from a folder, URL, notes, or this chat."),
    ("/refine", "Review this chat now and save the lessons to memory and skills."),
    ("/memory pending", "See memory writes waiting for your approval."),
    ("/tools list", "Show tools. <b>disable</b> and <b>enable</b> turn them off and on."),
    ("hermes mcp", "Add and manage MCP servers. <b>/reload-mcp</b> picks up changes."),
    ("/plugins", "List installed plugins and their status."),
], keyw=0.32)
y = callout(c, X[2], y, "Where things live", [
    mono("~/.hermes/config.yaml") + ": settings. Edit with <b>hermes config edit</b>.",
    mono("~/.hermes/.env") + ": API keys, tokens, and other secrets.",
    mono("~/.hermes/SOUL.md") + ": the agent's identity and tone.",
    mono("~/.hermes/memories/") + ": MEMORY.md and USER.md, what Hermes remembers.",
    mono("~/.hermes/skills/") + ": installed skills.",
    mono("AGENTS.md") + ": instructions for one project, in its folder.",
])
check(y, "p2c3")
footer(c)
c.showPage()
c.save()
print("ok")
