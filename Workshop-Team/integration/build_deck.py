"""Editable PowerPoint builder. No GUI, network calls or PDF substitute."""
from pathlib import Path
import json
import math
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.oxml.xmlchemy import OxmlElement

HERE = Path(__file__).resolve().parent
TEAM = HERE.parent
ROOT = TEAM.parent
OUT = TEAM/'deliverables'
TOKENS = json.loads((TEAM/'design/tokens.json').read_text())
DATA = json.loads((HERE/'slides.json').read_text())
C = {k:v['hex'].lstrip('#') for k,v in TOKENS['color'].items()}
FONTS = {'Arial': Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
         'Consolas': Path('/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/Consola.ttf')}
for f in FONTS.values():
    assert f.exists(), f

def wrap(text, width, size, font):
    measure = ImageFont.truetype(str(FONTS[font]), round(size*4))
    lines = []
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            new = (line+' '+word).lstrip()
            if measure.getlength(new)/4 > width and line:
                lines.append(line)
                line = word
            else:
                line = new
            assert measure.getlength(line)/4 <= width+1, f'Unbreakable text: {line}'
        lines.append(line)
    return lines

def rgb(name):
    return RGBColor.from_string(C.get(name, name))

class Builder:
    def __init__(self):
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = Pt(960), Pt(540)
        self.p.core_properties.title = 'AI for Cyber Security — Two-hour workshop'
        self.p.core_properties.author = 'Kevin Riley'
        self.metrics = []
        self.links = []

    def rect(self, s, x,y,w,h, color):
        shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(x),Pt(y),Pt(w),Pt(h))
        shape.fill.solid(); shape.fill.fore_color.rgb = rgb(color)
        shape.line.fill.background()
        return shape

    def text(self,s,text,x,y,w,h,size=24,color='ink',bold=False,font='Arial',title=False,role='body'):
        lines = wrap(text,w-4,size,font)
        need = len(lines)*size*1.19+4
        assert need <= h+1, f'{s.shapes.title.text if s.shapes.title else ""}: {text[:60]} needs {need:.1f}, has {h}'
        shape = s.shapes.title if title else s.shapes.add_textbox(Pt(x),Pt(y),Pt(w),Pt(h))
        shape.left,shape.top,shape.width,shape.height = Pt(x),Pt(y),Pt(w),Pt(h)
        shape.name = ('Title' if title else role) + ' · ' + text[:35]
        tf=shape.text_frame; tf.clear(); tf.word_wrap=True; tf.auto_size=MSO_AUTO_SIZE.NONE
        tf.margin_left=tf.margin_right=Pt(2); tf.margin_top=tf.margin_bottom=Pt(0)
        # Soft wraps keep one logical paragraph editable as a single text block.
        p=tf.paragraphs[0]; p.text='\v'.join(lines)
        p.line_spacing=Pt(size*1.19); p.space_before=p.space_after=Pt(0)
        for r in p.runs:
            r.font.name=font; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=rgb(color)
            r._r.get_or_add_rPr().set('lang','en-US')
        self.metrics.append(dict(slide=self.p.slides.index(s)+1, text=text, role=role,
                                 size=size, font=font, required_height=round(need,2), available_height=h))
        return shape

    def build(self):
        for d in DATA:
            s=self.p.slides.add_slide(self.p.slide_layouts[5])
            dark=d['kind'] in ('title','close')
            s.background.fill.solid(); s.background.fill.fore_color.rgb=rgb('black' if dark else 'paper')
            if d.get('hidden'):
                s._element.set('show','0')
            fg='stage_ink' if dark else 'ink'
            accent='stage_accent' if dark else 'brand_blue'
            lab=d['kind']=='lab'
            phase = ('SUPPORT · '+d['id']) if d.get('hidden') else self.phase(d['slide'])
            if d['kind']=='reveal':
                phase = 'CHECK · '+phase
            self.text(s,phase,48,27,650,24,14,accent,True,role='meta')
            self.text(s,'Elapsed '+d['elapsed'],730,27,182,24,14,fg,role='meta')
            self.text(s,d['title'],48,77,864,96,48 if dark else 36,fg,True,title=True)
            if d['kind']=='title':
                self.text(s,d['sub'],48,216,800,100,28,fg)
                self.text(s,d['byline'],48,350,580,60,24,fg)
            elif d['kind']=='close':
                self.text(s,d['statement'],48,215,820,100,32,fg,True)
                self.text(s,d['byline'],48,350,600,60,24,fg)
            elif lab:
                self.lab(s,d)
            elif d.get('hidden'):
                self.support(s,d)
            elif d['kind']=='demo':
                block=d['blocks'][0]
                self.rect(s,48,184,864,160,'stage')
                self.text(s,'PROMPT · FULL TEXT IN WORKBOOK',64,194,830,24,16,'stage_accent',True,role='label')
                self.text(s,block['text'],64,229,830,110,24,'stage_ink')
                assert len(d.get('points',[]))<=3, 'Reflow demo points; never silently omit an instruction.'
                for j,point in enumerate(d.get('points',[])):
                    self.text(s,point,58,365+j*36,840,34,22)
            elif d['kind']=='statement':
                self.rect(s,48,188,864,140,'panel')
                self.text(s,'DATA · NOT AN INSTRUCTION',64,197,820,24,16,'brand_blue',True,role='label')
                self.text(s,d['blocks'][0]['text'],64,238,820,80,28,'ink',True)
                self.text(s,d['statement'],48,370,864,90,28,'ink',True)
            elif d['kind']=='break':
                self.text(s,'Five-minute break',48,205,864,60,36,'brand_blue',True)
                self.text(s,d['statement'],48,295,864,120,28)
            else:
                points=d.get('items',d.get('points',[]))
                step=55 if len(points)>4 else 66 if len(points)==4 else 83
                for j,point in enumerate(points):
                    self.text(s,f'{j+1:02}',48,190+j*step,55,42,24,'brand_blue',True)
                    self.text(s,point,118,188+j*step,790,step-4,26 if len(points)<5 else 24)
            if dark:
                logo=ROOT/'Files/Mark-Title-COLOR-ForDarkBG.png'
                with Image.open(logo) as im:
                    height=220*im.height/im.width
                pic=s.shapes.add_picture(str(logo),Pt(690),Pt(478-height),width=Pt(220))
                pic._element.nvPicPr.cNvPr.set('descr','Orange County Department of Education logo')
            self.rect(s,48,500,864,1,'hairline')
            ref=d.get('workbook_ref','AI for Cyber Security · Kevin Riley')
            self.text(s,ref,48,511,760,22,14,fg,role='meta')
            self.text(s,d['id'],846,511,66,22,14,fg,role='meta')
            notes=(f"{d['id']} · elapsed {d['elapsed']} · {d['minutes']} minutes\n"
                   + ('HIDDEN SUPPORT: zero added minutes; return to parent after use.\n' if d.get('hidden') else '')
                   + d['notes'] + '\n\nWORKBOOK: '+ref
                   + '\nSOURCE MAPPING: '+ '; '.join(d.get('source_mapping',[])))
            for prompt in d.get('full_workbook_prompts',[]):
                notes += '\n\nFULL WORKBOOK PROMPT / INSTRUCTION\n'+prompt
            s.notes_slide.notes_text_frame.text=notes
        # Explicit internal links make hidden support reachable without showing it in the timed sequence.
        by_id={d['id']:s for d,s in zip(DATA,self.p.slides)}
        for d,s in zip(DATA,self.p.slides):
            if d.get('hidden'):
                parent=by_id[f'C{d["parent_slide"]:02}']
                target=self.text(s,'Return to lab',700,473,210,25,16,'brand_blue',True,role='label')
                target.click_action.target_slide=parent
            else:
                supports=[x for x in DATA if x.get('parent_slide')==d.get('slide')]
                for j,x in enumerate(supports):
                    label={'S07A':'Routes & setup','S14A':'Commands','S14B':'Checker help','S18A':'Report checks'}[x['id']]
                    target=self.text(s,label,540+j*190,376,182,24,16,'brand_blue',True,role='link')
                    target.click_action.target_slide=by_id[x['id']]
        OUT.mkdir(exist_ok=True)
        path=OUT/'CITE-AI-Cybersecurity-Workshop.pptx'
        self.p.save(path)
        (HERE/'text-fit-report.json').write_text(json.dumps(self.metrics,indent=2)+'\n')
        print(f'Built {path}: 21 core + 4 hidden support slides, editable text, notes; NOT RENDERED.')

    @staticmethod
    def phase(n):
        return ('WELCOME' if n<3 else 'WARM-UP' if n<7 else 'READINESS' if n==7 else
                'LAB 1 · POLICY' if n<12 else 'BREAK' if n==12 else 'LAB 2 · TRIAGE' if n<16 else
                'REVIEW HABIT' if n==16 else 'LAB 3 · LOCAL REPORT' if n<20 else 'CLOSE')

    def lab(self,s,d):
        self.rect(s,48,174,864,40,'stage')
        self.text(s,f'{d["minutes"]} MINUTES · STOP AT {d["end_minute"]}',62,182,565,30,20,'stage_ink',True)
        self.text(s,d.get('provenance','SYNTHETIC'),650,185,245,25,16,'stage_accent',True,role='label')
        for j,step in enumerate(d['steps']):
            self.text(s,f'{j+1}. {step}',52,225+j*30,856,29,20)
        phases='  /  '.join(f'{label}: {mins}m' for label,mins in d.get('phases',[]))
        self.text(s,phases,48,350,864,25,16,'brand_blue',role='label')
        for x,label,text in [(48,'DONE WHEN',d['done_when']),(490,'STUCK?',d['fallback'])]:
            card=self.rect(s,x,402,422,88,'panel')
            card.name='Lab card · '+label
            self.text(s,label,x+10,404,402,24,16,'brand_blue',True,role='label')
            self.text(s,text,x+10,431,402,52,20,role='body-card')

    def support(self,s,d):
        for j,point in enumerate(d.get('points',[])):
            self.text(s,point,48,178+j*35,864,34,22)
        if d.get('code'):
            self.rect(s,48,297,864,150,'stage')
            self.text(s,'UBUNTU / WSL BASH · NORMAL USER · KIT COPY',62,303,835,24,16,'stage_accent',True,role='label')
            self.text(s,d['code'],62,334,835,109,20,'stage_ink',font='Consolas')
        else:
            self.text(s,d['fallback'],48,332,864,110,24,'brand_blue')

if __name__=='__main__':
    Builder().build()
