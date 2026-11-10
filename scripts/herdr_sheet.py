"""Generate herdr-Cheat-Sheet.pdf (2-page landscape reference).

Needs Python 3.10+ and reportlab:
    python3 -m venv .venv && .venv/bin/pip install reportlab
    .venv/bin/python scripts/herdr_sheet.py herdr-Cheat-Sheet.pdf

Prints OVERFLOW if a column runs past the footer.
"""
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

OUT = sys.argv[1]
W, H = landscape(letter)
DARK = HexColor("#1F2023")
ORANGE = HexColor("#E8590C")
ROW = HexColor("#F1F2F4")
LINE = HexColor("#C9CCD1")
TEXT = HexColor("#4A4D52")
INK = HexColor("#111111")

M = 32
GAP = 18
COLW = (W - 2 * M - 2 * GAP) / 3
TOP = H - 66

key_style = ParagraphStyle("k", fontName="Courier-Bold", fontSize=8.6, leading=10.2, textColor=INK)
desc_style = ParagraphStyle("d", fontName="Helvetica", fontSize=8.3, leading=10.2, textColor=TEXT)
note_style = ParagraphStyle("n", fontName="Helvetica", fontSize=8.1, leading=10, textColor=INK)
call_style = ParagraphStyle("c", fontName="Helvetica", fontSize=8.3, leading=10.4, textColor=INK)


def mono(s):
    return f'<font name="Courier-Bold">{s}</font>'


def header(c, sub, page):
    c.setFillColor(DARK)
    c.rect(0, H - 50, W, 50, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(32, H - 50, 8, 50, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(54, H - 33, "herdr Cheat Sheet")
    c.setFillColor(HexColor("#A9ACB2"))
    c.setFont("Helvetica", 10)
    c.drawRightString(W - M, H - 31, f"{sub}   ·   page {page} of 2")


def footer(c):
    c.setFillColor(HexColor("#6B6E73"))
    c.setFont("Helvetica", 7)
    c.drawString(M, 18, "Checked against herdr 0.9.5 and herdr.dev/tui/docs, November 2026. "
                 "Keys change between releases: press prefix+? inside herdr to see the current list.")
    c.drawRightString(W - M, 18, "Cite Talk 2026 · github.com/OCDEkr/Cite-Talk-2026")


def section(c, x, y, num, title, rows, keyw=0.36, note=None):
    c.setFillColor(DARK)
    c.rect(x, y - 21, COLW, 21, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ORANGE)
    c.drawString(x + 7, y - 15, num)
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawString(x + 27, y - 15, title)
    y -= 21
    top = y
    kw = COLW * keyw
    dw = COLW - kw - 6
    for i, (k, d) in enumerate(rows):
        kp = Paragraph(k, key_style)
        dp = Paragraph(d, desc_style)
        _, kh = kp.wrap(kw - 10, 1000)
        _, dh = dp.wrap(dw, 1000)
        h = max(kh, dh) + 7
        if i % 2 == 1:
            c.setFillColor(ROW)
            c.rect(x, y - h, COLW, h, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x, y - h, x + COLW, y - h)
        kp.drawOn(c, x + 6, y - 4 - kh)
        dp.drawOn(c, x + kw, y - 4 - dh)
        y -= h
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(x, y, x, top)
    c.line(x + COLW, y, x + COLW, top)
    if note:
        p = Paragraph(note, note_style)
        _, nh = p.wrap(COLW, 1000)
        p.drawOn(c, x, y - 4 - nh)
        y -= nh + 4
    return y - 14


def callout(c, x, y, title, lines):
    paras = [Paragraph(l, call_style) for l in lines]
    hs = [p.wrap(COLW - 18, 1000)[1] for p in paras]
    h = 22 + sum(hs) + 8
    c.setFillColor(ROW)
    c.rect(x, y - h, COLW, h, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(x, y - h, 3, h, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(x + 12, y - 14, title)
    yy = y - 20
    for p, ph in zip(paras, hs):
        p.drawOn(c, x + 12, yy - ph)
        yy -= ph
    return y - h - 14


def check(y, label):
    if y < 30:
        print(f"OVERFLOW in {label}: y={y:.1f}")


X = [M, M + COLW + GAP, M + 2 * (COLW + GAP)]
c = canvas.Canvas(OUT, pagesize=landscape(letter))
c.setTitle("herdr Cheat Sheet")
c.setAuthor("Cite Talk 2026")

# ---------------- Page 1 ----------------
header(c, "Keys, panes, tabs, and workspaces", 1)

y = TOP
y = section(c, X[0], y, "01", "Start and stop (in your terminal)", [
    ("herdr", "Start herdr, or reattach to the session already running. Run it from your project folder."),
    ("herdr --session work", "Use a separate named session. Most people only need the default one."),
    ("herdr session list", "List sessions. <b>session stop</b> and <b>session delete</b> clean them up."),
    ("herdr status", "Client and server status, including versions."),
    ("herdr --remote host", "Attach to herdr on another machine over SSH."),
    ("herdr integration install claude", "Lets herdr resume Claude Code conversations after a server restart."),
    ("herdr server stop", "Stop the server and every process in its panes, agents included."),
    ("herdr update", "Install the latest version. Homebrew installs update through brew instead."),
])
y = section(c, X[0], y, "02", "The prefix key", [
    ("ctrl+b", "The prefix. Press it, let go, then press the action key. <b>prefix+c</b> means ctrl+b, then c."),
    ("prefix+?", "Show every active binding. Press / to filter the list."),
    ("prefix+q", "Detach. Everything keeps running. Run <b>herdr</b> to come back."),
    ("prefix+s", "Open settings."),
    ("prefix+shift+r", "Reload config.toml after you edit it."),
    ("prefix+o", "Jump to the pane behind the latest notification."),
], note="You can skip the keys entirely. Click to focus, drag borders to resize, right-click for menus, drag to select and copy.")
check(y, "p1c1")

y = TOP
y = section(c, X[1], y, "03", "Panes", [
    ("prefix+v", "Split right."),
    ("prefix+minus", "Split down."),
    ("prefix+h/j/k/l", "Move focus left, down, up, or right."),
    ("prefix+tab", "Cycle to the next pane. Add shift to go back."),
    ("prefix+shift+ h/j/k/l", "Swap the pane with its neighbor in that direction."),
    ("prefix+z", "Zoom the pane to fill the tab. Press again to restore the layout."),
    ("prefix+r", "Resize mode: size the pane from the keyboard."),
    ("prefix+x", "Close the pane."),
    ("prefix+shift+p", "Rename the pane."),
    ("prefix+e", "Open the pane's scrollback in your editor."),
    ("prefix+[", "Copy mode. See section 08."),
])
y = section(c, X[1], y, "04", "Tabs", [
    ("prefix+c", "New tab. herdr asks for a name first."),
    ("prefix+n / p", "Next or previous tab."),
    ("prefix+1..9", "Jump to a tab by number."),
    ("prefix+shift+t", "Rename the tab."),
    ("prefix+shift+x", "Close the tab."),
])
check(y, "p1c2")

y = TOP
y = section(c, X[2], y, "05", "Workspaces and the sidebar", [
    ("prefix+w", "Workspace navigation. Up and Down change workspace, h/j/k/l move between panes, Esc leaves."),
    ("prefix+g", "Goto picker: every agent and terminal, grouped by workspace. See section 07."),
    ("prefix+shift+n", "New workspace."),
    ("prefix+shift+g", "New workspace on a new git worktree, a separate checkout of the repo."),
    ("prefix+shift+w", "Rename the workspace."),
    ("prefix+shift+d", "Close the workspace. herdr asks first."),
    ("prefix+b", "Show or hide the sidebar."),
])
y = callout(c, X[2], y, "How herdr is organized", [
    "<b>Session</b>: the background server. Panes live here and survive closing the terminal window.",
    "<b>Workspace</b>: one per project or task. The sidebar sums up the agents inside it.",
    "<b>Tab</b>: a layout inside a workspace, such as agents, logs, or server.",
    "<b>Pane</b>: a real terminal. Split it right or down.",
    "<b>Agent</b>: Claude Code or another coding tool that herdr spots running in a pane.",
])
y = callout(c, X[2], y, "Habits that save you", [
    "Give each repo its own workspace, and name it.",
    "Detach with <b>prefix+q</b> instead of closing things. Agents keep working while you're away.",
    "Watch the sidebar for <b>blocked</b> agents. They are waiting on you.",
    "Running a second agent on the same repo? Give it its own worktree so the two don't edit the same files.",
])
check(y, "p1c3")
footer(c)
c.showPage()

# ---------------- Page 2 ----------------
header(c, "Agents, copy mode, scripting, and config", 2)

y = TOP
y = section(c, X[0], y, "06", "Agent states in the sidebar", [
    ("working", "Busy on a task."),
    ("blocked", "Stopped at an approval or a question. Go read it and answer."),
    ("done", "Finished, and you haven't looked yet."),
    ("idle", "At its prompt and ready for the next task."),
    ("unknown", "herdr sees an agent but can't tell its state. Don't assume it finished."),
], keyw=0.26, note="herdr recognizes Claude Code, Codex, Gemini, Cursor, Copilot, OpenCode, and others. "
   "State looks wrong? Run " + mono("herdr agent explain &lt;pane&gt;") + ".")
y = section(c, X[0], y, "07", "Goto picker (prefix+g)", [
    ("/", "Search names, agent kinds, tabs, branches, and paths."),
    ("j/k", "Move up and down the list. Arrow keys work too."),
    ("Left / Right", "Jump to the previous or next workspace."),
    ("b w i d", "Show only blocked, working, idle, or done agents."),
    ("a", "Show all terminals again."),
    ("Enter", "Go to the selected pane."),
    ("Esc", "Close the picker."),
], keyw=0.26)
y = callout(c, X[0], y, "Where things live", [
    mono("~/.config/herdr/config.toml") + ": settings and keys.",
    mono("~/.config/herdr/herdr.log") + ": logs, next to the client and server logs.",
    mono("~/.herdr/worktrees") + ": where new worktrees go.",
    mono("herdr.dev/tui/docs") + ": full documentation.",
])
check(y, "p2c1")

y = TOP
y = section(c, X[1], y, "08", "Copy mode (prefix+[)", [
    ("h/j/k/l", "Move the cursor. w, b, and e move by word."),
    ("PageUp / Down", "Scroll a page. ctrl+u and ctrl+d scroll half a page."),
    ("/ or ?", "Search forward or back. n and N repeat the search."),
    ("v or Space", "Start a selection."),
    ("y or Enter", "Copy the selection and leave."),
    ("q or Esc", "Leave without copying."),
], keyw=0.32, note="The pane keeps running while you're in copy mode. Dragging with the mouse copies without entering it.")
y = section(c, X[1], y, "09", "Configure", [
    ("~/.config/herdr/ config.toml", "Your settings file. herdr runs fine without one."),
    ("herdr --default-config", "Print every option with comments. Copy the lines you want."),
    ('prefix = "ctrl+a"', "Change the prefix. Goes under <b>[keys]</b>. Every binding can change."),
    ('name = "dracula"', "Pick a theme under <b>[theme]</b>: catppuccin, tokyo-night, nord, gruvbox, and more."),
    ("herdr config check", "Check config.toml for mistakes."),
    ("herdr server reload-config", "Apply your edits to the running server."),
    ("herdr config reset-keys", "Back up config.toml and remove your custom keys."),
], keyw=0.42)
check(y, "p2c2")

y = TOP
y = section(c, X[2], y, "10", "Drive herdr from the command line", [
    ("herdr agent list", "Every agent and its state."),
    ("herdr pane split --current --direction right --no-focus", "Open a pane beside this one. Focus stays where it is."),
    ("herdr agent start rev --kind claude --pane w1:p2", "Start Claude Code in pane w1:p2 and name it rev."),
    ('herdr agent prompt rev "review the diff" --wait', "Send rev a prompt and wait until it finishes or needs you."),
    ("herdr agent wait rev --until blocked", "Wait until rev needs your input."),
    ("herdr agent read rev --lines 120", "Read rev's recent output."),
    ('herdr pane run w1:p2 "npm test"', "Run a command in another pane."),
    ("herdr worktree create --branch fix", "New git worktree with a workspace of its own."),
], keyw=0.5, note="These work from inside a herdr pane and reply in JSON. Pane IDs look like w1:p2; "
   "get them from " + mono("herdr pane list") + ".")
y = callout(c, X[2], y, "Be careful", [
    "<b>herdr server stop</b> and closing a workspace end every process in those panes.",
    "herdr refuses to launch inside one of its own panes. Detach first.",
    "Running tmux inside herdr? Both use ctrl+b, so change one prefix.",
    "A blocked agent is asking permission. Read what it wants before you approve.",
])
check(y, "p2c3")
footer(c)
c.showPage()
c.save()
print("ok")
