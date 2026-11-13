"""Shared layout for the two-page landscape cheat sheets.

Each sheet script calls start(title, footer, out_path), then draws with
header / section / callout / footer, and finally c.showPage() and c.save().
"""
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

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
    c.drawString(54, H - 33, TITLE)
    c.setFillColor(HexColor("#A9ACB2"))
    c.setFont("Helvetica", 10)
    c.drawRightString(W - M, H - 31, f"{sub}   ·   page {page} of 2")


def footer(c):
    c.setFillColor(HexColor("#6B6E73"))
    c.setFont("Helvetica", 7)
    c.drawString(M, 18, FOOTER)
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



TITLE = ""
FOOTER = ""
X = [M, M + COLW + GAP, M + 2 * (COLW + GAP)]


def start(title, footer_text, out):
    global TITLE, FOOTER
    TITLE, FOOTER = title, footer_text
    from reportlab.pdfgen import canvas as _cv
    cv = _cv.Canvas(out, pagesize=landscape(letter))
    cv.setTitle(title)
    cv.setAuthor("Cite Talk 2026")
    return cv
