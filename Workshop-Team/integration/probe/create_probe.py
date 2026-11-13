from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

out = Path(__file__).resolve().parent
p = Presentation()
p.slide_width, p.slide_height = Inches(13.333333), Inches(7.5)
s = p.slides.add_slide(p.slide_layouts[5])
t = s.shapes.title
t.left, t.top, t.width, t.height = Inches(.67), Inches(.8), Inches(12), Inches(1.3)
t.text = 'Native PowerPoint renderer probe'
t.text_frame.paragraphs[0].font.size = Pt(36)
t.text_frame.paragraphs[0].font.name = 'Arial'
b = s.shapes.add_textbox(Inches(.67), Inches(2.5), Inches(11.5), Inches(2))
b.text_frame.word_wrap = True
b.text_frame.text = 'Editable text • 16:9 slide\nOne logical text block. This is a tooling probe.'
for para in b.text_frame.paragraphs:
    para.font.name, para.font.size = 'Arial', Pt(24)
    para.font.color.rgb = RGBColor.from_string('155191')
s.notes_slide.notes_text_frame.text = 'Probe only. Native PDF must be exported from this actual editable PPTX. No workshop build.'
p.save(out / 'renderer-probe.pptx')
print(out / 'renderer-probe.pptx')
