"""Package local Markdown/HTML handouts. No external services or renderer."""
from pathlib import Path
import html
import json
import re
import shutil
import zipfile

HERE=Path(__file__).resolve().parent
TEAM=HERE.parent
OUT=TEAM/'deliverables'
KIT=OUT/'participant'
CURRENT_DOC = None

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\[\[([^]]+)\]\]', lambda m: html.escape(m[1].split('/')[-1]), text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    def link(m):
        target=html.unescape(m[2])
        if re.match(r'(?i)^(javascript|data|file):', target):
            return m[1]
        if not re.match(r'(?i)^(https?://|mailto:|#)',target):
            local=(CURRENT_DOC.parent/target.split('#')[0]).resolve()
            if not local.is_relative_to(OUT) or not local.exists():
                return m[1] + ' (source reference)'
        if target.endswith('.md'):
            target=target[:-3]+'.html'
        return f'<a href="{html.escape(target,quote=True)}">{m[1]}</a>'
    return re.sub(r'\[([^]]+)\]\(([^)]+)\)',link,text)

def render_md(path):
    global CURRENT_DOC
    CURRENT_DOC=path
    text=path.read_text()
    text=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
    lines=text.splitlines(); body=[]; i=0; ids={}
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            lang=line[3:]; block=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i+=1
            body.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>')
        elif line.startswith('#'):
            level=len(line)-len(line.lstrip('#')); title=line[level:].strip()
            ident=re.sub(r'[^\w -]','',title.lower()).replace(' ','-')
            ids[ident]=ids.get(ident,0)+1
            ident += '' if ids[ident]==1 else '-'+str(ids[ident])
            body.append(f'<h{level} id="{ident}">{inline(title)}</h{level}>')
        elif line.startswith('|') and i+1<len(lines) and re.match(r'^\|[ :|-]+\|$',lines[i+1]):
            headers=line.strip('|').split('|'); i+=2; rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append(lines[i].strip('|').split('|')); i+=1
            body.append('<table><thead><tr>'+''.join('<th>'+inline(x.strip())+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x.strip())+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>')
            continue
        elif line.startswith('- '):
            items=[]
            while i<len(lines) and lines[i].startswith('- '):
                items.append('<li>'+inline(lines[i][2:])+'</li>'); i+=1
            body.append('<ul>'+''.join(items)+'</ul>'); continue
        elif line.strip():
            para=[line]
            while i+1<len(lines) and lines[i+1].strip() and not re.match(r'^(#|```|\||- )',lines[i+1]):
                i+=1; para.append(lines[i])
            body.append('<p>'+inline(' '.join(para))+'</p>')
        i+=1
    title=path.stem.replace('-',' ')
    style='''body{font:17px/1.55 Arial,sans-serif;color:#111;max-width:960px;margin:36px auto;padding:0 24px}h1,h2,h3{line-height:1.2;color:#155191}h2{margin-top:2em}a{color:#155191}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;border-left:3px solid #5a6270;padding:14px;font:14px/1.5 Consolas,monospace}code{font-family:Consolas,monospace}table{border-collapse:collapse;width:100%;font-size:15px}td,th{border:1px solid #5a6270;padding:8px;text-align:left;vertical-align:top}th{background:#eff4fa}li{margin:.4em 0}@media print{body{font-size:11pt;margin:0;max-width:none}pre{font-size:9pt;background:white}table{font-size:9pt}h2{break-after:avoid}tr,pre{break-inside:avoid}a{color:#111}a[href^="https"]:after{content:" (" attr(href) ")";font-size:8pt}}'''
    page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'"><title>{html.escape(title)}</title><style>{style}</style></head><body>'+ '\n'.join(body)+'</body></html>'
    path.with_suffix('.html').write_text(page)

def label_blocks(text, role):
    def label(m):
        lang,content=m[1],m[2]
        if lang=='bash':
            label='UBUNTU / WSL BASH · NORMAL USER · IN THE KIT COPY'
        elif lang=='powershell':
            label='WINDOWS POWERSHELL · PREWORK ONLY'
        elif lang=='csv':
            label='SYNTHETIC DATA · NOT AN INSTRUCTION'
        elif content.lstrip().startswith(('/status','/permissions')):
            label='INSIDE THE AGENT SESSION'
        elif role=='PARTICIPANT-WORKBOOK' and any(content.startswith(p) for p in ['Read only','Find each','Read labs/','Reply with READY','Plan a tiny','Implement work/']):
            label='PROMPT · PASTE INTO THE APPROVED AGENT'
        else:
            label='REVIEW TEXT · DO NOT EXECUTE AS A COMMAND'
        return f'**{label}**\n\n```{lang}\n{content}```'
    return re.sub(r'```(\w*)\n(.*?)```',label,text,flags=re.S)

def main():
    keep={'teaching': {'PARTICIPANT-WORKBOOK.md','NO-ACCOUNT-PACKET.md','ANSWER-KEY.md','AGENDA.md'},
          'linux': {'SETUP-PREFLIGHT.md','COMMAND-VERIFICATION.md','preflight.sh'}}
    # This directory is generated exclusively by this script. Remove stale internal
    # material from previous package iterations, preserving the source folders.
    if KIT.exists():
        for f in KIT.rglob('*'):
            if f.is_file():
                rel=f.relative_to(KIT)
                allowed=(len(rel.parts)>2 and rel.parts[:2]==('teaching','labs')) or (
                    len(rel.parts)==2 and rel.parts[0] in keep and
                    (rel.name in keep[rel.parts[0]] or (f.suffix=='.html' and f.with_suffix('.md').name in keep[rel.parts[0]])))
                if not allowed:f.unlink()
        for folder in sorted(KIT.rglob('*'),key=lambda p:len(p.parts),reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):folder.rmdir()
    for folder in keep:
        target=KIT/folder; target.mkdir(parents=True,exist_ok=True)
        for source in (TEAM/folder).iterdir():
            if source.is_file() and source.name in keep[folder]:
                shutil.copy2(source,target/source.name)
    shutil.copytree(TEAM/'teaching/labs',KIT/'teaching/labs',dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    workbook=KIT/'teaching/PARTICIPANT-WORKBOOK.md'
    text=workbook.read_text().replace('a supported Python 3 runtime','Python 3.11+ (supported workshop floor; Linux rehearsal target 3.12)')
    text=text.replace('this proposal has only tested the local host path','local reference tests have run on macOS only')
    text=text.replace('for these proposed exercises','for these exercises')
    text=text.replace('Final integration and sign-off remain with the lead.', 'Native PowerPoint rendering is NOT RUN; technical/platform limits are in the verification report.')
    # Portable standalone links replace vault-qualified references.
    text=re.sub(r'\[\[Workshop-Team/teaching/([^]]+)\]\]',r'[\1](\1.md)',text)
    for path in [workbook,KIT/'linux/SETUP-PREFLIGHT.md',KIT/'teaching/NO-ACCOUNT-PACKET.md']:
        content=text if path==workbook else path.read_text()
        content=re.sub(r'(?m)^status: .*$', 'status: integrated-workshop-edition',content)
        content=content.replace('Round 2. Print or save this single file before class.', 'Workshop edition. Print or save this single file before class.')
        path.write_text(label_blocks(content,path.stem))
    report=KIT/'teaching/labs/reference_report.py'
    content=report.read_text().replace("        with Path(sys.argv[2]).open('x', encoding='utf-8') as handle:\n            handle.write(render(rows))", "        content = render(rows)\n        with Path(sys.argv[2]).open('x', encoding='utf-8') as handle:\n            handle.write(content)")
    report.write_text(content)
    (KIT/'README.md').write_text('''# CITE participant kit

**Start here: [Participant workbook](teaching/PARTICIPANT-WORKBOOK.html).** Editable Markdown is beside the HTML. The workbook links the complete no-account packet for print/offline participation. No account, runtime, network or partner is needed for that review route once the packet is supplied.

For a live or local-script route, complete the [setup/preflight](linux/SETUP-PREFLIGHT.html) before class. Inside the approved disposable environment, the organizer places this extracted folder at `~/cite-workshop`, with `teaching/` and `linux/` as siblings. Work from `~/cite-workshop/teaching`, not the repository root. Use a fresh `work/` directory and new output names. A folder is not an isolation boundary.

Only purpose-created fictional policy and synthetic records are used. The exercises produce a checklist, checked log script and static local report. No scanner, server, production account change or plugin is required. Reasoning review and actual execution are recorded separately. Facilitator notes, build sources and team discussion are supplied separately from this participant ZIP.

Runtime/platform limits and native PowerPoint rendering status are in the facilitator's verification report. No native-rendered PDF is included.
''')
    facilitator=OUT/'facilitator'
    facilitator.mkdir(exist_ok=True)
    shutil.copy2(TEAM/'teaching/SOURCES-AND-VERIFICATION.md',facilitator/'TEACHING-SOURCES-AND-VERIFICATION.md')
    shutil.copy2(TEAM/'linux/VERIFICATION.md',facilitator/'LINUX-VERIFICATION.md')
    # Facilitator guide uses the actual final slide data, including full prompts.
    slides=json.loads((HERE/'slides.json').read_text())
    parts=['# Facilitator guide', '', '21 core slides total exactly 120 minutes. Four hidden support views add zero minutes.', '',
           'PowerPoint PDF export and native visual review: NOT RUN / awaiting user approval. Do not retry without authorization.', '',
           'Readiness: stop troubleshooting at minute 25; use 25–28 for source evidence and transition. Preserve the break, verification and Q&A.', '',
           'Two-minute model stall: switch to authored specimen. Cut optional styling/stretch work first; report incomplete execution honestly.', '']
    for d in slides:
        parts.extend([f'## {d["id"]} · {d["elapsed"]} · {d["title"]}', '',d['notes'],''])
        for prompt in d.get('full_workbook_prompts',[]):
            parts.extend(['**Full workbook prompt / instruction**','','```text',prompt.rstrip(),'```',''])
    (OUT/'FACILITATOR-GUIDE.md').write_text('\n'.join(parts))
    source_lines=['# Sources and slide mapping','', 'Official source retrieval dates and executed evidence are recorded in the specialist reports linked below. Lead consumed those audits; this package makes no new upstream verification claim.','',
                  '- [Teaching sources and verification](facilitator/TEACHING-SOURCES-AND-VERIFICATION.md)',
                  '- [Official command/source matrix](participant/linux/COMMAND-VERIFICATION.md)',
                  '- [Fixture provenance](participant/teaching/labs/PROVENANCE.md)',
                  '- [Linux execution limits](facilitator/LINUX-VERIFICATION.md)','',
                  '| Slide | Elapsed | Original source notes / supporting artifacts |','| --- | --- | --- |']
    for d in slides:
        source_lines.append(f'| {d["id"]} {d["title"]} | {d["elapsed"]} | '+ '; '.join(d.get('source_mapping',[]) or ['Teaching projection-content / lab references; see provenance'])+' |')
    (OUT/'SOURCES-AND-MAPPING.md').write_text('\n'.join(source_lines)+'\n')
    (OUT/'README.md').write_text('''# CITE AI for Cyber Security — workshop package

**Attendees start here: [Participant workbook](participant/teaching/PARTICIPANT-WORKBOOK.html).** It links the complete print/offline no-account packet. Handouts also have editable Markdown sources. The participant ZIP contains only attendee instructions, answer material, setup/source references and safe lab assets; internal proposals/reviews remain in the team source folders.

**Facilitators:** use the [facilitator guide](FACILITATOR-GUIDE.html) for timings, debriefs and full prompts, plus [computed agenda](participant/teaching/AGENDA.html), [source mapping](SOURCES-AND-MAPPING.html) and [verification report](VERIFICATION.md). Facilitator source-audit records are in `facilitator/`, outside the participant ZIP.

`CITE-AI-Cybersecurity-Workshop.pptx` is editable, with 21 timed core slides and four hidden support views. Use the Help buttons during work and Return to lab on support views. The hidden views add zero minutes. Scope: fictional policy checklist, deterministic synthetic log triage, static local HTML report. Default live route is approved Claude; local Python and paper review need no AI account. Paper work is recorded as review, not execution.

## Prepare the disposable lab

Installation/authentication are prework. Use an organization-approved disposable environment; a new folder is not isolation. Python 3.11+ is the participant floor; Linux rehearsal target is Ubuntu 24.04/Python 3.12. Actual reference execution here used macOS/Python 3.14.9. Linux/WSL runtime rehearsal remains NOT RUN.

Inside that prepared environment, place this package's `participant/teaching` and `participant/linux` folders under `~/cite-workshop/` as siblings. Open a terminal in `~/cite-workshop/teaching`, inspect the workbook R0 commands, then create a fresh `work/` folder. Do not run from the repository root. Use fresh output names on reruns; reference scripts refuse to overwrite output. No GitHub account, SSH key, pip, Node, plugin, scanner or server is needed. A print-only attendee needs only the complete no-account packet.

## Delivery and limitations

Native PowerPoint PDF export: **NOT RUN — awaiting user approval**. The export approval request was canceled without authorization. It was not retried. No exported PDF, PDF raster or native visual-review claim is supplied. The one-slide probe PPTX is a tooling artifact, not part of the session. Handout HTML has local print CSS; no external assets, scripts or invented public URLs. These HTML handouts are not slide renders.

Coordinator-relayed final specialist findings have been resolved and regression-checked; see the verification report. Structural and reference-code checks do not establish classroom pacing, agent inference, participant-generated correctness, browser rendering or Linux/WSL installation success.

## Reproduce in this repository

Use the coordinator-prepared document interpreter recorded in `../integration/BUILD-APPROACH.md`. Run `prepare_manifest.py`, `build_deck.py`, `package_workshop.py`, then `verify_final.py` from `Workshop-Team/integration/` via that interpreter (the scripts resolve paths themselves). Source/build files live there; source design tokens are under `Workshop-Team/design/`, source teaching assets under `Workshop-Team/teaching/`, and read-only brand assets under root `Files/`. No original builder is imported or executed. No dependencies are installed and no native-export script is invoked by this build sequence.
''')
    for path in sorted(OUT.rglob('*.md')):
        render_md(path)
    print(f'Packaged Markdown/HTML handouts and lab files under {KIT}')

if __name__=='__main__':
    main()
