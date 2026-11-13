"""Check the proposed design tokens: WCAG contrast, density and slide-manifest rules.

Standard library only. Run from the repo root:
    python3 -I Workshop-Team/design/check_tokens.py
    python3 -I Workshop-Team/design/check_tokens.py --slides Workshop-Team/design/slide-manifest.json \
        --agenda Workshop-Team/teaching/agenda.json

--slides  JSON list of slide objects (see slide-manifest.json for the fields).
--agenda  optional teaching agenda; slide numbers, titles and minutes must match.
Exit code is non-zero on any failure.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS = json.loads((HERE / 'tokens.json').read_text())
COLOR = {k: v['hex'] for k, v in TOKENS['color'].items()}
D = TOKENS['density']
CONTEXTS = {k: v for k, v in TOKENS['contexts'].items() if not k.startswith('_')}


def luminance(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(verbose=True):
    fails = []
    for fg, bg, need in TOKENS['required_pairs']:
        r = ratio(COLOR[fg], COLOR[bg])
        if verbose:
            print(f'{"ok " if r >= need else "FAIL"} {fg:13} on {bg:11} {r:5.2f}:1 (need {need})')
        if r < need:
            fails.append(f'contrast {fg} on {bg}')
    for pair in TOKENS['forbidden_pairs']:
        if verbose:
            r = ratio(COLOR[pair['fg']], COLOR[pair['bg']])
            print(f'ban  {pair["fg"]:13} on {pair["bg"]:11} {r:5.2f}:1  {pair["why"]}')
    return fails


def words(text):
    return len(text.split())


def check_blocks(s, bad):
    """Command/prompt blocks: [{"context": "bash", "text": "...", "size": 20}]."""
    for block in s.get('blocks', []):
        ctx = block.get('context')
        if ctx not in CONTEXTS:
            bad(f'block context {ctx!r} unknown; use one of {sorted(CONTEXTS)}')
            continue
        if not CONTEXTS[ctx]['slides']:
            bad(f'context {ctx!r} is workbook-only (e.g. admin prework); keep it off slides')
        text = block.get('text', '')
        if ctx == 'prompt':
            limit = D['demo_prompt_full_max_words'] if block.get('full_prompt') else D['demo_prompt_excerpt_max_words']
            if words(text) > limit:
                bad(f'prompt {words(text)} words > {limit}; excerpt it, full text in workbook')
            continue
        lines = text.splitlines()
        if len(lines) > D['code_max_lines']:
            bad(f'{len(lines)} code lines > {D["code_max_lines"]}')
        size = block.get('size', 20)
        cap = D['code_max_chars_per_line'] if size >= 20 else D['code_floor_max_chars_per_line']
        if size < TOKENS['type']['scale']['code']['floor']:
            bad(f'code size {size} below floor')
        for ln in lines:
            if ln.lstrip().startswith(('$ ', 'PS>', '# ')):
                bad(f'prompt marker inside copyable text: {ln[:30]}')
            if len(ln) > cap:
                bad(f'code line {len(ln)} chars > {cap} at {size}pt: {ln[:40]}')


def check_slides(path, agenda_path=None):
    fails = []
    slides = json.loads(Path(path).read_text())
    seen_lab = False
    for n, s in enumerate(slides, 1):
        kind, title = s.get('kind'), s.get('title', '')

        def bad(msg):
            fails.append(f'slide {n} ({kind}) "{title[:40]}": {msg}')
        if len(title) > D['title_max_chars']:
            bad(f'title {len(title)} chars > {D["title_max_chars"]}')
        pts = s.get('points', [])
        if kind == 'concept':
            if len(pts) > D['concept_max_points']:
                bad(f'{len(pts)} points > {D["concept_max_points"]}; use kind "terms" for short lists')
            if sum(map(words, pts)) > D['concept_body_max_words']:
                bad('body over word budget')
            for p in pts:
                if words(p) > D['concept_point_max_words']:
                    bad(f'point over {D["concept_point_max_words"]} words: {p[:40]}')
        elif kind == 'terms':
            if len(pts) > D['terms_max_items']:
                bad(f'{len(pts)} items > {D["terms_max_items"]}')
            for p in pts:
                if words(p) > D['terms_item_max_words']:
                    bad(f'item over {D["terms_item_max_words"]} words: {p[:40]}')
        elif kind == 'statement':
            if words(s.get('statement', '')) > D['statement_max_words']:
                bad('statement too long')
        elif kind == 'route':
            if len(s.get('routes', [])) != D['routes']:
                bad(f'route slide must show all {D["routes"]} routes with equal weight')
        elif kind == 'lab':
            seen_lab = True
            steps = s.get('steps', [])
            if len(steps) > D['lab_max_steps']:
                bad(f'{len(steps)} steps > {D["lab_max_steps"]}')
            for st in steps:
                if words(st) > D['lab_step_max_words']:
                    bad(f'step over {D["lab_step_max_words"]} words: {st[:40]}')
            if words(s.get('done_when', '')) > D['lab_done_when_max_words']:
                bad('done-when too long')
            for field in ('minutes', 'elapsed', 'done_when', 'fallback', 'workbook_ref', 'provenance'):
                if not s.get(field):
                    bad(f'lab slide missing {field}')
            phases = s.get('phases', [])
            if phases and sum(p[1] for p in phases) != s.get('minutes'):
                bad(f'phase minutes {sum(p[1] for p in phases)} != slide minutes {s.get("minutes")}')
        elif kind == 'reveal':
            if not seen_lab:
                bad('answer reveal appears before any lab work slide')
            items = s.get('items', [])
            if len(items) > D['reveal_max_items']:
                bad(f'{len(items)} reveal items > {D["reveal_max_items"]}')
            for it in items:
                if words(it) > D['reveal_item_max_words']:
                    bad(f'reveal item over {D["reveal_item_max_words"]} words: {it[:40]}')
        check_blocks(s, bad)
    if agenda_path:
        agenda = json.loads(Path(agenda_path).read_text())
        if len(agenda) != len(slides):
            fails.append(f'agenda has {len(agenda)} rows, manifest {len(slides)} slides')
        for a, s in zip(agenda, slides):
            if a['slide'] != s.get('slide') or a['minutes'] != s.get('minutes') or a['title'] != s.get('title'):
                fails.append(f'agenda/manifest mismatch at slide {a["slide"]}: {a["title"]!r} {a["minutes"]} vs {s.get("title")!r} {s.get("minutes")}')
        total = sum(s.get('minutes', 0) for s in slides)
        if total != 120:
            fails.append(f'manifest minutes total {total}, expected 120')
        clock = 0
        for s in slides:
            want = f'{clock:02d}–{clock + s["minutes"]:02d}'
            if s.get('elapsed') != want:
                fails.append(f'slide {s["slide"]} elapsed {s.get("elapsed")!r}, computed {want}')
            clock += s['minutes']
    for f in fails:
        print('FAIL', f)
    return fails


if __name__ == '__main__':
    args = sys.argv
    failures = check_contrast(verbose='--slides' not in args)
    if '--slides' in args:
        agenda = args[args.index('--agenda') + 1] if '--agenda' in args else None
        failures += check_slides(args[args.index('--slides') + 1], agenda)
    print('PASS' if not failures else f'{len(failures)} failure(s)')
    sys.exit(1 if failures else 0)
