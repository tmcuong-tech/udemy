#!/usr/bin/env python3
"""Theme reskin of the AWS AI Practitioner deck toward the CLSSGB house design.

Keeps all 374 slides, layouts and images. Applies a VISIBLE house treatment:
  - Arial on every run.
  - A brand-blue accent bar (#1F6FEB) under every content-slide title.
  - Section dividers (Domain / Task / Topic) restyled to the eyebrow+title look:
    the label becomes an UPPERCASE blue eyebrow over a dark bold title.
  - Cover restyled to Arial; version bumped to 12.0.
Content slides keep their existing layouts/images (reskin, not a rebuild).
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(REPO, "courseware", "WSQ - Master Trainer Slides - AWS Certified AI Practitioner Training - v11.pptx")
DST  = os.path.join(REPO, "courseware", "WSQ - Master Trainer Slides - AWS Certified AI Practitioner Training - v12.pptx")

DARK  = RGBColor(0x16, 0x1B, 0x26)
BLUE  = RGBColor(0x1F, 0x6F, 0xEB)
GREY  = RGBColor(0x5B, 0x63, 0x72)

def add_accent_bar(slide, prs, title):
    """Full-width thin brand bar just under the title."""
    y = title.top + title.height - Inches(0.02)
    if y > prs.slide_height - Inches(0.2):        # guard: don't drop it off-slide
        y = title.top + title.height
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), y,
                                 prs.slide_width - Inches(1.0), Inches(0.055))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    try: bar.shadow.inherit = False
    except Exception: pass
    return bar

def main():
    p = Presentation(SRC)
    slides = list(p.slides)
    arial = bars = dividers = 0

    for si, s in enumerate(slides, 1):
        is_divider = s.slide_layout.name == "SECTION_HEADER"

        # Arial on every run
        for sh in s.shapes:
            if sh.has_text_frame:
                for para in sh.text_frame.paragraphs:
                    for r in para.runs:
                        r.font.name = "Arial"; arial += 1

        if is_divider:
            cand = None
            for sh in s.shapes:
                if sh.has_text_frame and len([1 for pa in sh.text_frame.paragraphs if pa.text.strip()]) >= 2:
                    cand = sh; break
            if cand is None:
                cand = max((sh for sh in s.shapes if sh.has_text_frame),
                           key=lambda sh: len(sh.text_frame.text), default=None)
            if cand is not None:
                seen = 0
                for pa in cand.text_frame.paragraphs:
                    if not pa.text.strip():
                        continue
                    seen += 1
                    for r in pa.runs:
                        r.font.name = "Arial"; r.font.bold = True
                        if seen == 1:
                            r.text = r.text.upper()
                            try: r.font.color.rgb = BLUE
                            except Exception: pass
                        else:
                            try: r.font.color.rgb = DARK
                            except Exception: pass
                dividers += 1
            continue   # dividers get the eyebrow, not the underline bar

        if si == 1:   # cover: Arial + version bump, no bar
            for sh in s.shapes:
                if sh.has_text_frame:
                    for pa in sh.text_frame.paragraphs:
                        for r in pa.runs:
                            r.font.name = "Arial"
                            if "Version:" in r.text:
                                r.text = r.text.replace("11.0", "12.0").replace("11", "12") if "11" in r.text else r.text
            continue

        # content/admin slides: brand accent bar under the title
        title = None
        try: title = s.shapes.title
        except Exception: pass
        if title is not None and title.top is not None:
            add_accent_bar(s, p, title); bars += 1

    p.save(DST)
    print("saved", os.path.basename(DST))
    print(f"  slides:{len(slides)}  Arial runs:{arial}  accent bars:{bars}  divider eyebrows:{dividers}")

if __name__ == "__main__":
    main()
