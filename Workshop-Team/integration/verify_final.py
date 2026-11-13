"""Structural PPTX and clean-copy local checks. No native export or GUI."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pptx import Presentation

HERE=Path(__file__).resolve().parent
TEAM=HERE.parent
OUT=TEAM/'deliverables'
DATA=json.loads((HERE/'slides.json').read_text())
evidence=[]

def run(args, expected=0, cwd=None):
    result=subprocess.run(list(map(str,args)),capture_output=True,text=True,timeout=40,cwd=cwd)
    evidence.append(dict(command=list(map(str,args)),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
    assert result.returncode==expected, result.stdout+result.stderr
    return result

def main():
    core=[s for s in DATA if not s.get('hidden')]
    (HERE/'core-slides.json').write_text(json.dumps(core,indent=2,ensure_ascii=False)+'\n')
    run([sys.executable,'-I',TEAM/'design/check_tokens.py','--slides',HERE/'core-slides.json','--agenda',TEAM/'teaching/agenda.json'])
    run([sys.executable,'-I',TEAM/'design/check_tokens.py','--slides',HERE/'slides.json'])
    p=Presentation(OUT/'CITE-AI-Cybersecurity-Workshop.pptx')
    assert len(p.slides)==25
    assert abs(p.slide_width/p.slide_height-16/9)<1e-6
    assert len(core)==21 and sum(s['minutes'] for s in core)==120
    visible=hidden=0
    shapes=text_blocks=0
    for s,d in zip(p.slides,DATA):
        assert s.shapes.title is not None and s.shapes.title.text.replace('\v',' ')==d['title']
        is_hidden=s._element.get('show')=='0'
        assert is_hidden==bool(d.get('hidden'))
        hidden+=is_hidden;visible+=not is_hidden
        notes=s.notes_slide.notes_text_frame.text
        assert d['id'] in notes and d['notes'] in notes
        for prompt in d.get('full_workbook_prompts',[]):
            assert prompt in notes
        for sh in s.shapes:
            shapes+=1
            assert sh.left>=0 and sh.top>=0
            assert sh.left+sh.width<=p.slide_width+2 and sh.top+sh.height<=p.slide_height+2, (d['id'],sh.name)
            if sh.shape_type==13:
                assert sh._element.nvPicPr.cNvPr.get('descr')
            if sh.has_text_frame and sh.text:
                text_blocks+=1
                assert sh.text_frame.word_wrap
                assert len(sh.text_frame.paragraphs)==1
                for para in sh.text_frame.paragraphs:
                    for r in para.runs:
                        if not r.text: continue
                        assert r.font.size and r.font.size.pt>=14,(d['id'],r.text)
                        if sh.name.startswith('body') or sh==s.shapes.title:
                            assert r.font.size.pt>=20
                        assert r._r.get_or_add_rPr().get('lang')=='en-US'
    assert visible==21 and hidden==4
    # Regression checks for coordinator-relayed final read-only peer findings.
    actual={d['id']:s for d,s in zip(DATA,p.slides)}
    text=lambda key:'\n'.join(sh.text for sh in actual[key].shapes if sh.has_text_frame)
    assert 'Mark decisions needed.' in text('C08') and 'Preserve deadlines.' in text('C08')
    assert 'Run labs/check_triage.py' in text('C14')
    assert 'Build, then run the workbook L3 command.' in text('C18')
    assert 'empty input and escaped text' in text('C18')
    assert 'SETUP' in text('C07') and 'SYNTHETIC' not in text('C07')
    ready_notes=actual['C07'].notes_slide.notes_text_frame.text
    assert '/status' in ready_notes and '/permissions' in ready_notes and 'Reply with READY.' in ready_notes
    for key in ['C10','C15','C19']:assert 'CHECK ·' in text(key)
    for key in ['C07','C09','C14','C18']:
        s=actual[key]
        cards=[sh for sh in s.shapes if sh.name.startswith('Lab card')]
        for sh in s.shapes:
            if sh.name.startswith('body-card'):
                assert any(card.left<sh.left and card.top<sh.top and
                           sh.left+sh.width<card.left+card.width and
                           sh.top+sh.height<card.top+card.height for card in cards)
            if sh.name.startswith('link'):
                assert sh.top+sh.height<=500*12700
                assert sh.left+sh.width<=912*12700
                assert sh.click_action.target_slide in [actual['S07A'],actual['S14A'],actual['S14B'],actual['S18A']]
    fit=json.loads((HERE/'text-fit-report.json').read_text())
    for item in fit:
        if item['role']=='link':
            assert item['text'] in '\n'.join(sh.text for sh in p.slides[item['slide']-1].shapes if sh.has_text_frame)
    assert 'Commands' in text('C14') and 'Checker help' in text('C14')
    for d,s in zip(DATA,p.slides):
        if d.get('hidden'):
            back=next(sh for sh in s.shapes if sh.has_text_frame and sh.text=='Return to lab')
            assert back.click_action.target_slide==actual[f'C{d["parent_slide"]:02}']
    run(['bash','-n',OUT/'participant/linux/preflight.sh'])
    run(['bash',OUT/'participant/linux/preflight.sh'],expected=2)
    # Fresh extraction rehearses the exact archive paths and reference commands.
    archive=OUT/'CITE-participant-kit.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted((OUT/'participant').rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts:
                z.write(f,Path('cite-workshop')/f.relative_to(OUT/'participant'))
    with zipfile.ZipFile(archive) as z:
        assert not any(any(word in name for word in ['PROPOSAL','PEER-REVIEW','PEER-QUESTIONS','CORRECTIONS','/design/']) for name in z.namelist())
    with tempfile.TemporaryDirectory(prefix='extracted-check-',dir=HERE) as tmp:
        with zipfile.ZipFile(archive) as z:z.extractall(tmp)
        root=Path(tmp)/'cite-workshop'
        teaching=root/'teaching'
        # Validator's development-only source dependencies are staged separately,
        # never shipped as attendee drafts. Its lab modules are from this archive.
        qa=Path(tmp)/'validator-source'
        shutil.copytree(TEAM/'teaching',qa/'teaching',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(TEAM/'design',qa/'design',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(teaching/'labs',qa/'teaching/labs',dirs_exist_ok=True)
        run([sys.executable,'-I',qa/'teaching/validate_teaching.py'])
        copied_report=json.loads((qa/'teaching/verification.json').read_text())
        (HERE/'extracted-kit-verification.json').write_text(json.dumps(copied_report,indent=2)+'\n')
        fixture=teaching/'labs/signins.csv'
        before=hashlib.sha256(fixture.read_bytes()).hexdigest()
        (teaching/'work').mkdir(exist_ok=True)
        run([sys.executable,'labs/reference_triage.py','labs/signins.csv','work/reference-events.csv'],cwd=teaching)
        run([sys.executable,'labs/check_triage.py','work/reference-events.csv'],cwd=teaching)
        run([sys.executable,'labs/reference_report.py','work/reference-events.csv','work/reference-review.html'],cwd=teaching)
        # Generated-success filename also works with the report fallback.
        shutil.copy2(teaching/'work/reference-events.csv',teaching/'work/flagged-events.csv')
        run([sys.executable,'labs/reference_report.py','work/flagged-events.csv','work/fallback-from-checked.html'],cwd=teaching)
        assert hashlib.sha256(fixture.read_bytes()).hexdigest()==before
        wrong=teaching/'work/wrong-header-only.csv'
        wrong.write_text('wrong_column\n')
        run([sys.executable,'labs/reference_report.py','work/wrong-header-only.csv','work/rejected.html'],expected=1,cwd=teaching)
        assert not (teaching/'work/rejected.html').exists()
        existing=(teaching/'work/reference-review.html').read_bytes()
        run([sys.executable,'labs/reference_report.py','work/reference-events.csv','work/reference-review.html'],expected=1,cwd=teaching)
        assert (teaching/'work/reference-review.html').read_bytes()==existing
    # HTML handout links must resolve inside the delivered package; no remote assets/scripts.
    links=[]
    class Inspect(HTMLParser):
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            assert tag not in {'script','iframe','object','embed'},tag
            assert not any(k.startswith('on') for k in attrs)
            assert 'src' not in attrs
            if 'href' in attrs:links.append((self.path,attrs['href']))
    parser=Inspect()
    for f in OUT.rglob('*.html'):
        parser.path=f;parser.feed(f.read_text())
    for f,target in links:
        if target.startswith(('http://','https://','mailto:','#')):continue
        local=(f.parent/target.split('#')[0]).resolve()
        assert local.is_relative_to(OUT) and local.exists(),(f,target)
    report=dict(status='PASS_STRUCTURAL_AND_LOCAL_REFERENCE_CHECKS',python=platform.python_version(),
                platform=platform.platform(),core_slides=visible,hidden_support_slides=hidden,
                computed_minutes=120,editable_text_blocks=text_blocks,shapes_checked=shapes,
                local_html_links_checked=len(links),
                packages={name:importlib.metadata.version(name) for name in ['python-pptx','Pillow','pypdf','pypdfium2']},
                executed=evidence,
                native_export={'status':'NOT RUN / awaiting user approval','reason':'Approval request canceled without authorization; not retried. No PDF generated.'},
                not_run=['Native PowerPoint PDF export','Native slide visual inspection / PDF raster',
                         'Browser rendering','Linux/WSL VM execution','Python 3.11 or 3.12 runtime rehearsal',
                         'Live agent login/inference','Participant-generated code','Classroom timing rehearsal'],
                final_peer_signoff='Coordinator-relayed design/teaching findings resolved; regression checks PASS. Native visual review NOT RUN.')
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'VERIFICATION.md').write_text('''# Verification report

Structural and local reference checks: **PASS**. Coordinator-relayed final design/teaching findings resolved and covered by regression checks. Lead signs off the editable PPTX and packet within the limitations below.

- 21 visible timed core slides, four hidden zero-time support slides, exactly 120 computed minutes.
- Editable single-block text, real title placeholders, notes/full prompts, shape bounds, font floors, en-US language and image alt text checked in actual PPTX. Internal Help/Return links are authored; click behavior is not GUI-tested.
- Design density/contrast and agenda lint passed. Font-based fit checks passed; these are measurements, not visual review.
- Actual participant ZIP extracted into a fresh directory; reference triage/checker/report commands passed with expected rows. Wrong-header-only input rejected without output; existing output preserved; fixture hash unchanged.
- Teacher validator ran in a separate source staging copy using the extracted archive's lab modules: 25 local checks, ten CLI checks, 21 matching timed slides, four bounded support views, design lint PASS. Reference CLIs also ran directly from the extracted attendee kit. Detailed evidence is in `../integration/extracted-kit-verification.json` and local commands in `verification.json`.
- Regressions checked: complete C08 instructions; current R0 READY/status/permissions in C07 notes; explicit C14 checker and C18 workbook L3 run instruction/report checks; padded DONE/STUCK cards; semantic Help links clear of footer and inside the 912-point content edge; CHECK labels on reveals; SETUP provenance; correct per-slide link metrics. Participant ZIP excludes internal proposals/reviews/questions/corrections and design discussion.
- Linux preflight syntax passed; macOS runtime correctly returned SKIP/exit 2. No Linux success is claimed.
- Offline HTML handouts contain no scripts/remote assets; local links resolve inside this package. Print CSS is supplied; browser/print appearance is not visually tested.

**Native export: NOT RUN / awaiting user approval.** The PowerPoint approval request was canceled unanswered. It was not retried and no alternative route was used. No PDF export, slide raster, contact sheet or native visual sign-off is claimed. No separately drawn PDF is supplied.

Other NOT RUN: Linux/WSL VM and Python-floor rehearsal, native Windows, live model access/permissions, participant-generated code, browser rendering and classroom pacing. The 120-minute total is arithmetic, not a timed live rehearsal. Runtime references executed on macOS/Python 3.14.9.

Known scope limits: reference triage uses a fixed synthetic schema and arbitrary US/UTC rules; it does not detect compromise or impossible travel. The static report is an application exercise, not a network scanner. Generated participant code must be reviewed/tested separately. Final read-only specialist findings were relayed by the coordinator and resolved; no native visual sign-off is claimed.
''')
    # Write handout HTML for the new verification report without recopying source material.
    spec=importlib.util.spec_from_file_location('package_workshop',HERE/'package_workshop.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.render_md(OUT/'VERIFICATION.md')
    for f in [OUT/'README.md',OUT/'README.html']:
        assert f.exists()
    (OUT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(OUT))+'\n' for f in sorted(OUT.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.txt'))
    print(f'PASS: {visible} core + {hidden} hidden, 120 minutes, {text_blocks} text blocks; curated extracted kit, regression checks and local links passed. Native export NOT RUN.')

if __name__=='__main__':main()
