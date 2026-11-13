"""Prepare reviewed-source slide data only. Does not build or render a deck."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
TEAM = HERE.parent
agenda = json.loads((TEAM / 'teaching/agenda.json').read_text())
narrative = (TEAM / 'teaching/SLIDE-NARRATIVE.md').read_text()
workbook = (TEAM / 'teaching/PARTICIPANT-WORKBOOK.md').read_text()
sections = re.split(r'^## Slide (\d+) \| (\d+)–(\d+) \| (.+)\n', narrative, flags=re.M)
assert len(sections) == 1 + 5 * len(agenda)
layouts = {
    1: 'title', 7: 'lab', 9: 'lab', 10: 'checkpoint', 12: 'break',
    14: 'lab', 15: 'checkpoint', 18: 'lab', 19: 'checkpoint', 21: 'close',
}
lab_fields = {
    7: ('Readiness, elapsed 20–28',
        ['Locate the disposable kit and inspect Python availability.',
         'Inspect the approved agent and permissions, or choose review.',
         'Switch unresolved setups to review by minute 25.'],
        'Everyone proceeds on a live, local-script, or paper review route.',
        'Use printed inputs and answer-key specimens; no account or runtime needed.'),
    9: ('Lab 1 — turn a policy into a usable checklist, elapsed 28–44',
        ['Read labs/offboarding-policy.txt and predict the deadline.',
         'Draft or repair the checklist; take no live action.',
         'Trace every requirement to a policy line.'],
        'Four systems, roles, verification, evidence, correct deadline and missing decisions.',
        'Repair specimen A using the printed policy; write one corrected row.'),
    14: ('Lab 2 — write a script you can check, elapsed 53–82',
         ['Predict rows, then inspect the proposed script.',
          'Run only reviewed local code; preserve the input.',
          'Compare IDs and reasons; review boundary checks.'],
         'E06/E07/E10/E11 match exact reasons; explain boundary exclusions.',
         'Hand-flag all 12 rows; repair specimen B and review the inert snippet.'),
    18: ('Lab 3 — build a local review report, elapsed 87–110',
         ['Approve the small plan and inspect proposed code.',
          'Build local HTML from the checked CSV.',
          'Trace source values; test empty input and escaped text.'],
         'Four events, three categories, source match and safe text rendering.',
         'Sketch the report and correct specimen C against the printed CSV.'),
}
checkpoint_rows = {
    10: ['WORKING: Trace all four systems and deadline to policy.',
         'PARTIAL: Mark unsupported retention or ownership claims as decisions needed.',
         'BLOCKED: Repair specimen A using policy and record review completion.'],
    15: ['WORKING: Explain exact IDs, reasons and a boundary exclusion.',
         'PARTIAL: Trace the first mismatch to a source row.',
         'BLOCKED: Hand-check specimen B; record review rather than execution.'],
    19: ['WORKING: Trace four events, three categories and escaped source text.',
         'PARTIAL: Name the failing check and preserve the evidence.',
         'BLOCKED: Annotate specimen C and describe unexecuted checks.'],
}
concept_overrides = {
    8: ['Read offboarding-policy.txt; draft only.', 'Preserve deadlines.', 'Mark decisions needed.'],
    4: ['Name the outcome and input.', 'Limit allowed actions.', 'Choose an acceptance check.'],
    5: ['Read before run; use a safe environment.',
        'Protect data; narrow access.', 'Verify against evidence.'],
    13: ['Success only; outside 07:00–18:59 UTC.',
         'Success outside the US training baseline.',
         'Success after ≥3 same-user failures within ten minutes.'],
    20: ['Low stakes and repetitive.', 'Know how to check the result.',
         'Keep the prompts and checks.'],
}
prompt_blocks = re.findall(r'```text\n(.*?)```', workbook, flags=re.S)
def find_prompt(prefix):
    return next(p for p in prompt_blocks if p.startswith(prefix))
prompts = {8: [find_prompt('Read only labs/offboarding'), find_prompt('Find each deadline')],
           13: [find_prompt('Read labs/signins')],
           16: [find_prompt('Read these source')],
           17: [find_prompt('Plan a tiny'), find_prompt('Implement work/build_report')]}
prompts[7] = [next(p for p in prompt_blocks if p.lstrip().startswith('/status')),
              find_prompt('Reply with READY')]
readiness = re.search(r'^## R0 —.*?(?=^## L1 —)', workbook, flags=re.M|re.S).group(0)
design = json.loads((TEAM/'design/slide-manifest.json').read_text())
projection = json.loads((TEAM/'teaching/projection-content.json').read_text())
slides = []
elapsed = 0
for i, entry in enumerate(agenda):
    number, start, end, title, body = sections[1 + i * 5: 6 + i * 5]
    number, start, end = int(number), int(start), int(end)
    assert number == entry['slide'] and title == entry['title']
    assert start == elapsed and end - start == entry['minutes'] > 0
    elapsed = end
    screen = re.search(r'\*\*Screen:\*\* (.*?)\n', body).group(1)
    notes = body.split('**Notes:** ', 1)[1].strip()
    if number == 17:
        notes = notes.replace('in this proposed core', 'in the approved core')
        notes = notes.replace('If lead selects scanner, this block and its checks must be rewritten before final build. ', '')
    slide = dict(id=f'S{number:02}', slide=number, title=title,
                 kind=layouts.get(number, 'concept'), minutes=entry['minutes'],
                 start_minute=start, end_minute=end,
                 elapsed=f'{start:02}–{end:02}',
                 activity=entry['activity'], source_screen=screen,
                 notes=notes, narrative_ref=f'teaching/SLIDE-NARRATIVE.md#slide-{number}',
                 workbook_ref='teaching/PARTICIPANT-WORKBOOK.md',
                 source_mapping=re.findall(r'\[\[([^]]+)\]\]', body),
                 branding=number in (1, 21),
                 provenance='SYNTHETIC' if 7 <= number <= 19 and number != 12 else None)
    if slide['kind'] == 'concept':
        slide['points'] = concept_overrides.get(number, screen.split(' · '))
    if number in lab_fields:
        ref, steps, done, fallback = lab_fields[number]
        slide.update(workbook_section=ref, steps=steps, done_when=done, fallback=fallback)
    if number in checkpoint_rows:
        slide['rows'] = checkpoint_rows[number]
        slide['evidence_reveal'] = screen
    if number in prompts:
        slide['full_workbook_prompts'] = prompts[number]
    slide.update(design[i])
    for override in projection:
        if override.get('core_slide') == number:
            slide.update({k:v for k,v in override.items() if k not in {'notes', 'id'}})
            slide['notes'] += '\n\nFACILITATION: ' + override.get('notes', '')
    slide['id'] = f'C{number:02}'
    slide['hidden'] = False
    if number in (8, 9, 10):
        slide['provenance'] = 'FICTIONAL POLICY'
    if number == 9:
        slide['done_when'] = 'Four systems; correct deadline; evidence; decisions named.'
    if number == 14:
        slide['done_when'] = 'Exact IDs and reasons; unchanged input; boundary explained.'
        slide['steps'][2] = 'Run labs/check_triage.py; compare exact IDs, source values and reasons.'
    if number == 18:
        slide['done_when'] = 'Four events; three categories; safe text; source match.'
        slide['steps'][2] = 'Build, then run the workbook L3 command.'
        slide['steps'][3] = 'Check counts, source values, empty input and escaped text.'
    if number == 8:
        slide['points'] = ['Read labs/offboarding-policy.txt; draft only.',
                           'Preserve deadlines.', 'Mark decisions needed.']
    if number == 7:
        slide['routes'] = ['live', 'script', 'paper']
        slide['provenance'] = 'SETUP'
        slide['notes'] += '\n\nCURRENT WORKBOOK R0 — FULL READINESS REFERENCE\n' + readiness
    slides.append(slide)
assert elapsed == 120 and slides[6]['minutes'] == 8
assert slides[11]['minutes'] == 5 and slides[-1]['minutes'] == 5
sources = ['teaching/agenda.json', 'teaching/SLIDE-NARRATIVE.md',
           'teaching/PARTICIPANT-WORKBOOK.md', 'teaching/verification.json',
           'linux/PROPOSAL.md', 'linux/SETUP-PREFLIGHT.md',
           'linux/COMMAND-VERIFICATION.md', 'linux/VERIFICATION.md',
           'design/PROPOSAL.md', 'design/tokens.json', 'COORDINATOR-NOTES.md',
           'teaching/projection-content.json', 'design/slide-manifest.json',
           'teaching/PEER-REVIEW.md', 'linux/PEER-REVIEW.md', 'design/PEER-REVIEW.md']
for support in projection:
    if 'parent_slide' in support:
        s = dict(support, hidden=True)
        s['blocks'] = ([{'context':'bash','text':s['code']}] if s.get('code') else [])
        s['elapsed'] = 'support ' + '–'.join(map(str, s['display_window']))
        if s['id']=='S07A':
            s['provenance']='SETUP'
        slides.append(s)
metadata = dict(schema_version=1, status='frozen-after-three-peer-reviews',
                final_build_authorized=True, duration_minutes=elapsed,
                core_slide_count=21, hidden_support_count=4, slide_count=len(slides),
                source_hashes={p: hashlib.sha256((TEAM/p).read_bytes()).hexdigest() for p in sources},
                agenda_authority='teaching/agenda.json',
                renderer='NOT RUN: native PowerPoint export awaiting user approval; canceled request; do not retry',
                rasterizer='pypdfium2',
                source_status='Lead execution evidence is recorded separately in deliverables/verification.json and integration/extracted-kit-verification.json; this generator does not run lab checks.')
(HERE/'slides.json').write_text(json.dumps(slides, indent=2, ensure_ascii=False) + '\n')
(HERE/'manifest.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n')
print(f'Prepared 21 core + 4 hidden support slides, {elapsed} minutes; no deck built by this script.')
