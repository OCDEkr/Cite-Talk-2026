"""Build the CITE slide deck from the existing eight-section outline and guide.
Produces only the deck, its PDF proof, and visual verification images.
"""
from pathlib import Path
import re
import json
from PIL import Image, ImageDraw, ImageFont
import fitz
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent/'CITE-Slides'
OUT.mkdir(exist_ok=True)
FONTDIR=Path('/System/Library/Fonts/Supplemental')
FONTS={'regular':FONTDIR/'Arial.ttf','bold':FONTDIR/'Arial Bold.ttf','mono':FONTDIR/'Andale Mono.ttf'}
BG='#FFFFFF'; FG='#111111'; MUTED='#454B53'; ACCENT='#155191'; PANEL='#EFF4FA'
LOGO=ROOT/'Files'/'Mark-Title-COLOR-ForLightBG.png'
prs=Presentation(); prs.slide_width=Inches(13.333333); prs.slide_height=Inches(7.5)
prs.core_properties.title='AI for Cyber Security — CITE 2026'
prs.core_properties.author='Kevin Riley'
pdf=fitz.open()

class Canvas:
    def __init__(self,dark=False):
        self.slide=prs.slides.add_slide(prs.slide_layouts[6]); self.page=pdf.new_page(width=960,height=540)
        self.dark=dark
        self.slide.background.fill.solid()
        self.slide.background.fill.fore_color.rgb=RGBColor.from_string('000000' if dark else 'FFFFFF')
        self.rect(0,0,960,540,'#000000' if dark else BG)
    def color(self,color):
        if self.dark:
            return {FG:'#FFFFFF',MUTED:'#D3D7DD',PANEL:'#151515'}.get(color,color)
        return color
    def rect(self,x,y,w,h,color):
        color=self.color(color)
        from pptx.enum.shapes import MSO_SHAPE
        s=self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x/72), Inches(y/72), Inches(w/72), Inches(h/72))
        s.fill.solid(); s.fill.fore_color.rgb=RGBColor.from_string(color[1:]); s.line.fill.background()
        self.page.draw_rect(fitz.Rect(x,y,x+w,y+h),color=None,fill=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)))
    def text(self,text,x,y,w,h,size=22,color=FG,style='regular'):
        color=self.color(color)
        # Keep the logo blue as a graphic accent on black while using white text.
        if self.dark and color==ACCENT: color='#FFFFFF'
        font=ImageFont.truetype(str(FONTS[style]),size*4)
        lines=[]
        for para in text.split('\n'):
            if not para: lines.append(''); continue
            line=''
            for word in para.split(' '):
                candidate=(line+' '+word).lstrip()
                if font.getlength(candidate)/4>w and line:
                    lines.append(line); line=word
                else: line=candidate
            lines.append(line)
        lh=size*1.22
        if len(lines)*lh>h+1:
            raise ValueError(f'Text overflow: {text[:60]!r}: {len(lines)*lh:.1f} > {h}')
        for j,line in enumerate(lines):
            if not line: continue
            box=self.slide.shapes.add_textbox(Inches(x/72),Inches((y+j*lh)/72),Inches(w/72),Inches(lh/72))
            tf=box.text_frame; tf.clear(); tf.word_wrap=False
            tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
            p=tf.paragraphs[0]; p.text=line
            p.font.name='Andale Mono' if style=='mono' else 'Arial'
            p.font.size=Pt(size); p.font.bold=style=='bold'; p.font.color.rgb=RGBColor.from_string(color[1:])
            p.space_before=Pt(0); p.space_after=Pt(0)
            name={'regular':'WorkshopRegular','bold':'WorkshopBold','mono':'WorkshopMono'}[style]
            self.page.insert_font(fontname=name,fontfile=str(FONTS[style]))
            self.page.insert_text((x,y+j*lh+size*.94),line,fontsize=size,fontname=name,
                color=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)))
    def line(self,x1,y1,x2,y2,color=ACCENT,width=1.8):
        from pptx.enum.shapes import MSO_CONNECTOR
        shape=self.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
            Inches(x1/72),Inches(y1/72),Inches(x2/72),Inches(y2/72))
        shape.line.color.rgb=RGBColor.from_string(color[1:]); shape.line.width=Pt(width)
        self.page.draw_line((x1,y1),(x2,y2),color=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)),width=width)
    def outline(self,x,y,w,h,oval=False,color=ACCENT,width=1.8):
        from pptx.enum.shapes import MSO_SHAPE
        shape=self.slide.shapes.add_shape(MSO_SHAPE.OVAL if oval else MSO_SHAPE.RECTANGLE,
            Inches(x/72),Inches(y/72),Inches(w/72),Inches(h/72))
        shape.fill.background(); shape.line.color.rgb=RGBColor.from_string(color[1:]); shape.line.width=Pt(width)
        rgb=tuple(int(color[i:i+2],16)/255 for i in (1,3,5))
        if oval: self.page.draw_oval(fitz.Rect(x,y,x+w,y+h),color=rgb,width=width)
        else: self.page.draw_rect(fitz.Rect(x,y,x+w,y+h),color=rgb,width=width)
    def icon(self,name,x,y,size=29):
        """Small original line icons, kept as editable PowerPoint geometry."""
        color='#FFFFFF' if self.dark else ACCENT
        # Icon paths use a 24-unit grid.
        def line(a,b,c,d): self.line(x+a*size/24,y+b*size/24,x+c*size/24,y+d*size/24,color)
        def box(a,b,w,h,oval=False): self.outline(x+a*size/24,y+b*size/24,w*size/24,h*size/24,oval,color)
        if name=='terminal':
            box(2,3,20,17); line(6,8,10,11); line(10,11,6,14); line(13,15,18,15)
        elif name=='code':
            line(8,6,2,12); line(2,12,8,18); line(16,6,22,12); line(22,12,16,18); line(14,3,10,21)
        elif name=='check':
            box(2,2,20,20,True); line(6,12,10,16); line(10,16,18,8)
        elif name=='eye':
            for a,b,c,d in [(1,12,7,6),(7,6,17,6),(17,6,23,12),(23,12,17,18),(17,18,7,18),(7,18,1,12)]: line(a,b,c,d)
            box(9,9,6,6,True)
        elif name=='folder':
            for a,b,c,d in [(2,5,10,5),(10,5,13,8),(13,8,22,8),(22,8,22,20),(22,20,2,20),(2,20,2,5)]: line(a,b,c,d)
        elif name=='file' or name=='book':
            box(4,2,16,20); line(8,8,16,8); line(8,12,16,12); line(8,16,14,16)
            if name=='book': line(7,2,7,22)
        elif name=='shield':
            for a,b,c,d in [(3,4,12,1),(12,1,21,4),(21,4,20,15),(20,15,12,22),(12,22,4,15),(4,15,3,4)]: line(a,b,c,d)
            line(7,11,11,15); line(11,15,17,8)
        elif name=='lock':
            box(4,10,16,12); box(7,2,10,12,True); line(12,15,12,18)
        elif name=='target' or name=='scan' or name=='globe':
            box(2,2,20,20,True)
            if name=='target': box(7,7,10,10,True); line(12,12,21,3)
            elif name=='scan':
                line(12,12,19,5); line(12,2,12,22); line(2,12,22,12); box(7,7,10,10,True)
            else: box(7,2,10,20,True); line(2,12,22,12)
        elif name=='person':
            box(8,1,8,8,True); line(3,22,3,17); line(3,17,8,12); line(8,12,16,12); line(16,12,21,17); line(21,17,21,22)
        elif name=='chat':
            box(2,3,20,15); line(6,18,6,23); line(6,23,12,18); line(7,8,17,8); line(7,12,14,12)
        elif name=='package':
            box(3,4,18,17); line(3,9,21,9); line(10,4,10,13); line(14,4,14,13)
        elif name=='window':
            box(2,3,20,18); line(2,8,22,8); line(5,5.5,6,5.5); line(8,5.5,9,5.5)
    def branding(self,num):
        if num==1: return
        # Use the new light-background logo everywhere. White slides need no box;
        # black section slides get a white backing to preserve wordmark contrast.
        if self.dark: self.rect(679,490,243,48,'#FFFFFF')
        shape=self.slide.shapes.add_picture(str(LOGO),Inches(690/72),Inches(497/72),width=Inches(220/72))
        shape.name='OCDE logo watermark'
        self.page.insert_image(fitz.Rect(690,497,910,497+220*369/2000),filename=str(LOGO))


SECTIONS=[
    ('Intro','00–08','Intro.md'),
    ('Guardrails','08–16','Guardrails.md'),
    ('Hands-on setup','16–42','Setup Walkthrough.md'),
    ('Examples and demos','42–70','Examples.md'),
    ('Skills, agents, and plugins','70–85','Skills Agents Plugins.md'),
    ('Application builds','85–110','Application Builds.md'),
    ('Getting started','110–115','Getting Started.md'),
    ('Close','115–120','Close.md')]
SLIDES=[]

def source_block(filename,heading):
    """Read an actual note section, so prompts come from the user's source."""
    text=(ROOT/filename).read_text()
    match=re.search(r'^#{2,3} '+re.escape(heading)+r'\s*$',text,re.M)
    if not match: raise ValueError((filename,heading))
    tail=text[match.end():]
    end=re.search(r'^#{2,3} ',tail,re.M)
    return tail[:end.start()] if end else tail

def prompt_from(filename,heading):
    return re.search(r'```[^\n]*\n(.*?)\n```',source_block(filename,heading),re.S).group(1)

def add(section,kind,title,items=(),notes='',source=None,prompt=None,icons=(),sub='',minutes=None):
    s={'section':section,'kind':kind,'title':title,'items':list(items),'notes':notes,
       'source':source or SECTIONS[section-1][2], 'prompt':prompt,'icons':list(icons),
       'sub':sub,'minutes':minutes}
    SLIDES.append(s)

def divider(section,sub):
    add(section,'divider',SECTIONS[section-1][0],sub=sub,
        notes=f'Section {section} of Talk Outline.md. Follow the linked notes and the existing HTML guide. Section allocation: {SECTIONS[section-1][1]} elapsed minutes.')

def practice(section,title,items,minutes,notes='',source=None):
    add(section,'practice',title,items,notes,source=source,minutes=minutes)

# 01 — Intro: the original framing, audience, definition, applications, and caveat.
add(1,'title','AI for Cyber Security',
    ['What AI-assisted coding does for small teams','Kevin Riley · CITE 2026 · kriley@ocde.us'],
    'Audience: K–12 district and county-office IT staff, often teams of one to five who own networks, identity, devices, and security. Open with the work that waits because nobody has time to write the script. No demo during the intro.',sub='01 · INTRO')
add(1,'agenda','The route',
    [(f'{i:02d}',name,time) for i,(name,time,_) in enumerate(SECTIONS,1)],
    'This deck follows Talk Outline.md in its stated order. The HTML guide puts Build an app before Extend it; the root outline governs deck order, so Skills/Agents/Plugins comes before Application builds. Examples occupy 42–65; a five-minute break is included at 65–70. Setup assumes the prework recommended by Setup Walkthrough: complete early installs before arrival. Without prework, the source estimates about 55 minutes for setup, which would not fit the full two-hour session. Keep prompts in the existing guide and notes; there is no attendee kit.',source='Talk Outline.md; Cite Talk Guide.html')
add(1,'statement','Who this is for',
    ['You, if your “security team” is also the help desk, the network team, and the person who resets passwords.'],
    'Ask for a show of hands: who has dedicated security staff? Most people know what needs doing. The limiting factor is hours. Use the original small-team framing without adding an unsupported current staffing statistic.')
add(1,'cards','What AI-assisted coding is',
    [('Autocomplete','Finishes the line you started.'),('Chat','You ask, copy, run, and check.'),('Agents','Read files, write code, run it, and respond to results.')],
    'The talk focuses on level 3. Describe the file/terminal loop and the human’s role in defining the goal and checking the result. The tool knows your environment only through the context and access you provide.',icons=['code','chat','terminal'])
add(1,'grid','The work nobody had time to script',
    [('Log triage','Review the outliers.'),('Config review','Check network and identity exports.'),('Glue scripts','Connect the systems you already run.'),('Incident prep','Draft playbooks and evidence collection.'),('Vendor code','Read it before running as admin.'),('Compliance','Draft requests and control evidence.')],
    'Keep all six application areas from Intro. These are examples of potential work, not promised time savings. Save live work for Examples.',icons=['scan','shield','code','folder','eye','file'])
add(1,'cards','Why small teams gain the most',
    [('A large security team','Already has scripting and analysis specialists. The tools can help them move faster.'),('A small district IT team','Can tackle useful work that previously stayed in the backlog.')],
    'Retain the capability argument from Intro. Avoid a guaranteed factor-of-ten claim or fixed estimates for hours saved. Your judgment supplies the operational context.',icons=['person','target'])
add(1,'statement','The caveat before we go on',
    ['It will confidently write a script that deletes the wrong accounts. You still have to read it.'],
    'The wording comes from Intro. Transition directly into the five guardrails. State the risk plainly and explain that the same review habits apply to the later app build.')

# 02 — Guardrails, before setup and before any demo.
divider(2,'Five rules before any demo.')
add(2,'list','The five guardrails',
    ['Read before you run.','Work in a safe place.','Protect the data.','Keep permissions tight.','Verify the output.'],
    'Handout: Guardrails Checklist.md. These are professional working habits for every demonstration. Keep legal statements general and refer to the district’s own data-review process.',icons=['eye','folder','lock','shield','check'])
add(2,'cards','Read it. Give it a safe place to work.',
    [('Read before you run','Inspect actions that delete, disable, write, or send.'),('Work in a safe place','Use a scratch folder, test tenant, or non-production copy.')],
    'Use report-only mode for cleanup scripts before changes. A scratch folder organizes work but is not OS isolation; a process can still act with the user’s permissions. See Guardrails, rules 1–2.',icons=['eye','folder'])
add(2,'cards','Protect the data and the access',
    [('Protect the data','No student records, passwords, API keys, or unapproved district information in prompts.'),('Keep permissions tight','Use the narrowest access required. Review plugins and shell commands.')],
    'Follow the local approval and data-privacy agreements. Credentials needed by code belong outside the prompt. Do not claim that any paid plan automatically prevents training or makes district data approved. Shell access can change files even without an Edit tool.',icons=['lock','shield'])
add(2,'statement','Confidence is not evidence',
    ['Run the query against known data. Test the script. Spot-check the citations.'],
    'The model is fluent whether right or wrong. Logs, vendor documents, and web pages can contain prompt-injection attempts. Treat their contents as evidence to inspect, not authority to change the task. A human owns claims going to leadership or an auditor.')

# 03 — Setup, using the existing guide and the requested GitHub/clone introduction.
divider(3,'Claude Code running, a project on GitHub, and an editor ready.')
add(3,'git','Get Git on Mac or PC',
    [('MAC · TERMINAL','xcode-select --install\nFinish the installer; reopen Terminal.\nWith Homebrew already installed: brew install git'),
     ('PC · GIT BASH','git-scm.com/install/windows\nInstall Git for Windows, including Git Bash.\nOpen Git Bash from the Start menu.')],
    'This slide precedes the first hands-on pause. Git is the software; clone is a command it includes. On a Mac use Terminal. On Windows use Git Bash for the shared shell commands. The GitHub URL is confirmed by the repository origin and Kevin. Use HTTPS to download the talk so students do not need SSH keys just to read it. Installing Apple Command Line Tools can take time; send as prework. Check git --version after installation.',source='User-requested GitHub/install slide; Setup Guide.md; https://git-scm.com/install/mac; https://git-scm.com/install/windows')
add(3,'code','Clone the talk and open the guide',
    ['git --version\ncd ~/Desktop\ngit clone https://github.com/OCDEkr/Cite-Talk-2026.git\ncd Cite-Talk-2026',
     'Open Cite Talk Guide.html in your browser.\nUse Setup Guide.md and the Cheat Sheets folder alongside it.'],
    'Run this block in Mac Terminal or Windows Git Bash. Choose another writable folder if Desktop is not available. If Cite-Talk-2026 already exists, open that clone and update deliberately rather than overwriting it. Confirm the root contains Cite Talk Guide.html, Talk Outline.md, Files, and Cheat Sheets. Repository access must be checked before the event if it is private. No new kit or scripts subfolder is the attendee destination.',source='Talk Outline.md; Cite Talk Guide.html; repository origin',sub='github.com/OCDEkr/Cite-Talk-2026')
add(3,'splitcode','Check Git, Python, and Node',
    [('MAC · TERMINAL','brew install git python node\n\ngit --version\npython3 --version\nnode --version'),
     ('PC · POWERSHELL, THEN GIT BASH','winget install Python.Python.3.12\nwinget install OpenJS.NodeJS.LTS\n\n# Reopen Git Bash, then check:\npython --version\nnode --version')],
    'Follow the platform paths in the existing guide. Homebrew must already be installed before the Mac command; the HTML guide includes its install line. Git for Windows was installed on the previous slide. Windows installers run from PowerShell; reopen Git Bash afterward for PATH updates. Windows uses python rather than python3. Claude Code itself does not require Node/Python, but generated projects may. Linux/WSL commands remain in the guide.',source='Setup Guide.md; Setup Walkthrough.md; Cite Talk Guide.html')
add(3,'splitcode','Install Claude Code, then sign in',
    [('MAC / LINUX / WSL','curl -fsSL https://claude.ai/install.sh | bash\n\nclaude --version\nclaude doctor\nclaude'),
     ('WINDOWS · POWERSHELL','irm https://claude.ai/install.ps1 | iex\n\n# Reopen Git Bash:\nclaude --version\nclaude doctor\nclaude')],
    'Official installer commands verified during preparation. Installation and account access should be tested ahead of time. At the Claude prompt use /status to check the account and model. WSL may require copying a printed login URL into the Windows browser. Point to HTML guide step 4b for the alternative provider path; do not switch the entire class provider live.',source='Setup Guide.md; Cite Talk Guide.html; https://code.claude.com/docs/en/setup',sub='Inside Claude Code: /status')
add(3,'code','Permissions and the workshop shortcut',
    ['# Bash · Windows Git Bash or Linux\necho \'alias clauded="claude --dangerously-skip-permissions"\' >> ~/.bashrc\n. ~/.bashrc',
     '# Zsh · macOS default shell\necho \'alias clauded="claude --dangerously-skip-permissions"\' >> ~/.zshrc\n. ~/.zshrc'],
    'Choose the block for the shell you are using; do not run both. echo writes the quoted alias definition literally, and >> appends without replacing the existing configuration. The next command uses the dot builtin to load the file into the current shell. Use the home path ~/.bashrc or ~/.zshrc, not ./.bashrc unless the current directory actually is the home directory. Run the block once to avoid duplicate entries. The alias bypasses permission checks and is optional; plain claude also works. Bypass mode is not a sandbox and can act with the user’s permissions. Use only for the workshop’s throwaway work, away from real systems and sensitive files. /permissions inspects and narrows access. Do not assume all installations have the same default permission mode.',source='Setup Guide.md §6; Cite Talk Guide.html §5; Guardrails.md; user-requested echo/reload commands',
    sub='Choose your shell. >> appends; the leading dot reloads the file. clauded skips permission checks.')
add(3,'code','Connect your own GitHub account',
    ['ssh-keygen -t ed25519 -C "you@yourdistrict.org"\ncat ~/.ssh/id_ed25519.pub\nssh -T git@github.com',
     'GitHub → Settings → SSH and GPG keys → New SSH key'],
    'This sets up the attendee’s own project, distinct from cloning the talk repository with HTTPS. Use a GitHub account and never overwrite an existing key. Use a passphrase on work machines. Copy only the .pub file into GitHub, never the private key. Check the authenticated message; “does not provide shell access” is normal. The source’s blank-passphrase suggestion is not necessary to complete the exercise.',source='Setup Guide.md §7; Setup Walkthrough.md; Cite Talk Guide.html §6')
add(3,'cards','VS Code and the GitHub CLI',
    [('VS Code','Open the project. Install Python and Claude Code extensions; WSL users add the WSL extension.'),('GitHub CLI','Install gh, then run gh auth login. Check with gh auth status.')],
    'Mac: brew install gh. Linux/WSL: follow the guide’s package-manager path. Windows: install GitHub CLI via its current official package. gh enables Claude to create a repository; SSH authentication alone does not. Browser fallback: create the empty private repo manually, then give Claude its SSH URL. Verify code . works in the selected shell if using it.',source='Setup Guide.md §§8–9; Setup Walkthrough.md; Cite Talk Guide.html §7',icons=['window','terminal'])
add(3,'prompt','Connect your first project',
    notes='From a new project folder, launch Claude and run /init first. Use plain claude or the optional clauded alias discussed in the guide. Replace YOUR_GITHUB_USERNAME. Do not run this inside the talk clone; it creates the attendee’s own project. Read commands before allowing writes/pushes. The exact prompt is from Setup Guide, step 10.',
    source='Setup Guide.md §10; Cite Talk Guide.html §8',
    prompt='Set up this folder as a git repository named "my-project", create a private GitHub repository under the username YOUR_GITHUB_USERNAME, add it as the origin remote using SSH, and push. Use the gh command for anything that needs GitHub itself.',
    sub='mkdir -p ~/my-project && cd ~/my-project  →  claude  →  /init')
practice(3,'Pause: finish your setup',
    [('DO','Follow the setup steps in Cite Talk Guide.html. Finish login, editor, and your first project.'),('CHECK','Claude answers in the right folder. Your own private repository shows the project files.'),('IF BLOCKED','Use the guide’s troubleshooting steps or pair with a working machine.')],12,
    'Target elapsed 30–42. All platform installations should already be underway or done from prework. Original Setup Walkthrough allows 55 minutes from cold; this two-hour version needs prework. Keep both the talk clone and the attendee project clear in the explanation. Show the project pushed to GitHub before moving to examples.',source='Setup Walkthrough.md; Setup Guide.md; Cite Talk Guide.html')
add(3,'cards','Optional ways to extend your setup',
    [('No paid plan?','Step 4b describes OpenRouter. Check provider availability and data terms before use.'),('Optional tools','herdr, Codex, and Hermes have their own setup sections. Everyone uses Claude Code in this class.')],
    'Keep these references so the HTML guide remains complete. They are optional, not additional installation requirements during the timed setup block. The exact free model ID, provider logging/training terms, and non-Anthropic compatibility need a near-event check. Do not repeat the source’s blanket paid-versus-free data-training claim. Other-agent installation commands are intentionally left in the guide rather than adding another toolchain to the class.',source='Cite Talk Guide.html §§4b,9–11; user clarification',icons=['globe','book'])

# 04 — All five example areas, with hands-on pauses on existing prompts/assets.
divider(4,'GRC, red team, blue team, code review, and OSINT.')
add(4,'list','Five areas. Useful outputs.',
    ['GRC: policies, procedures, and vendor vetting.','Red team: exposure reports, awareness, and tabletops.','Blue team: log triage, detection rules, and alert explanations.','Code review: vendor scripts and your own automation.','OSINT: your own organization’s public exposure.'],
    'Only authorized assets and scrubbed or synthetic data. Examples.md recommends two or three live demos rather than all of them. Use one GRC prompt, the existing fictitious scan report, and a code/config review. Blue-team log triage is the strongest live demo if the presenter stages a suitable log export.',source='Examples.md; Cite Talk Guide.html · Try prompts',icons=['file','scan','shield','eye','globe'])
add(4,'cards','GRC: turn documents into useful work',
    [('Policy gaps','Compare an AUP with CIS IG1 and NIST CSF Govern.'),('Policy to procedure','Turn the 24-hour offboarding requirement into an auditable checklist.'),('Vendor vetting','Use provided terms and privacy documents. Mark silence “not addressed”.')],
    'These are the three GRC examples in Examples.md. The following exercise uses policy-to-procedure because the source prompt supplies the policy sentence and systems. It needs no new input file or invented handout.',source='Examples.md · GRC',icons=['file','check','eye'])
add(4,'prompt','GRC: turn a policy into a procedure',
    notes='The prompt is copied verbatim from Examples.md, “Turn a policy into a procedure.” This produces a draft checklist only. No identity system is connected and no accounts are changed. Point to the evidence column.',
    source='Examples.md · Turn a policy into a procedure',
    prompt=prompt_from('Examples.md','Turn a policy into a procedure'))
practice(4,'Pause: make the checklist usable',
    [('DO','Run the offboarding prompt. Ask a follow-up that makes the checklist useful to your team.'),('CHECK','Find the role, verification, and evidence for each named system.'),('DISCUSS','Which steps came from the policy, and which still need a district decision?')],5,
    'Use the existing prompt, not a generated training policy or new lab pack. Keep the 24-hour requirement, inspect missing assumptions, and do not execute offboarding actions. Short share-back: one useful row and one thing to verify.',source='Examples.md · Turn a policy into a procedure')
add(4,'prompt','Red team: make sense of your scan',
    notes='Use the existing Files/scan-report.pdf: a fictitious vulnerability report. Start Claude in the cloned repository’s Files directory so the prompt’s filename resolves. No new input is created. This interprets an already-produced report; it does not run an attack. The Nessus source is also present, but it is not Nmap XML.',
    source='Examples.md · Make sense of your own exposure report; Files/scan-report.pdf',
    prompt=prompt_from('Examples.md','Make sense of your own exposure report'),sub='Existing file: Files/scan-report.pdf')
practice(4,'Pause: find Monday’s priorities',
    [('DO','Run the exposure-report prompt against Files/scan-report.pdf.'),('CHECK','Trace one recommended fix back to the report’s finding and evidence.'),('DISCUSS','Would cabinet understand the summary? What needs confirmation before acting?')],5,
    'A second basic-task pause using an existing repository file. Verify the difference between unique findings and affected host instances. Do not accept a false-positive claim as fact without support. The file identifies its data as fictitious. Other red-team prompts in the guide cover awareness scenarios and ransomware tabletops.',source='Examples.md · Red team; Files/scan-report.pdf')
add(4,'prompt','Blue team: triage a log export',
    notes='This is the original blue-team prompt. Stage an approved scrubbed/synthetic signins.csv before presenting if running live; that file is not currently in the root materials. Do not imply it comes from a new kit. The agent should inspect schema and explain thresholds. Impossible travel requires location/time evidence; it must not invent coordinates or history. Show both the flagged rows and the reusable script. Other blue-team prompts cover KQL and alert interpretation.',
    source='Examples.md · Triage a log export; Cite Talk Guide.html · Blue team',
    prompt=prompt_from('Examples.md','Triage a log export'),sub='Demo when a suitable signins.csv is staged; review the code and the evidence.')
add(4,'prompt','Code review: read it before it runs',
    notes='Copied from Examples.md. Stage a non-sensitive deploy.ps1 if demonstrating this exact prompt; no such script is currently present. The existing Files/cisco-config.txt.md is available for config review now and will be used in the skill example. Never execute the script just to review it. The second code-review example in the notes checks cleanup-accounts.py for date/filter errors.',
    source='Examples.md · Review a script before you run it as admin',
    prompt=prompt_from('Examples.md','Review a script before you run it as admin'))
add(4,'prompt','OSINT: see what an outsider sees',
    notes='Use public sources about your own organization, within authorization. The source prompt uses Example Unified School District as a placeholder. Give a real approved organization for a live demo rather than inventing public-source findings. The second OSINT example uses Have I Been Pwned; bulk access may require an API key. No automatic staff messaging.',
    source='Examples.md · What your district leaks publicly',
    prompt=prompt_from('Examples.md','What your district leaks publicly'))
add(4,'break','Five-minute break',
    ['Save your work. Return at elapsed minute 70.','Next: skills, agents, plugins, then the app build.'],
    'Pause at 65–70 elapsed. This break is between the examples and extensions sections. It does not reorder the outline.',sub='65–70 · BREAK')

# 05 — The manual tutorials and ECC install explicitly requested by the outline.
divider(5,'A skill for a task. An agent for a job. A plugin to package them.')
add(5,'cards','Smallest to largest',
    [('Skill','Instructions Claude loads for a repeatable task.'),('Agent','A specialist with its own context and selected tools.'),('Plugin','Skills, agents, hooks, and connectors packaged for installation.')],
    'Teach the same nesting as Skills Agents Plugins.md and the HTML guide. Skills guide behavior; they are not permission isolation. Agents need appropriate tools and limits. Plugins can execute code through hooks and servers.',icons=['file','person','package'])
add(5,'code','Build a skill: a folder and a file',
    ['~/.claude/skills/config-review/SKILL.md',
     '---\ndescription: Reviews a network device config against\n  district security standards. Use for config reviews.\n---\nCheck weak credentials, SNMP communities, telnet,\nmanagement access, and missing syslog.\nReturn issue, source line, severity, and proposed fix.\nDo not change the configuration.'],
    'Based on the manual config-review tutorial in Skills Agents Plugins.md. Personal path: ~/.claude/skills; project-shared path: .claude/skills. The abbreviated on-screen skill preserves the source checks and output. Full original tutorial remains in the root note. The existing switch configuration has weak credentials, public/private SNMP, and telnet; management reachability cannot be determined fully from this snippet, so identify uncertainty.',source='Skills Agents Plugins.md · Build a skill by hand; Files/cisco-config.txt.md; https://code.claude.com/docs/en/skills')
practice(5,'Pause: try your config-review skill',
    [('DO','Create the skill from the tutorial. Invoke /config-review with the supplied Cisco configuration.'),('CHECK','Trace one finding to its exact source line.'),('DISCUSS','Which findings are proven by the file, and which require network context?')],4,
    'Use Files/cisco-config.txt.md from the existing clone. Show how to reference its path or paste the supplied config. Do not apply the proposed configuration changes. This is a practice pause inside the original skills tutorial, not a replacement exercise.',source='Skills Agents Plugins.md · Build a skill by hand; Files/cisco-config.txt.md')
add(5,'code','Build an agent: a narrow job',
    ['~/.claude/agents/log-triage.md',
     '---\nname: log-triage\ndescription: Reviews exported security logs.\ntools: Read, Bash, Grep\nmodel: sonnet\n---\nFind anomalies and return ranked evidence.\nNever modify the source file.'],
    'This follows the log-triage tutorial. Important factual correction to the source: tools: Read, Bash, Grep still permits writes/deletes through Bash. “Never modify” is an instruction, not enforcement. For a reviewer that needs no execution, use Read, Glob, Grep and omit Bash. A log analyst that writes/runs a script needs execution access and corresponding sandbox/permission controls. Test delegation with “use the log-triage agent on signins.csv” only when a suitable input is staged.',source='Skills Agents Plugins.md · Build an agent by hand; https://code.claude.com/docs/en/sub-agents',sub='Bash can change files. Tool restrictions and instructions are different controls.')
add(5,'splitcode','Package the pieces as a plugin',
    [('DIRECTORY','my-security-pack/\n  .claude-plugin/plugin.json\n  skills/config-review/SKILL.md\n  agents/log-triage.md'),
     ('MANIFEST','{\n  "name": "my-security-pack",\n  "version": "0.1.0",\n  "description": "K-12 security pack"\n}')],
    'Show the structure from the original manual plugin tutorial; do not spend time publishing a marketplace. For local development, claude --plugin-dir ./my-security-pack. Explain hooks and MCP connectors, and review code before installing. The existing Skills/Grc assessment-v4.zip is a real packaged example in the repository.',source='Skills Agents Plugins.md · Build a plugin by hand; Skills/Grc assessment-v4.zip')
add(5,'code','Install ECC, then inspect what it adds',
    ['/plugin marketplace add https://github.com/affaan-m/ECC\n/plugin install ecc@ecc',
     '/plugin'],
    'Retains the ECC install explicitly requested in Talk Outline. Verified these native plugin commands against the ECC repository while preparing. First explain that enabled hooks run with the user’s permissions. Use the native plugin path once; do not also layer the full manual installer. Show an installed component or feature after installation. Exact agent/skill counts are deliberately not frozen.',source='Skills Agents Plugins.md · You do not have to build it all: install ECC; Cite Talk Guide.html · Extend it; https://github.com/affaan-m/ECC')
add(5,'list','Five focused plugins',
    ['Humanizer: edit AI-sounding prose.','Superpowers: plan, test, and debug systematically.','Frontend design: build the interface.','Impeccable: audit and improve the front end.','TDD: use a test-first workflow.'],
    'These are the five focused options in Skills Agents Plugins.md. Keep exact marketplace commands in the existing note; inspect the current manifest before use. Do not install every option live. Use /plugin to inspect what is installed, and choose the smallest extension that serves the job.',source='Skills Agents Plugins.md · A starter kit of plugins; Resource Index.md',icons=['file','target','window','eye','check'])

# 06 — The source prompt starts the live scanner build; no scanner is prebuilt.
divider(6,'From one-off scripts to a working application.')
add(6,'prompt','A web-based Zenmap clone',
    notes='Use Kevin’s original prompt verbatim, in a fresh project folder. Let the class watch research, planning, and clarifying questions before coding. This is a working scanner with a backend that invokes Nmap, plus saved-scan import, as Kevin clarified. It is built live with students; this preparation does not build a scanner. /model opus selects the available Opus model; check the actual model shown rather than assuming a version name.',
    source='Application Builds.md · Demo 1. An nmap web front end; Cite Talk Guide.html · Build an app; user clarification',
    prompt=prompt_from('Application Builds.md','Demo 1. An nmap web front end'),
    sub='Fresh project folder → /model opus → send the original prompt')
add(6,'cards','Have answers ready',
    [('Scan types','Discovery, ports, and service/version information. Leave OS detection off initially.'),('Stack and users','Simple local backend and web front end. One local user.'),('Inputs and targets','Real scans on authorized targets, plus saved Nmap XML import.')],
    'These are the questions anticipated in Application Builds.md. Install Nmap separately before the build. Keep the app bound to localhost and validate its scan inputs/backend invocation. Use only owned or explicitly authorized targets. Do not direct a room of students to scan the conference network. A simple TCP connect profile is a useful first working slice. The existing .nessus report is not Nmap XML; it cannot be substituted silently for an import test.',source='Application Builds.md; user clarifications',icons=['scan','window','folder'])
practice(6,'Pause: build it together',
    [('PLAN','Answer the questions and review the plan before code is written.'),('BUILD','Let Claude create the local front end and the backend that calls Nmap.'),('RUN','Launch the app. Run one authorized scan and inspect the actual result.')],15,
    'Section allocation 85–110: allow roughly five minutes for prompt/plan/questions, fifteen minutes to build, and five minutes to verify and debrief. This is a small first version, not full Zenmap feature parity. Build on screen with the students. If a dependency or model delay blocks completion, identify the failing layer honestly. Preserve verification time rather than polishing a topology view.',source='Application Builds.md; Cite Talk Guide.html · Build an app')
add(6,'list','Verify the app you just built',
    ['A real scan runs through the browser and backend.','Raw output and host/port/service views agree.','Saved Nmap XML imports into the result views.','Use the fictitious 50-machine scan to check display and navigation.','Explain an error, a validation rule, and the next improvement.'],
    'Kevin requested fictitious saved scan data with about 50 machines for an import test, alongside working real scans. No Nmap XML fixture is currently present in the supplied root files; stage that test input separately before class. The existing scan-report.nessus is a different format. Do not claim fabricated 45/5 or port totals from the discarded kit. A completed import alone is not the live scanner. Check target validation, command argument handling, errors/timeouts, and localhost binding before any wider use.',source='Application Builds.md; user clarification',icons=['scan','eye','folder','globe','check'])

# 07 — Plans, first task, habit, and adoption remain in the deck.
divider(7,'Pick a plan. Choose a first task. Build the habit.')
add(7,'plans','Pick a plan that fits the work',
    [('Free','$0','Claude chat; alternative-provider setup is in the guide.'),('Pro','$20/mo','About $17/mo with annual billing; includes Claude Code.'),('Max / Ultra','$100 / $200/mo','Higher individual usage tiers.'),('Team / Enterprise','Per-seat / quoted','Shared administration and district adoption.'),('API','Usage-based','Metered automation and scripts.')],
    'Keep the plan-selection section from Getting Started and the HTML guide. Official pricing checked during preparation: Pro is $20 billed monthly or roughly $17 per month with annual billing, Max $100, Ultra $200. Recheck pricing, eligibility, account controls, usage limits, and district agreements close to the event. A paid plan alone does not establish an approved data-handling destination.',source='Getting Started.md · Pick a plan; Cite Talk Guide.html · Get started; https://claude.com/pricing')
add(7,'cards','Choose your first project',
    [('Low stakes','Read data or work on a copy in a scratch folder.'),('Repetitive','Choose a task you do often enough to reuse the result.'),('Checkable','Know what a correct answer looks like.')],
    'Start with plain Claude Code, add extensions when a real need appears. Examples from the source: summarize sign-in logs, draft an offboarding checklist, review a privacy policy, or create a tabletop. Save disabling accounts and production changes for after the review habit is established.',source='Getting Started.md · What to install first; Choose your first project',icons=['shield','code','check'])
add(7,'cards','Build the habit. Bring it to your team.',
    [('One repeatable task','Write a skill and measure the time spent and corrections made.'),('One small pilot','Show evidence, agree on data/account rules, then scale deliberately.')],
    'Source: build one skill, measure the result, grow by one thing at a time. Bring leadership evidence from actual use rather than a promised multiplier. Review team/enterprise choices and approved-data rules when expanding beyond an individual trial.',source='Getting Started.md · Build the habit; Bring it to your team',icons=['file','person'])

# 08 — Original close and original attendee resources.
divider(8,'One frame. One action. Your questions.')
add(8,'statement','A fast junior analyst',
    ['Capable, tireless, and never trusted blind.','Monday: pick one annoying task. Give it one hour.'],
    'Recap the capability and the five guardrails in one breath. Do not guarantee the first task saves time; measure it. Use a scratch folder or approved copy and choose a result you can verify.',source='Close.md; Getting Started.md')
add(8,'list','Take the material with you',
    ['Cite Talk Guide.html: setup, prompts, guardrails, and resources.','Setup Guide.md: the step-by-step installation reference.','Guardrails Checklist.md: the habits to keep by your desk.','Resource Index.md and Cheat Sheets: more tools when you need them.'],
    'All materials are in the repository root or its existing subfolders. Return to the cloned repository and open Cite Talk Guide.html. No new attendee package or replacement guide is needed. Verify the repository is accessible to registrants before the event.',source='Close.md; Talk Outline.md; Cite Talk Guide.html',icons=['book','terminal','shield','folder'],sub='github.com/OCDEkr/Cite-Talk-2026')
add(8,'statement','Thank you. What would you want it to do first?',
    ['Kevin Riley · kriley@ocde.us'],
    'Reserve the end of the 115–120 block for Q&A. Ask what task in their own week they would point Claude Code at first if the room is quiet. End at the two-hour mark.',source='Close.md')


def render():
    for num,s in enumerate(SLIDES,1):
        section=s['section']; kind=s['kind']; items=s['items']; icons=s['icons']
        dark=kind in ('title','divider')
        c=Canvas(dark)
        label=f'{section:02d} · {SECTIONS[section-1][0].upper()}'
        if kind=='practice': label+=' · HANDS-ON PAUSE'
        if kind=='break': label='FIVE-MINUTE BREAK'
        c.text(label,48,29,760,25,12,ACCENT,'bold')
        c.text('65–70' if kind=='break' else SECTIONS[section-1][1],815,29,100,25,12,MUTED)
        c.rect(48,63,57,4,ACCENT)
        c.rect(48,506,608,1,'#7F8792' if dark else '#CCD2DA')
        c.text('CITE 2026  /  AI FOR CYBER SECURITY',48,516,510,18,9,MUTED)
        c.text(f'{num:02d}',620,516,40,18,9,MUTED)
        if kind in ('title','divider'):
            if kind=='divider':
                c.text(f'{section:02d}',48,104,220,95,70,ACCENT,'bold')
                c.rect(48,207,100,5,ACCENT)
                c.text(s['title'],48,237,864,125,43,FG,'bold')
                c.text(s['sub'],48,383,850,85,23,MUTED)
            else:
                c.rect(48,138,6,145,ACCENT)
                c.text(s['title'],78,157,820,128,48,FG,'bold')
                c.text(items[0],78,326,800,70,27,MUTED)
                c.text(items[1],78,431,800,50,18,MUTED)
        else:
            c.text(s['title'],48,86,864,91,34,FG,'bold')
            if kind=='agenda':
                for j,(index,title,time) in enumerate(items):
                    y=185+j*36
                    c.text(index,48,y,46,31,18,ACCENT,'bold')
                    c.text(title,118,y,640,31,21)
                    c.text(time,810,y,100,31,17,MUTED)
            elif kind=='cards':
                n=len(items); gap=20; w=(864-gap*(n-1))/n
                for j,(head,body) in enumerate(items):
                    x=48+j*(w+gap); c.rect(x,199,w,265,PANEL)
                    c.icon(icons[j] if icons else 'file',x+18,217,31)
                    c.text(head,x+18,266,w-36,73,24,ACCENT,'bold')
                    c.text(body,x+18,345,w-36,111,19)
            elif kind=='grid':
                for j,(head,body) in enumerate(items):
                    x=48+(j%3)*295; y=186+(j//3)*150
                    c.icon(icons[j],x,y,30)
                    c.text(head,x+45,y,225,57,21,ACCENT,'bold')
                    c.text(body,x+45,y+63,225,74,18)
            elif kind in ('statement','break'):
                size=35 if len(items[0])<100 else 31
                c.rect(48,203,5,218,ACCENT)
                c.text(items[0],77,205,820,215,size,FG,'bold')
                if len(items)>1: c.text(items[1],77,432,820,55,22,MUTED)
            elif kind=='list':
                step=57 if len(items)>=5 else 68
                for j,item in enumerate(items):
                    y=194+j*step
                    c.icon(icons[j] if icons else 'check',51,y,28)
                    c.text(item,109,y-2,801,step-5,22 if len(items)>=5 else 23)
                if s['sub']: c.text(s['sub'],48,476,864,25,14,ACCENT,'bold')
            elif kind=='practice':
                c.text(f'{s["minutes"]} MINUTES · WORK, THEN CHECK',48,178,864,27,13,ACCENT,'bold')
                for j,(head,body) in enumerate(items):
                    y=226+j*87
                    c.icon(['code','check','chat'][j],48,y,26)
                    c.text(head,88,y,113,29,13,ACCENT,'bold')
                    c.text(body,211,y-3,697,81,22)
            elif kind=='prompt':
                c.rect(48,190,864,259,PANEL)
                c.text(s['prompt'],69,213,822,220,21)
                if s['sub']: c.text(s['sub'],48,463,864,36,14,MUTED)
            elif kind=='git':
                c.text('github.com/OCDEkr/Cite-Talk-2026',48,178,864,37,23,ACCENT,'bold')
                for j,(head,body) in enumerate(items):
                    x=48+j*442; c.rect(x,243,422,204,PANEL)
                    c.text(head,x+17,260,388,29,18,ACCENT,'bold')
                    c.text(body,x+17,310,388,122,18)
                c.text('Install Git first. “git clone” is the command that downloads the repository.',48,466,864,34,16,MUTED)
            elif kind=='code':
                y=190
                for item in items:
                    size=17 if len(item.splitlines())>6 else 18
                    font=ImageFont.truetype(str(FONTS['mono']),size*4)
                    lines=sum(max(1,int(font.getlength(line)/4/826)+1) for line in item.splitlines())
                    # Actual wrapping is checked by Canvas.text.
                    h=max(53,min(250,lines*size*1.22+25))
                    c.rect(48,y,864,h,PANEL)
                    c.text(item,65,y+12,830,h-17,size,FG,'mono')
                    y+=h+15
                if s['sub']: c.text(s['sub'],48,466,864,36,14,MUTED)
            elif kind=='splitcode':
                for j,(head,body) in enumerate(items):
                    x=48+j*442; c.rect(x,190,422,271,PANEL)
                    c.text(head,x+15,205,392,45,15,ACCENT,'bold')
                    c.text(body,x+15,259,392,190,15,FG,'mono')
                if s['sub']: c.text(s['sub'],48,474,864,26,14,MUTED)
            elif kind=='plans':
                for j,(plan,price,body) in enumerate(items):
                    y=188+j*57
                    c.text(plan,48,y,190,49,21,ACCENT,'bold')
                    c.text(price,254,y,185,49,18)
                    c.text(body,457,y,454,50,18)
        c.branding(num)
        c.slide.notes_slide.notes_text_frame.text=(
            f'SECTION {section}: {SECTIONS[section-1][0]}\n'
            f'ELAPSED BLOCK: {SECTIONS[section-1][1]} minutes\n\n'
            f'{s["notes"]}\n\n'
            +(f'EXACT SOURCE PROMPT\n{s["prompt"]}\n\n' if s['prompt'] else '')
            +f'SOURCE: {s["source"]}\nPRIMARY REFERENCES: Talk Outline.md; Cite Talk Guide.html')
    prs.save(OUT/'CITE-AI-Talk-High-Contrast.pptx')
    pdf.save(OUT/'CITE-AI-Talk-High-Contrast.pdf',garbage=4,deflate=True)


def verify():
    p=Presentation(OUT/'CITE-AI-Talk-High-Contrast.pptx')
    assert len(p.slides)==len(SLIDES)
    assert [s['section'] for s in SLIDES]==sorted(s['section'] for s in SLIDES)
    assert [s['section'] for s in SLIDES if s['kind'] in ('title','divider')]==list(range(1,9))
    last=0
    for _,time,_ in SECTIONS:
        begin,end=map(int,time.split('–')); assert begin==last; last=end
    assert last==120
    logo=LOGO.read_bytes()
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    for i,(slide,s) in enumerate(zip(p.slides,SLIDES),1):
        assert slide.notes_slide.notes_text_frame.text.strip()
        assert str(slide.background.fill.fore_color.rgb)==('000000' if s['kind'] in ('title','divider') else 'FFFFFF')
        pics=[x for x in slide.shapes if x.shape_type==MSO_SHAPE_TYPE.PICTURE]
        assert len(pics)==(0 if i==1 else 1)
        assert all(x.image.blob==logo for x in pics)
        for shape in slide.shapes:
            assert shape.left>=0 and shape.top>=0
            assert shape.left+shape.width<=p.slide_width+10,(i,shape.name)
            assert shape.top+shape.height<=p.slide_height+10,(i,shape.name)
    all_content='\n'.join(s['title']+'\n'+s['notes']+'\n'+str(s['items']) for s in SLIDES)
    assert 'attendee-kit' not in all_content
    assert 'offboarding-policy.txt' not in all_content
    assert 'scripts/workshop-deck' not in all_content
    for category in ['GRC','Red team','Blue team','Code review','OSINT']:
        assert category in '\n'.join(s['title'] for s in SLIDES)
    app=next(s for s in SLIDES if s['title']=='A web-based Zenmap clone')
    assert app['prompt']==prompt_from('Application Builds.md','Demo 1. An nmap web front end')
    doc=fitz.open(OUT/'CITE-AI-Talk-High-Contrast.pdf'); assert len(doc)==len(SLIDES)
    for start in range(0,len(doc),12):
        sheet=Image.new('RGB',(1440,920),'#D9DEDD'); draw=ImageDraw.Draw(sheet)
        for j in range(min(12,len(doc)-start)):
            pix=doc[start+j].get_pixmap(matrix=fitz.Matrix(.48,.48),alpha=False)
            im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); im.thumbnail((458,205))
            x=(j%3)*480+10; y=(j//3)*230+22
            sheet.paste(im,(x,y)); draw.text((x,y-16),str(start+j+1),fill='black')
        sheet.save(OUT/f'preview-{start//12+1}.png')
    report={'slides':len(SLIDES),'outline_order':[s[0] for s in SECTIONS],
            'duration_minutes':120,'exact_logo_verified':str(LOGO),
            'black_slides':[i for i,s in enumerate(SLIDES,1) if s['kind'] in ('title','divider')],
            'source_notes':sorted({s[2] for s in SECTIONS}|{'Talk Outline.md','Cite Talk Guide.html','Setup Guide.md'}),
            'validation':'PASS: eight-section order, notes, logo, backgrounds, bounds, exact app prompt, and PDF pages.',
            'rendering_limit':'PDF proof shares layout instructions; native PowerPoint rendering was not compared.'}
    (OUT/'deck-verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    render()
    verify()

