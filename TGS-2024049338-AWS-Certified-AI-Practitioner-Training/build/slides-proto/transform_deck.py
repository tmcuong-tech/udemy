#!/usr/bin/env python3
"""Generalised 1:1 deck transform: any source .pptx -> the house component design,
KEEPING THE SAME SLIDE COUNT and all content + screenshots.

Usage:
    python3 transform_deck.py <source.pptx> <output.pptx> [eyebrow]

For each source slide it emits ONE house-styled slide:
  slide 1              -> cover()
  Domain/Task/Topic /
    SECTION_HEADER     -> section()  (eyebrow + big title + left bar)
  slide with a picture -> framed picture()  (biggest embedded image + house header/footer)
  short text list      -> tile_grid()
  everything else      -> content()  (house-styled bullets)
Screenshots are extracted from the source into assets/screens_<tag>/ and downscaled at build
time is left to a later compression pass. Loads the component library from build_slides.py
without running its BUILD section.
"""
import os, re, sys, io
from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "v11-work.pptx")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "..", "courseware", "TRANSFORMED.pptx")
EYEBROW = sys.argv[3] if len(sys.argv) > 3 else "COURSE SLIDES  ·  WSQ"
TAG = re.sub(r'\W+', '', os.path.splitext(os.path.basename(OUT))[0])[:20] or "deck"
SCRDIR = os.path.join(HERE, "assets", f"screens_{TAG}")
os.makedirs(SCRDIR, exist_ok=True)

# ---- load component library (everything before the BUILD marker) ----
_src = open(os.path.join(HERE, "build_slides.py"), encoding="utf-8").read()
_comp = _src.split("# ============================================================ BUILD")[0]
# point ASSETS/screens at this deck's screenshot dir by overriding ASSETS resolution
NS = {"__file__": os.path.join(HERE, "build_slides.py")}
exec(compile(_comp, "build_slides.py", "exec"), NS)
# redirect picture() to this deck's screen dir: patch os.path.join in picture via a wrapper
_ASSETS = NS["ASSETS"]
def PIC(title, image_file, caption=None, kicker=None):
    # image_file is an absolute path here
    saved = NS["ASSETS"]
    return NS["picture"](title, os.path.relpath(image_file, os.path.join(saved, "screens")) if False else image_file,
                         caption=caption, kicker=kicker)
cover, section, content, tile_grid, picture = NS["cover"], NS["section"], NS["content"], NS["tile_grid"], NS["picture"]
prs = NS["prs"]

# make picture() accept an absolute path: monkeypatch by putting files under ASSETS/screens
SCREENS_UNDER_ASSETS = os.path.join(_ASSETS, "screens")
os.makedirs(SCREENS_UNDER_ASSETS, exist_ok=True)

# Per-slide content overrides: title-substring (lowercased) -> (kicker, [bullets]).
# Used where the original slide is a stock image with no usable text (e.g. the ice-breaker).
OVERRIDES = {
    "let's know each other": ("ICE-BREAKER", [
        "Your name and organisation / role.",
        "Your experience with AI, machine learning or AWS (if any).",
        "What you want to build with AI on AWS after this course."]),
    "lets know each other": ("ICE-BREAKER", [
        "Your name and organisation / role.",
        "Your experience with AI, machine learning or AWS (if any).",
        "What you want to build with AI on AWS after this course."]),
}

DOMWT = {1:"20%",2:"24%",3:"28%",4:"14%",5:"14%"}
DOMNAME = {1:"Fundamentals of AI and ML",2:"Fundamentals of Generative AI",
           3:"Applications of Foundation Models",4:"Guidelines for Responsible AI",
           5:"Security, Compliance, and Governance for AI Solutions"}

def slide_text(s):
    lines=[]
    for sh in s.shapes:
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                t=para.text.strip()
                if t: lines.append(t)
    lines=[l for l in lines if l not in ("#","") and "Maarek" not in l
           and not l.startswith("©") and not re.fullmatch(r'[\W_]{0,3}#[\W_]{0,3}', l)]
    title=lines[0] if lines else ""
    return title, lines[1:]

def biggest_pic(s):
    best=None; area=0
    for sh in s.shapes:
        if "PICTURE" in str(sh.shape_type):
            try:
                a=Emu(sh.width).inches*Emu(sh.height).inches
                if a>3.0 and a>area:
                    area=a; best=sh
            except: pass
    return best

def extract(sh, n, j):
    img=sh.image; fn=f"{TAG}_s{n:03d}_{j}.{img.ext}"
    path=os.path.join(SCREENS_UNDER_ASSETS, fn)
    open(path,"wb").write(img.blob)
    return fn

def is_short_list(body):
    return 2<=len(body)<=6 and all(len(b)<=70 for b in body)

def main():
    p=Presentation(SRC); sl=list(p.slides)
    cur_kicker=None; stats={"cover":0,"section":0,"picture":0,"tile":0,"content":0}
    # override the cover eyebrow for this deck
    for i,s in enumerate(sl,1):
        title, body = slide_text(s)
        low=title.lower()
        if i==1:
            cover(); stats["cover"]+=1; continue
        mdom=re.match(r'domain\s*([1-5])',low); mtask=re.match(r'task\s*([1-5]\.\d)',low); mtopic=re.match(r'topic\s*(\d+)',low)
        if s.slide_layout.name=="SECTION_HEADER" or mdom or mtask or mtopic:
            if mdom:
                d=int(mdom.group(1)); nm=body[0] if body else DOMNAME.get(d,"")
                if "fundamental of al" in nm.lower(): nm=DOMNAME[d]
                section(f"DOMAIN {d}", nm or DOMNAME[d], DOMWT.get(d,""), sub=f"Exam weighting {DOMWT.get(d,'')} · {DOMNAME.get(d,'')}")
                cur_kicker=f"DOMAIN {d}"
            elif mtask:
                section(f"TASK {mtask.group(1)}", body[0] if body else title, ""); cur_kicker=f"TASK {mtask.group(1)}"
            elif mtopic:
                section(f"TOPIC {mtopic.group(1)}", body[0] if body else title, ""); cur_kicker=f"TOPIC {mtopic.group(1)}"
            else:
                section(title.upper() if len(title)<30 else "SECTION", body[0] if body else title, ""); cur_kicker=None
            stats["section"]+=1; continue
        # content override (e.g. ice-breaker): force the house bullet layout, ignore the stock image
        ov=next((v for k,v in OVERRIDES.items() if k in low), None)
        if ov:
            content(title.rstrip(". "), ov[1], kicker=ov[0]); stats["content"]+=1; continue
        pic=biggest_pic(s)
        if pic is not None:
            fn=extract(pic, i, 0)
            cap=body[0] if (body and len(body[0])<=120) else None
            picture(title or "Reference", fn, caption=cap, kicker=cur_kicker); stats["picture"]+=1; continue
        if not title and not body:
            content("", [" "], kicker=cur_kicker); stats["content"]+=1; continue
        if is_short_list(body):
            tile_grid(title or "Overview", body, kicker=cur_kicker, cols=(2 if len(body)<=4 else 3), size=15); stats["tile"]+=1
        else:
            items=body if body else [title]
            content(title or "", items, kicker=cur_kicker, size=(18 if len(items)>6 else 20)); stats["content"]+=1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    print(f"saved {os.path.basename(OUT)}  ({len(prs.slides._sldIdLst)} slides; source had {len(sl)})")
    print("  ", stats)

if __name__=="__main__":
    main()
